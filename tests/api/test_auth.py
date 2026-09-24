from framework.clients.openwebui_client import OpenWebUIClient

def test_chats_requires_authentication():
    client = OpenWebUIClient()


    response = client.get("/api/v1/chats/")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"


def test_pinned_chats_requires_authentication():
    client = OpenWebUIClient()


    response = client.get("/api/v1/chats/pinned")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"

