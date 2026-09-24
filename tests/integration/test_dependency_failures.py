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


def test_dependency_malformed_response_is_detected(monkeypatch):
    client = OllamaClient()

    class MalformedResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("malformed JSON response")

    def fake_post(*args, **kwargs):
        return MalformedResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    try:
        client.generate("malformed response test")
        assert False, "Expected malformed dependency response failure"
    except ValueError as exc:
        assert "malformed" in str(exc).lower()


def test_dependency_empty_response_is_handled(monkeypatch):
    client = OllamaClient()

    class EmptyResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {}

    def fake_post(*args, **kwargs):
        return EmptyResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    result = client.generate("empty response test")

    assert isinstance(result, dict)
    assert result["response"] == ""


def test_dependency_unavailable_is_detected(monkeypatch):
    client = OllamaClient()

    def fake_post(*args, **kwargs):
        raise requests.ConnectionError(
            "simulated dependency unavailable"
        )

    monkeypatch.setattr(requests, "post", fake_post)

    try:
        client.generate("dependency unavailable test")
        assert False, "Expected dependency unavailable failure"
    except requests.ConnectionError as exc:
        assert "unavailable" in str(exc).lower()