# ID: API-055
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class BaseProvider(ABC):
    """
    Abstract Base Class for a music service provider.
    Defines the interface that all provider connectors must implement.
    """

    @abstractmethod
    async def search(
        self, q: str, type: str, limit: int, offset: int
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Search for tracks, albums, or artists."""
        pass

    @abstractmethod
    async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """Get a single playlist."""
        pass

    @abstractmethod
    async def get_playlist_tracks(
        self, playlist_id: str, limit: int, offset: int
    ) -> Dict[str, Any]:
        """Get the tracks in a playlist."""
        pass

    @abstractmethod
    async def sync_playlists(self) -> Dict[str, Any]:
        """Sync all playlists from the provider to the local database."""
        pass

    # Add other abstract methods for all the operations that need to be supported
    # across all providers, e.g.:
    #
    # @abstractmethod
    # async def get_track(self, track_id: str) -> Dict[str, Any]:
    #     pass
    #
    # @abstractmethod
    # async def get_album(self, album_id: str) -> Dict[str, Any]:
    #     pass
    #
    # @abstractmethod
    # async def get_artist(self, artist_id: str) -> Dict[str, Any]:
    #     pass

    @abstractmethod
    async def get_oauth_login_url(self, state: str) -> str:
        """Constructs the provider-specific URL for OAuth2 authorization."""
        pass

    @abstractmethod
    async def handle_oauth_callback(
        self, code: Optional[str], error: Optional[str], state: str
    ) -> str:
        """
        Handles the callback from the OAuth2 provider.

        This processes either the authorization code or an error. Returns HTML
        content for the popup window.
        """
        pass

    # For now, we will keep it simple and only include the methods that are
    # currently being used in the spotify service.
