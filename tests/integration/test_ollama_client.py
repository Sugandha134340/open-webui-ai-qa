import pytest

from framework.clients.ollama_client import (
    OllamaClient,
)


def test_ollama_client_configuration():
    client = OllamaClient()

    assert client.base_url == (
        "http://localhost:11434"
    )

    assert client.model == "llama3.2:3b"
    assert client.timeout == 120


@pytest.mark.integration
def test_ollama_health_check():
    client = OllamaClient()

    data = client.health_check()

    assert "models" in data


@pytest.mark.integration
def test_ollama_model_is_available():
    client = OllamaClient()

    assert client.is_model_available() is True


@pytest.mark.integration
def test_ollama_generate():
    client = OllamaClient()

    result = client.generate(
        "Reply with exactly QA_OLLAMA_OK",
        temperature=0.0,
    )

    assert "response" in result
    assert result["response"].strip() != ""

    assert result["model"] == "llama3.2:3b"

    assert result["latency_seconds"] > 0
