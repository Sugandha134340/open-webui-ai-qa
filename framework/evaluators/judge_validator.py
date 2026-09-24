import json
from pathlib import Path
from datetime import datetime, timezone
from framework.evaluators.semantic_evaluator import (
    SemanticEvaluator,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "judge_validation.json"
)


class JudgeValidator:
    """
    Validates the LLM-as-a-judge evaluator against
    human-labelled examples.
    """

    def __init__(self):
        self.evaluator = SemanticEvaluator()

    def load_cases(self):
        with DATASET_PATH.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def validate(self):
        cases = self.load_cases()

        results = []

        for case in cases:

            result = self.evaluator.evaluate(
                requirements=[
                    case["requirement"]
                ],
                actual_response=case["response"],
            )

            judge_label = result["passed"]
            human_label = case["human_label"]

            results.append({
                "case_id": case["case_id"],
                "requirement": case["requirement"],
                "human_label": human_label,
                "judge_label": judge_label,
                "agreement": (
                    judge_label == human_label
                ),
                "score": result["score"],
                "reason": result["reason"],
            })

        total = len(results)

        agreement_count = sum(
            1
            for result in results
            if result["agreement"]
        )

        false_positives = sum(
            1
            for result in results
            if (
                result["judge_label"] is True
                and result["human_label"] is False
            )
        )

        false_negatives = sum(
            1
            for result in results
            if (
                result["judge_label"] is False
                and result["human_label"] is True
            )
        )

        agreement_rate = (
            agreement_count / total
            if total
            else 0.0
        )

        return {
            "total_cases": total,
            "agreement_count": agreement_count,
            "agreement_rate": round(
                agreement_rate,
                4,
            ),
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "results": results,
        }

    def save_report(
        self,
        report,
        filename="judge_validation_report.json",
    ):
        """
        Save the LLM-as-judge validation results as JSON.
        """

        reports_dir = PROJECT_ROOT / "reports"

        reports_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_with_metadata = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "judge_model": self.evaluator.model,
            "validation_type": "human_label_agreement",
            **report,
        }

        report_path = reports_dir / filename

        with report_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                report_with_metadata,
                file,
                indent=2,
                ensure_ascii=False,
            )

        return report_path


