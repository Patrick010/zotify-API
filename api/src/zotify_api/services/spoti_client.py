import logging
from typing import Any, Dict, List, Optional

import httpx
from fastapi import HTTPException

from zotify_api.auth_state import SPOTIFY_API_BASE

logger = logging.getLogger(__name__)


class SpotiClient:
    """
    A stateless client for interacting with the Spotify Web API.
    It must be initialized with an access token.
    """

    def __init__(self, access_token: str, refresh_token: Optional[str] = None):
        if not access_token:
            raise ValueError("SpotiClient must be initialized with an access token.")
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._client = httpx.AsyncClient(base_url=SPOTIFY_API_BASE)

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Makes an authenticated request to the Spotify API.
        """
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._access_token}"

        try:
            response = await self._client.request(
                method, url, headers=headers, **kwargs
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.warning("Spotify access token is invalid or expired.")
            logger.error(
                f"Spotify API request failed: {e.response.status_code} - {e.response.text}"
            )
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text
            )
        except httpx.RequestError as e:
            logger.error(f"Could not connect to Spotify API: {e}")
            raise HTTPException(
                status_code=503,
                detail="Service unavailable: Could not connect to Spotify.",
            )

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

    async def search(
        self, q: str, type: str, limit: int, offset: int
    ) -> Dict[str, Any]:
        """
        Performs a search on Spotify.
        """
        params = {
            "q": q,
            "type": type,
            "limit": limit,
            "offset": offset,
        }
        response = await self._request("GET", "/search", params=params)
        return response.json()

    async def get_current_user_playlists(
        self, limit: int = 20, offset: int = 0
    ) -> Dict[str, Any]:
        """
        Gets a list of the playlists owned or followed by the current user.
        """
        params = {"limit": limit, "offset": offset}
        response = await self._request("GET", "/me/playlists", params=params)
        return response.json()

    async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """
        Gets a playlist owned by a Spotify user.
        """
        response = await self._request("GET", f"/playlists/{playlist_id}")
        return response.json()

    async def get_playlist_tracks(
        self, playlist_id: str, limit: int = 100, offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get full details of the items of a playlist owned by a Spotify user.
        """
        params = {"limit": limit, "offset": offset}
        response = await self._request(
            "GET", f"/playlists/{playlist_id}/tracks", params=params
        )
        return response.json()

    async def get_all_current_user_playlists(self) -> List[Dict[str, Any]]:
        """
        Gets a list of all playlists owned or followed by the current user, handling pagination.
        """
        all_playlists = []
        url = "/me/playlists"
        params = {"limit": 50}

        while url:
            response = await self._request("GET", url, params=params)
            data = response.json()
            all_playlists.extend(data.get("items", []))
            url = data.get("next")
            params = {}  # params are included in the 'next' URL

        return all_playlists

    async def create_playlist(
        self,
        user_id: str,
        name: str,
        public: bool,
        collaborative: bool,
        description: str,
    ) -> Dict[str, Any]:
        """
        Creates a new playlist for a Spotify user.
        """
        data = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description,
        }
        response = await self._request("POST", f"/users/{user_id}/playlists", json=data)
        return response.json()

    async def update_playlist_details(
        self,
        playlist_id: str,
        name: str,
        public: bool,
        collaborative: bool,
        description: str,
    ) -> None:
        """
        Updates the details of a playlist.
        """
        data = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description,
        }
        await self._request("PUT", f"/playlists/{playlist_id}", json=data)

    async def add_tracks_to_playlist(
        self, playlist_id: str, uris: List[str]
    ) -> Dict[str, Any]:
        """
        Adds one or more items to a user's playlist.
        """
        data = {"uris": uris}
        response = await self._request(
            "POST", f"/playlists/{playlist_id}/tracks", json=data
        )
        return response.json()

    async def remove_tracks_from_playlist(
        self, playlist_id: str, uris: List[str]
    ) -> Dict[str, Any]:
        """
        Removes one or more items from a user's playlist.
        """
        data = {"tracks": [{"uri": uri} for uri in uris]}
        response = await self._request(
            "DELETE", f"/playlists/{playlist_id}/tracks", json=data
        )
        return response.json()

    async def unfollow_playlist(self, playlist_id: str) -> None:
        """
        Unfollows a playlist for the current user. (Spotify's way of "deleting" a playlist from a user's library)
        """
        await self._request("DELETE", f"/playlists/{playlist_id}/followers")

    async def close(self):
        """Closes the underlying httpx client."""
        await self._client.aclose()

    @staticmethod
    async def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
        """
        Refreshes the Spotify access token using the refresh token.
        This is a static method as it does not depend on the client's state.
        """
        from zotify_api.auth_state import CLIENT_ID, CLIENT_SECRET, SPOTIFY_TOKEN_URL

        if not refresh_token:
            raise HTTPException(status_code=400, detail="No refresh token available.")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    SPOTIFY_TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET)
                )
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to refresh token: {e.response.text}",
                )
            except httpx.RequestError:
                raise HTTPException(
                    status_code=503,
                    detail="Service unavailable: Could not connect to Spotify.",
                )

    @staticmethod
    async def exchange_code_for_token(code: str, code_verifier: str) -> Dict[str, Any]:
        """
        Exchanges an authorization code for an access token.
        This is a static method as it does not depend on the client's state.
        """
        from zotify_api.auth_state import CLIENT_ID, REDIRECT_URI, SPOTIFY_TOKEN_URL

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "code_verifier": code_verifier,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to exchange code for token: {e.response.text}",
                )
            except httpx.RequestError:
                raise HTTPException(
                    status_code=503,
                    detail="Service unavailable: Could not connect to Spotify.",
                )
