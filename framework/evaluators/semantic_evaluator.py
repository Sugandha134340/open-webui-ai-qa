import json
import re

import requests


class SemanticEvaluator:
    """
    LLM-as-a-judge evaluator using the local Ollama model.

    The judge evaluates an AI response against explicit
    requirements and returns a structured evaluation.
    """

    def __init__(
        self,
        ollama_url="http://localhost:11434",
        model="llama3.2:3b",
        timeout=60,
    ):
        self.ollama_url = ollama_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def evaluate(
        self,
        requirements,
        actual_response,
        context="",
        expected_behavior="",
    ):
        """
        Evaluate an AI response against semantic requirements.

        Returns:
            {
                "passed": bool,
                "score": float,
                "criteria": [...],
                "reason": str
            }
        """

        prompt = self._build_prompt(
            requirements=requirements,
            actual_response=actual_response,
            context=context,
            expected_behavior=expected_behavior,
        )

        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        raw_output = data.get("response", "")

        result = self._parse_result(raw_output)

        return result

    def _build_prompt(
        self,
        requirements,
        actual_response,
        context,
        expected_behavior,
    ):
        requirements_text = "\n".join(
            f"{index}. {requirement}"
            for index, requirement in enumerate(
                requirements,
                start=1,
            )
        )

        return f"""
You are an AI quality evaluator.

Your task is to evaluate an AI-generated response
against explicit quality requirements.

Do NOT judge whether you personally like the answer.
Judge only whether the response satisfies the stated
requirements.

Evaluation context:
{context}

Expected behavior:
{expected_behavior}

Requirements:
{requirements_text}

Actual AI response:
{actual_response}

For every requirement, determine whether it is satisfied.

Return ONLY valid JSON using exactly this structure:

{{
  "criteria": [
    {{
      "requirement": "original requirement text",
      "passed": true,
      "reason": "short factual explanation"
    }}
  ],
  "score": 0.0,
  "passed": false,
  "reason": "overall explanation"
}}

Scoring rules:

- score = number of passed requirements / total requirements
- passed = true only when score >= 0.8
- Do not invent facts that are not present in the response.
- Do not reward an answer merely because it sounds plausible.
- Be strict about factual correctness.
""".strip()

    def _parse_result(self, raw_output):
        """
        Parse and validate the JSON returned by Ollama.
        """

        try:
            result = json.loads(raw_output)
        except json.JSONDecodeError:
            # Some models may occasionally wrap JSON in
            # Markdown despite being asked for JSON.
            result = self._extract_json(raw_output)

        if not isinstance(result, dict):
            raise ValueError(
                "Semantic judge returned a non-object JSON result."
            )

        criteria = result.get("criteria", [])

        if not isinstance(criteria, list):
            raise ValueError(
                "Semantic judge returned invalid criteria."
            )

        if not criteria:
            raise ValueError(
                "Semantic judge returned no criteria."
            )

        # Recalculate the score ourselves rather than
        # trusting the judge's arithmetic.
        passed_count = sum(
            1
            for criterion in criteria
            if criterion.get("passed") is True
        )

        score = passed_count / len(criteria)

        return {
            "passed": score >= 0.8,
            "score": round(score, 4),
            "criteria": criteria,
            "reason": result.get(
                "reason",
                "Semantic evaluation completed.",
            ),
        }

    @staticmethod
    def _extract_json(text):
        """
        Extract the first JSON object from model output.
        """

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL,
        )

        if not match:
            raise ValueError(
                "Could not find JSON in semantic judge response."
            )

        return json.loads(match.group(0))
