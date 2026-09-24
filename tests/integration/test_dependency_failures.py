import requests

from framework.clients.ollama_client import OllamaClient


class FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self.payload = payload or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(
                f"HTTP {self.status_code}"
            )

    def json(self):
        return self.payload


def test_dependency_http_500_is_detected(monkeypatch):
    client = OllamaClient()

    def fake_post(*args, **kwargs):
        return FakeResponse(500)

    monkeypatch.setattr(requests, "post", fake_post)

    try:
        client.generate("dependency failure test")
        assert False, "Expected HTTP 500 dependency failure"
    except requests.HTTPError as exc:
        assert "500" in str(exc)


def test_dependency_timeout_is_detected(monkeypatch):
    client = OllamaClient()

    def fake_post(*args, **kwargs):
        raise requests.Timeout("simulated dependency timeout")

    monkeypatch.setattr(requests, "post", fake_post)

    try:
        client.generate("dependency timeout test")
        assert False, "Expected dependency timeout"
    except requests.Timeout as exc:
        assert "timeout" in str(exc).lower()