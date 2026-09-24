from framework.clients.openwebui_client import OpenWebUIClient

def test_open_webui_version():
    client = OpenWebUIClient()

    
    response = client.get_version()

    assert response.status_code == 200

    data = response.json()

    assert "version" in data
    assert data["version"] == "0.11.4"

