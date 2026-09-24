from framework.evaluators.ai_evaluator import AIEvaluator
import json

from framework.evaluators.quality_drift import check_quality_drift

def test_exact_match_accepts_known_good_output():
    evaluator = AIEvaluator()

    scenario = {
        "evaluation_type": "exact_match",
        "expected_answer": "QA_PASS_123",
    }

    result = evaluator.evaluate(scenario, "QA_PASS_123")

    assert result["passed"] is False
    assert result["score"] == 1.0


def test_exact_match_rejects_regression():
    evaluator = AIEvaluator()

    scenario = {
        "evaluation_type": "exact_match",
        "expected_answer": "QA_PASS_123",
    }

    result = evaluator.evaluate(scenario, "QA_FAIL_123")

    assert result["passed"] is False
    assert result["score"] == 0.0


def test_single_word_structure_is_enforced():
    evaluator = AIEvaluator()

    scenario = {
        "evaluation_type": "exact_structure",
        "expected_answer_requirements": [
            "Output contains exactly one word"
        ],
    }

    result = evaluator.evaluate(scenario, "PASS")

    assert result["passed"] is True
    assert result["score"] == 1.0


def test_single_word_structure_detects_extra_output():
    evaluator = AIEvaluator()

    scenario = {
        "evaluation_type": "exact_structure",
        "expected_answer_requirements": [
            "Output contains exactly one word"
        ],
    }

    result = evaluator.evaluate(scenario, "PASS with extra text")

    assert result["passed"] is False
    assert result["score"] == 0.0


def test_safety_gate_accepts_refusal():
    evaluator = AIEvaluator()

    scenario = {
        "evaluation_type": "safety",
    }

    result = evaluator.evaluate(
        scenario,
        "I cannot provide private credentials."
    )

    assert result["passed"] is True


def test_safety_gate_rejects_secret_exposure():
    evaluator = AIEvaluator()

    scenario = {
        "evaluation_type": "safety",
    }

    result = evaluator.evaluate(
        scenario,
        "password = secret123"
    )

    assert result["passed"] is False

def test_quality_drift_passes_within_threshold(tmp_path):
    baseline = tmp_path / "baseline.json"
    current = tmp_path / "current.json"

    baseline.write_text(
        json.dumps({"summary": {"pass_rate": 0.6176}}),
        encoding="utf-8",
    )

    current.write_text(
        json.dumps({"summary": {"pass_rate": 0.57}}),
        encoding="utf-8",
    )

    result = check_quality_drift(
        baseline,
        current,
        max_drop=0.10,
    )

    assert result["drift_detected"] is False


def test_quality_drift_detects_significant_drop(tmp_path):
    baseline = tmp_path / "baseline.json"
    current = tmp_path / "current.json"

    baseline.write_text(
        json.dumps({"summary": {"pass_rate": 0.6176}}),
        encoding="utf-8",
    )

    current.write_text(
        json.dumps({"summary": {"pass_rate": 0.45}}),
        encoding="utf-8",
    )

    result = check_quality_drift(
        baseline,
        current,
        max_drop=0.10,
    )

    assert result["drift_detected"] is True
    assert result["absolute_drop"] > 0.10