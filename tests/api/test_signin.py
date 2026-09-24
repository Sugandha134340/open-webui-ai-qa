from framework.clients.openwebui_client import OpenWebUIClient


def test_signin_rejects_invalid_credentials():
    client = OpenWebUIClient()

    response = client.signin(
        "qa-invalid@example.com",
        "invalid-password",
    )

    assert response.status_code in (400, 401)

    data = response.json()

    assert "detail" in data