import base64
import hashlib
import inspect
import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote_plus

import httpx
from sqlalchemy.orm import Session

from zotify_api.auth_state import (
    CLIENT_ID,
    REDIRECT_URI,
    SPOTIFY_AUTH_URL,
    SPOTIFY_TOKEN_URL,
    pending_states,
)
from zotify_api.core.logging_framework import log_event
from zotify_api.database import crud
from zotify_api.services.spoti_client import SpotiClient

from .base import BaseProvider

logger = logging.getLogger(__name__)


class SpotifyConnector(BaseProvider):
    """
    Provider connector for the Spotify music service. It uses the SpotiClient
    to interact with the Spotify API.
    """

    def __init__(self, db: Session, client: Optional[SpotiClient] = None):
        self.db = db
        self.client = client

    async def get_oauth_login_url(self, state: str) -> str:
        """Constructs the provider-specific URL for OAuth2 authorization."""
        scopes = [
            "ugc-image-upload",
            "user-read-playback-state",
            "user-modify-playback-state",
            "user-read-currently-playing",
            "app-remote-control",
            "streaming",
            "playlist-read-private",
            "playlist-read-collaborative",
            "playlist-modify-private",
            "playlist-modify-public",
            "user-follow-modify",
            "user-follow-read",
            "user-read-playback-position",
            "user-top-read",
            "user-read-recently-played",
            "user-library-modify",
            "user-library-read",
            "user-read-email",
            "user-read-private",
        ]
        scope = " ".join(scopes)

        code_verifier = (
            base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
        )
        code_challenge = (
            base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
            .rstrip(b"=")
            .decode()
        )

        pending_states[state] = code_verifier

        auth_url = (
            f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={quote_plus(REDIRECT_URI)}"
            f"&scope={quote_plus(scope)}"
            f"&state={state}"
            f"&code_challenge_method=S256"
            f"&code_challenge={code_challenge}"
        )
        return auth_url

    async def handle_oauth_callback(
        self, code: Optional[str], error: Optional[str], state: str
    ) -> str:
        """
        Handles the callback from the OAuth2 provider.

        This processes either the authorization code or an error. Returns HTML
        content for the popup window.
        """
        if error:
            log_event(
                "Spotify authentication failed by user.",
                level="WARN",
                tags=["security"],
                details={"error": error, "state": state},
            )
            return f"""
            <html><head><title>Authentication Failed</title></head>
            <body>
                <h2>Authentication Failed</h2>
                <p>Reason: {error}</p>
                <button onclick="window.close()">OK</button>
            </body></html>
            """

        if not code:
            return (
                "<html><body><h2>Error</h2>"
                "<p>Missing authorization code.</p></body></html>"
            )

        code_verifier = pending_states.pop(state, None)
        if not code_verifier:
            log_event(
                "Invalid or expired state received in Spotify callback",
                level="ERROR",
                tags=["security"],
                details={"state": state},
            )
            return """
            <html><body><h2>Error</h2>
            <p>Invalid or expired state token. Please try logging in again.</p>
            </body></html>
            """

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "code_verifier": code_verifier,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
                resp.raise_for_status()

                tokens = resp.json()

                expires_at = datetime.now(timezone.utc) + timedelta(
                    seconds=tokens["expires_in"] - 60
                )
                token_data = {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens.get("refresh_token"),
                    "expires_at": expires_at,
                }
                crud.create_or_update_spotify_token(self.db, token_data=token_data)

                log_event(
                    "Spotify authentication successful", level="INFO", tags=["security"]
                )
                return """
                <html><head><title>Authentication Success</title></head>
                <body><p>Successfully authenticated. You can close this window.</p>
                <script>window.close();</script></body></html>
                """

        except httpx.HTTPStatusError as e:
            log_event(
                "Failed to get token from Spotify",
                level="ERROR",
                tags=["security"],
                details={
                    "status_code": e.response.status_code,
                    "response": e.response.text,
                },
            )
            return f"""
            <html><body><h2>Error</h2>
            <p>Failed to retrieve token. Status: {e.response.status_code}</p>
            </body></html>
            """
        except Exception as e:
            logger.error(f"An unexpected error occurred during Spotify callback: {e}")
            return (
                "<html><body><h2>Error</h2>"
                "<p>An unexpected error occurred.</p></body></html>"
            )

    async def search(
        self, q: str, type: str, limit: int, offset: int
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Search for tracks, albums, or artists on Spotify."""
        if not self.client:
            raise Exception("SpotiClient not initialized.")
        results = await self.client.search(q=q, type=type, limit=limit, offset=offset)
        for key in results:
            if "items" in results[key]:
                return results[key]["items"], results[key].get("total", 0)
        return [], 0

    async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """Get a single playlist from Spotify."""
        client = self.client
        if not client:
            raise Exception("SpotiClient not initialized.")
        playlist_data: Dict[str, Any] = await client.get_playlist(playlist_id)
        return playlist_data

    async def get_playlist_tracks(
        self, playlist_id: str, limit: int, offset: int
    ) -> Dict[str, Any]:
        """Get the tracks in a playlist from Spotify."""
        client = self.client
        if not client:
            raise Exception("SpotiClient not initialized.")
        tracks_data: Dict[str, Any] = await client.get_playlist_tracks(
            playlist_id, limit=limit, offset=offset
        )
        return tracks_data

    async def sync_playlists(self) -> Dict[str, Any]:
        """Fetch user's playlists from Spotify and save to the database."""
        if not self.client:
            raise Exception("SpotiClient not initialized.")
        spotify_playlists = await self.client.get_all_current_user_playlists()
        crud.clear_all_playlists_and_tracks(self.db)
        for playlist_data in spotify_playlists:
            playlist_id = playlist_data.get("id")
            playlist_name = playlist_data.get("name")
            if not playlist_id or not playlist_name:
                continue
            track_items = playlist_data.get("tracks", {}).get("items", [])
            track_ids = []
            for item in track_items:
                if track := item.get("track"):
                    if track_id := track.get("id"):
                        track_ids.append(track_id)

            crud.create_or_update_playlist(
                db=self.db,
                playlist_id=playlist_id,
                playlist_name=playlist_name,
                track_ids=track_ids,
            )
        return {
            "status": "success",
            "message": f"Successfully synced {len(spotify_playlists)} playlists.",
            "count": len(spotify_playlists),
        }
