import json
from datetime import datetime, timezone
from pathlib import Path

from framework.evaluators.ai_evaluator import AIEvaluator
from framework.evaluators.dataset_loader import (
    load_ai_scenarios,
    load_golden_dataset,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"


class EvaluationRunner:
    """
    Runs AI evaluation scenarios and produces a structured
    evaluation report.

    The runner is deliberately independent of the AI
    application. An AI response is supplied to the runner,
    allowing the same evaluation infrastructure to work with
    Open WebUI, Ollama, or a mocked response source.
    """

    def __init__(self):
        self.evaluator = AIEvaluator()

    def evaluate_response(self, scenario, actual_response):
        """
        Evaluate one AI response.
        """

        result = self.evaluator.evaluate(
            scenario,
            actual_response,
        )

        return {
            "scenario_id": scenario.get("scenario_id"),
            "category": scenario.get("category"),
            "severity": scenario.get("severity"),
            "evaluation_type": scenario.get(
                "evaluation_type"
            ),
            "actual_response": actual_response,
            "result": result,
        }

    def run(self, response_map):
        """
        Evaluate a mapping of scenario_id -> AI response.

        Example:

            {
                "AI001": "expected response",
                "AI002": "another response"
            }
        """

        scenarios = load_ai_scenarios()

        results = []

        for scenario in scenarios:

            scenario_id = scenario["scenario_id"]

            if scenario_id not in response_map:
                results.append({
                    "scenario_id": scenario_id,
                    "category": scenario.get("category"),
                    "severity": scenario.get("severity"),
                    "status": "NOT_RUN",
                    "reason": "No AI response provided",
                })
                continue

            actual_response = response_map[
                scenario_id
            ]

            evaluation = self.evaluate_response(
                scenario,
                actual_response,
            )

            results.append({
                **evaluation,
                "status": (
                    "PASS"
                    if evaluation["result"]["passed"]
                    else "FAIL"
                ),
            })

        return self._build_report(results)

    def _build_report(self, results):
        """
        Build aggregate evaluation statistics.
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

        not_run = sum(
            1
            for result in results
            if result["status"] == "NOT_RUN"
        )

        evaluated = passed + failed

        pass_rate = (
            passed / evaluated
            if evaluated
            else 0.0
        )

        return {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "summary": {
                "total_scenarios": total,
                "evaluated": evaluated,
                "passed": passed,
                "failed": failed,
                "not_run": not_run,
                "pass_rate": pass_rate,
            },

            "results": results,
        }

    def save_report(
        self,
        report,
        filename="ai_evaluation_results.json",
    ):
        """
        Save an evaluation report as JSON.
        """

        REPORTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path = REPORTS_DIR / filename

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

    def run_golden_regression(self, response_map):
        """
        Evaluate only the cases defined in golden_dataset.json.

        response_map:
            Dictionary mapping scenario_id -> actual AI response.
        """

        golden_cases = load_golden_dataset()

        results = []

        for case in golden_cases:
            scenario_id = case["scenario_id"]

            # Find the corresponding full scenario
            scenarios = load_ai_scenarios()

            scenario = next(
                (
                    item
                    for item in scenarios
                    if item["scenario_id"] == scenario_id
                ),
                None,
            )

            if scenario is None:
                results.append({
                    "scenario_id": scenario_id,
                    "status": "ERROR",
                    "reason": "Referenced scenario not found",
                })
                continue

            if scenario_id not in response_map:
                results.append({
                    "scenario_id": scenario_id,
                    "status": "NOT_RUN",
                    "reason": "No AI response provided",
                })
                continue

            actual_response = response_map[scenario_id]

            # Merge the golden-case evaluation definition
            # with the original scenario.
            evaluation_scenario = {
                **scenario,
                **case,
            }

            evaluation = self.evaluator.evaluate(
                evaluation_scenario,
                actual_response,
            )

            results.append({
                "scenario_id": scenario_id,
                "category": scenario.get("category"),
                "severity": scenario.get("severity"),
                "actual_response": actual_response,
                "expected_answer": case.get(
                    "expected_answer"
                ),
                "expected_answer_requirements": case.get(
                    "expected_answer_requirements"
                ),
                "status": (
                    "PASS"
                    if evaluation["passed"]
                    else "FAIL"
                ),
                "evaluation": evaluation,
            })

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

        not_run = sum(
            1
            for result in results
            if result["status"] == "NOT_RUN"
        )

        return {
            "type": "golden_regression",
            "total_cases": len(golden_cases),
            "passed": passed,
            "failed": failed,
            "not_run": not_run,
            "regression_detected": failed > 0,
            "results": results,
        }
