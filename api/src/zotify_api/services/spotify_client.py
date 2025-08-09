import httpx
import logging
import time
from typing import List, Dict, Any, Optional

from zotify_api.auth_state import spotify_tokens, SPOTIFY_API_BASE, save_tokens
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class SpotifyClient:
    """
    A client for interacting with the Spotify Web API.
    Handles authentication and token refreshing.
    """

    def __init__(self, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        self._access_token = access_token or spotify_tokens.get("access_token")
        self._refresh_token = refresh_token or spotify_tokens.get("refresh_token")
        self._client = httpx.AsyncClient(base_url=SPOTIFY_API_BASE)

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Makes an authenticated request to the Spotify API.
        Handles token validation and refreshing.
        """
        if not self._access_token:
            raise HTTPException(status_code=401, detail="Not authenticated with Spotify.")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._access_token}"

        try:
            response = await self._client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # Token expired, try to refresh
                logger.info("Spotify access token expired. Refreshing...")
                # Placeholder for refresh logic
                # await self.refresh_access_token()
                # headers["Authorization"] = f"Bearer {self._access_token}"
                # response = await self._client.request(method, url, headers=headers, **kwargs)
                # response.raise_for_status()
                # return response
                raise HTTPException(status_code=401, detail="Spotify token expired. Refresh functionality not yet implemented.")
            logger.error(f"Spotify API request failed: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            logger.error(f"Could not connect to Spotify API: {e}")
            raise HTTPException(status_code=503, detail="Service unavailable: Could not connect to Spotify.")

    async def get_tracks_metadata(self, track_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieves metadata for multiple tracks from the Spotify API.
        """
        if not track_ids:
            return []

        params = {"ids": ",".join(track_ids)}
        response = await self._request("GET", "/tracks", params=params)
        return response.json().get("tracks", [])

    async def get_current_user(self) -> Dict[str, Any]:
        """
        Retrieves the profile of the current user.
        """
        response = await self._request("GET", "/me")
        return response.json()

    async def get_devices(self) -> List[Dict[str, Any]]:
        """
        Retrieves the list of available playback devices for the current user.
        """
        response = await self._request("GET", "/me/player/devices")
        return response.json().get("devices", [])

    async def close(self):
        """Closes the underlying httpx client."""
        await self._client.aclose()

    async def refresh_access_token(self) -> None:
        """
        Refreshes the Spotify access token using the refresh token.
        """
        from zotify_api.auth_state import CLIENT_ID, CLIENT_SECRET, SPOTIFY_TOKEN_URL

        if not self._refresh_token:
            raise HTTPException(status_code=400, detail="No refresh token available.")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(SPOTIFY_TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
                resp.raise_for_status()
                new_tokens = resp.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=400, detail=f"Failed to refresh token: {e.response.text}")
            except httpx.RequestError:
                raise HTTPException(status_code=503, detail="Service unavailable: Could not connect to Spotify.")

        self._access_token = new_tokens["access_token"]
        spotify_tokens["access_token"] = new_tokens["access_token"]
        spotify_tokens["expires_at"] = time.time() + new_tokens["expires_in"] - 60
        if "refresh_token" in new_tokens:
            self._refresh_token = new_tokens["refresh_token"]
            spotify_tokens["refresh_token"] = new_tokens["refresh_token"]

        save_tokens(spotify_tokens)
