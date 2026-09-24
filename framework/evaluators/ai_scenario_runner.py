import json
import time
from datetime import datetime, timezone
from pathlib import Path

from framework.clients.ollama_client import OllamaClient
from framework.evaluators.ai_evaluator import AIEvaluator
from framework.evaluators.dataset_loader import (
    load_ai_scenarios,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORTS_DIR = PROJECT_ROOT / "reports"


class AIScenarioRunner:
    """
    Executes AI evaluation scenarios against a real model
    and evaluates the generated responses.

    Pipeline:

        Scenario
            ↓
        Ollama
            ↓
        AI response
            ↓
        AIEvaluator
            ↓
        Evaluation result
            ↓
        Structured report
    """

    def __init__(
        self,
        model="llama3.2:3b",
        temperature=0.0,
        timeout=120,
    ):
        self.model = model
        self.temperature = temperature

        self.client = OllamaClient(
            model=model,
            timeout=timeout,
        )

        self.evaluator = AIEvaluator()

    def build_prompt(self, scenario):
        """
        Build a model prompt from a structured scenario.
        """

        context = scenario.get(
            "context",
            "",
        )

        user_input = scenario.get(
            "input",
            "",
        )

        constraints = scenario.get(
            "constraints",
            [],
        )

        constraints_text = "\n".join(
            f"- {constraint}"
            for constraint in constraints
        )

        return f"""
Context:
{context}

User request:
{user_input}

Constraints:
{constraints_text}

Answer the user's request directly.
Follow the provided constraints.
Do not invent information or sources.
""".strip()

    def run_scenario(self, scenario):
        """
        Execute and evaluate one scenario.
        """

        scenario_id = scenario["scenario_id"]

        prompt = self.build_prompt(
            scenario
        )

        started_at = datetime.now(
            timezone.utc
        ).isoformat()

        execution_start = time.perf_counter()

        try:
            model_result = self.client.generate(
                prompt=prompt,
                temperature=self.temperature,
            )

            execution_time = (
                time.perf_counter()
                - execution_start
            )

            actual_response = model_result[
                "response"
            ]

            evaluation = self.evaluator.evaluate(
                scenario,
                actual_response,
            )

            return {
                "scenario_id": scenario_id,
                "category": scenario.get(
                    "category"
                ),
                "severity": scenario.get(
                    "severity"
                ),
                "started_at": started_at,
                "model": self.model,
                "temperature": self.temperature,
                "prompt": prompt,
                "response": actual_response,
                "latency_seconds": model_result[
                    "latency_seconds"
                ],
                "execution_time_seconds": round(
                    execution_time,
                    4,
                ),
                "ollama": {
                    "total_duration_ns": model_result.get(
                        "total_duration_ns"
                    ),
                    "load_duration_ns": model_result.get(
                        "load_duration_ns"
                    ),
                    "prompt_eval_count": model_result.get(
                        "prompt_eval_count"
                    ),
                    "eval_count": model_result.get(
                        "eval_count"
                    ),
                },
                "evaluation": evaluation,
                "status": (
                    "PASS"
                    if evaluation["passed"]
                    else "FAIL"
                ),
            }

        except Exception as exc:

            execution_time = (
                time.perf_counter()
                - execution_start
            )

            return {
                "scenario_id": scenario_id,
                "category": scenario.get(
                    "category"
                ),
                "severity": scenario.get(
                    "severity"
                ),
                "started_at": started_at,
                "model": self.model,
                "temperature": self.temperature,
                "status": "ERROR",
                "error": str(exc),
                "execution_time_seconds": round(
                    execution_time,
                    4,
                ),
            }

    def run_all(self):
        """
        Execute all scenarios in ai_scenarios.json.
        """

        scenarios = load_ai_scenarios()

        results = []

        for index, scenario in enumerate(
            scenarios,
            start=1,
        ):
            print(
                f"[{index}/{len(scenarios)}] "
                f"Running {scenario['scenario_id']}..."
            )

            result = self.run_scenario(
                scenario
            )

            results.append(result)

        return self.build_report(
            results
        )

    def build_report(self, results):
        """
        Build aggregate metrics.
        """

        total = len(results)

        passed = sum(
            1
            for result in results
            if result["status"] == "PASS"
        )

        failed = sum(
            1
            for result in results
            if result["status"] == "FAIL"
        )

        errors = sum(
            1
            for result in results
            if result["status"] == "ERROR"
        )

        latencies = [
            result["latency_seconds"]
            for result in results
            if "latency_seconds" in result
        ]

        average_latency = (
            sum(latencies) / len(latencies)
            if latencies
            else 0.0
        )

        return {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "model": self.model,

            "temperature": self.temperature,

            "summary": {
                "total_scenarios": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "evaluated": (
                    passed + failed
                ),
                "pass_rate": (
                    passed / (passed + failed)
                    if (passed + failed)
                    else 0.0
                ),
                "average_latency_seconds": round(
                    average_latency,
                    4,
                ),
            },

            "results": results,
        }

    def save_report(
        self,
        report,
        filename="ai_scenario_results.json",
    ):
        """
        Save the complete scenario evaluation report.
        """

        REPORTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path = (
            REPORTS_DIR / filename
        )

        with report_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                report,
                file,
                indent=2,
                ensure_ascii=False,
            )

        return report_path
