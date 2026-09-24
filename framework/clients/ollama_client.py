import time

import requests


class OllamaClient:
    """
    Client for communicating with a local Ollama server.
    """

    def __init__(
        self,
        base_url="http://localhost:11434",
        model="llama3.2:3b",
        timeout=120,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate(
        self,
        prompt,
        system_prompt=None,
        temperature=0.0,
    ):
        """
        Generate a response from Ollama.

        Returns a structured dictionary containing:
        - response
        - latency
        - model
        - Ollama metadata
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        if system_prompt:
            payload["system"] = system_prompt

        start_time = time.perf_counter()

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=self.timeout,
        )

        latency = time.perf_counter() - start_time

        response.raise_for_status()

        data = response.json()

        return {
            "response": data.get("response", ""),
            "latency_seconds": round(
                latency,
                4,
            ),
            "model": data.get(
                "model",
                self.model,
            ),
            "total_duration_ns": data.get(
                "total_duration"
            ),
            "load_duration_ns": data.get(
                "load_duration"
            ),
            "prompt_eval_count": data.get(
                "prompt_eval_count"
            ),
            "eval_count": data.get(
                "eval_count"
            ),
        }

    def health_check(self):
        """
        Verify that Ollama is reachable.
        """

        response = requests.get(
            f"{self.base_url}/api/tags",
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    def is_model_available(self):
        """
        Check whether the configured model exists
        in the local Ollama installation.
        """

        data = self.health_check()

        models = data.get("models", [])

        return any(
            model.get("name") == self.model
            for model in models
        )
