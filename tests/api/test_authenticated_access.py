import os

from dotenv import load_dotenv

from framework.clients.openwebui_client import OpenWebUIClient


load_dotenv()


def test_authenticated_user_can_access_chats():
    email = os.environ["OPENWEBUI_QA_EMAIL"]
    password = os.environ["OPENWEBUI_QA_PASSWORD"]

    client = OpenWebUIClient()

    login_response = client.signin(email, password)

    print("\n=== LOGIN RESPONSE ===")
    print("Status:", login_response.status_code)
    print("Body:", login_response.text)
    print("Cookies:", login_response.cookies.get_dict())

    assert login_response.status_code == 200