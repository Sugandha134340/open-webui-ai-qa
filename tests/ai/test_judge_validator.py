
from framework.evaluators.judge_validator import (
    JudgeValidator,
)


def test_validation_dataset_loads():
    validator = JudgeValidator()

    cases = validator.load_cases()

    assert len(cases) == 12

    for case in cases:
        assert "case_id" in case
        assert "requirement" in case
        assert "response" in case
        assert "human_label" in case


def test_judge_validation_metrics_structure():
    validator = JudgeValidator()

    # Test the metric calculation independently by
    # temporarily replacing the evaluator.
    class FakeEvaluator:

        def evaluate(
            self,
            requirements,
            actual_response,
        ):
            return {
                "passed": actual_response == "PASS",
                "score": 1.0
                if actual_response == "PASS"
                else 0.0,
                "reason": "Test evaluator",
            }

    validator.evaluator = FakeEvaluator()

    # Replace loaded cases with deterministic cases.
    validator.load_cases = lambda: [
        {
            "case_id": "TEST001",
            "requirement": "Test requirement",
            "response": "PASS",
            "human_label": True,
        },
        {
            "case_id": "TEST002",
            "requirement": "Test requirement",
            "response": "FAIL",
            "human_label": False,
        },
        {
            "case_id": "TEST003",
            "requirement": "Test requirement",
            "response": "PASS",
            "human_label": False,
        },
        {
            "case_id": "TEST004",
            "requirement": "Test requirement",
            "response": "FAIL",
            "human_label": True,
        },
    ]

    report = validator.validate()

    assert report["total_cases"] == 4
    assert report["agreement_count"] == 2
    assert report["agreement_rate"] == 0.5
    assert report["false_positives"] == 1
    assert report["false_negatives"] == 1


import pytest

from framework.evaluators.judge_validator import (
    JudgeValidator,
)


@pytest.mark.integration
def test_real_llm_judge_validation():
    validator = JudgeValidator()

    report = validator.validate()

    report_path = validator.save_report(report)

    print(
        f"\nValidation report saved to: "
        f"{report_path}"
    )

    assert report_path.exists()
    print("\n=== LLM JUDGE VALIDATION ===")
    print(f"Total cases: {report['total_cases']}")
    print(
        f"Agreement: "
        f"{report['agreement_count']}/"
        f"{report['total_cases']}"
    )
    print(
        f"Agreement rate: "
        f"{report['agreement_rate']}"
    )
    print(
        f"False positives: "
        f"{report['false_positives']}"
    )
    print(
        f"False negatives: "
        f"{report['false_negatives']}"
    )

    print("\n=== CASE RESULTS ===")

    for result in report["results"]:
        print(
            f"{result['case_id']} | "
            f"Human={result['human_label']} | "
            f"Judge={result['judge_label']} | "
            f"Agreement={result['agreement']}"
        )

    assert report["total_cases"] == 12
    assert 0.0 <= report["agreement_rate"] <= 1.0
