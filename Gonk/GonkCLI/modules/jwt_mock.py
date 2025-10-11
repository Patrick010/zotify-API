# ID: API-007
import requests

class JWTClient:
    def __init__(self, api_base_url="http://localhost:8000"):
        self.api_base_url = api_base_url
        self.token = None

    def register(self, username, password):
        response = requests.post(
            f"{self.api_base_url}/api/auth/register",
            json={"username": username, "password": password},
        )
        response.raise_for_status()
        return response.json()

    def _get_auth_headers(self):
        if not self.token:
            raise Exception("Not logged in")
        return {"Authorization": f"Bearer {self.token}"}

    def login(self, username, password):
        response = requests.post(
            f"{self.api_base_url}/api/auth/login",
            data={"username": username, "password": password},
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]
        return self.token

    def get_profile(self):
        response = requests.get(
            f"{self.api_base_url}/api/user/profile",
            headers=self._get_auth_headers(),
        )
        response.raise_for_status()
        return response.json()

    def update_preferences(self, theme=None, language=None, notifications_enabled=None):
        payload = {}
        if theme is not None:
            payload["theme"] = theme
        if language is not None:
            payload["language"] = language
        if notifications_enabled is not None:
            payload["notifications_enabled"] = notifications_enabled

        response = requests.patch(
            f"{self.api_base_url}/api/user/preferences",
            headers=self._get_auth_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    def get_liked_tracks(self):
        response = requests.get(
            f"{self.api_base_url}/api/user/liked",
            headers=self._get_auth_headers(),
        )
        response.raise_for_status()
        return response.json()

    def get_history(self):
        response = requests.get(
            f"{self.api_base_url}/api/user/history",
            headers=self._get_auth_headers(),
        )
        response.raise_for_status()
        return response.json()

    def clear_history(self):
        response = requests.delete(
            f"{self.api_base_url}/api/user/history",
            headers=self._get_auth_headers(),
        )
        response.raise_for_status()
        return response.status_code == 204
