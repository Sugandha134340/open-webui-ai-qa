import requests


class OpenWebUIClient:
    """Reusable HTTP client for Open WebUI."""

    def __init__(self, base_url="http://localhost:3000", timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, path, **kwargs):
        return self.session.get(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    def post(self, path, **kwargs):
        return self.session.post(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    def get_version(self):
        return self.get("/api/version")

    def signin(self, email, password):
        response = self.post(
            "/api/v1/auths/signin",
            json={
                "email": email,
                "password": password,
            },
        )

        if response.ok:
            data = response.json()

            # Preserve authentication token if the API returns one.
            token = data.get("token")
            if token:
                self.session.headers.update(
                    {"Authorization": f"Bearer {token}"}
                )

        return response

    def chat_completion(
        self,
        message,
        model="llama3.2:3b",
        stream=False,
    ):
        return self.post(
            "/api/chat/completions",
            json={
                "stream": stream,
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
            },
        )