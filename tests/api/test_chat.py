from framework.clients.openwebui_client import OpenWebUIClient


def test_chat_completion_requires_authentication():
    client = OpenWebUIClient()

    response = client.chat_completion(
        message="Reply with exactly QA_CHAT_OK",
        model="llama3.2:3b",
        stream=False,
    )

    print("\n=== CHAT RESPONSE ===")
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("content-type"))
    print("Body:", response.text)

    assert response.status_code == 401