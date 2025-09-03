from typing import Any, Dict

import pytest

from zotify_api.services.network_service import NetworkService


@pytest.fixture
def network_config() -> Dict[str, Any]:
    return {"proxy_enabled": False, "http_proxy": None, "https_proxy": None}


def test_get_network_config(network_config: Dict[str, Any]) -> None:
    service = NetworkService(network_config)
    config = service.get_network_config()
    assert config == network_config


def test_update_network_config(network_config: Dict[str, Any]) -> None:
    service = NetworkService(network_config)
    update_data = {"proxy_enabled": True, "http_proxy": "http://proxy.local:3128"}
    config = service.update_network_config(update_data)
    assert config["proxy_enabled"] is True
    assert config["http_proxy"] == "http://proxy.local:3128"
