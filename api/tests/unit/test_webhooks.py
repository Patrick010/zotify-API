from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from zotify_api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_webhooks(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    monkeypatch.setattr("zotify_api.services.webhooks.webhooks", {})


def test_register_webhook_unauthorized(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.post(
        "/api/webhooks/register",
        headers={"X-API-Key": "wrong_key"},
        json={"url": "http://test.com", "events": ["test_event"]},
    )
    assert response.status_code == 401


def test_register_webhook(monkeypatch):
    response = client.post(
        "/api/webhooks/register",
        headers={"X-API-Key": "test_key"},
        json={"url": "http://test.com", "events": ["test_event"]},
    )
    assert response.status_code == 201
    assert "id" in response.json()["data"]


def test_list_webhooks():
    response = client.get("/api/webhooks", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)


def test_unregister_webhook():
    reg_response = client.post(
        "/api/webhooks/register",
        headers={"X-API-Key": "test_key"},
        json={"url": "http://test.com", "events": ["test_event"]},
    )
    webhook_id = reg_response.json()["data"]["id"]
    response = client.delete(
        f"/api/webhooks/{webhook_id}", headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 204
    response = client.get("/api/webhooks", headers={"X-API-Key": "test_key"})
    assert len(response.json()["data"]) == 0


@patch("zotify_api.services.webhooks.httpx.post")
def test_fire_webhook(mock_post):
    client.post(
        "/api/webhooks/register",
        headers={"X-API-Key": "test_key"},
        json={"url": "http://test.com", "events": ["test_event"]},
    )

    # Test without API key
    response = client.post(
        "/api/webhooks/fire", json={"event": "test_event", "data": {}}
    )
    assert response.status_code == 401

    # Test with API key
    response = client.post(
        "/api/webhooks/fire",
        headers={"X-API-Key": "test_key"},
        json={"event": "test_event", "data": {}},
    )
    assert response.status_code == 202
    mock_post.assert_called_once()
