from unittest.mock import mock_open, patch

from fastapi.testclient import TestClient

from zotify_api.main import app

client = TestClient(app)


def test_get_system_info_unauthorized():
    response = client.get("/api/system/info")
    assert response.status_code == 401


def test_get_system_info():
    response = client.get("/api/system/info", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "system" in data["data"]
    assert "python_version" in data["data"]


def test_get_logs_unauthorized():
    response = client.get("/api/system/logs")
    assert response.status_code == 401


def test_get_logs():
    response = client.get("/api/system/logs", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


def test_get_config_unauthorized():
    response = client.get("/api/system/config")
    assert response.status_code == 401


def test_get_config():
    response = client.get("/api/system/config", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "version" in data["data"]


@patch("zotify_api.main.settings.config_path", "/tmp/config.json")
@patch("builtins.open", new_callable=mock_open, read_data='{"test": "test"}')
@patch("json.load", return_value={"test": "test"})
def test_get_config_file(mock_json_load, mock_file_open):
    response = client.get("/api/system/config/file", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    mock_file_open.assert_called_with("/tmp/config.json", "r")
    assert response.json() == {"data": {"test": "test"}}
