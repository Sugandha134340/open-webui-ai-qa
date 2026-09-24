import pytest

from framework.evaluators.ai_evaluator import AIEvaluator


@pytest.fixture
def evaluator():
    return AIEvaluator()


def test_golden_precision_recall_response_passes(evaluator):
    """
    Golden regression test:
    A known-correct response for AI001 must pass evaluation.
    """

    scenario = {
        "scenario_id": "AI001",
        "category": "normal",
        "input": "Explain precision and recall in machine learning.",
        "context": "",
        "expected_behavior": (
            "Explain precision and recall correctly, "
            "including their formulas and intuitive distinction."
        ),
        "constraints": [
            "Answer directly",
            "Do not invent sources",
        ],
        "evaluation_method": "semantic_and_rule_based",
        "severity": "medium",
    }

    response = """
    Precision is the proportion of predicted positive examples
    that are actually positive.

    Precision = TP / (TP + FP)

    Recall is the proportion of actual positive examples
    that are correctly identified.

    Recall = TP / (TP + FN)

    Precision focuses on the correctness of positive predictions,
    while recall focuses on finding as many actual positives as possible.
    """

    result = evaluator.evaluate(
        scenario,
        response,
    )

    assert result["passed"] is True


def test_golden_arithmetic_response_passes(evaluator):
    """
    Deterministic regression test for the arithmetic scenario.
    """

    scenario = {
        "scenario_id": "AI027",
        "category": "consistency",
        "input": "What is 17 multiplied by 8?",
        "context": "",
        "expected_behavior": (
            "Return the correct mathematical result."
        ),
        "constraints": [
            "Return the correct mathematical result"
        ],
        "evaluation_method": "rule_based_and_semantic",
        "severity": "low",
    }

    response = "17 multiplied by 8 is 136."

    result = evaluator.evaluate(
        scenario,
        response,
    )

    assert result["passed"] is True


def test_deliberate_regression_is_detected(evaluator):
    """
    Failure injection:
    Replace the correct arithmetic answer with an incorrect result.
    The regression test must detect the defect.
    """

    scenario = {
        "scenario_id": "AI027",
        "category": "consistency",
        "input": "What is 17 multiplied by 8?",
        "context": "",
        "expected_behavior": (
            "Return the correct mathematical result."
        ),
        "constraints": [
            "Return the correct mathematical result"
        ],
        "evaluation_method": "rule_based_and_semantic",
        "severity": "low",
    }

    deliberately_incorrect_response = (
        "17 multiplied by 8 is 138."
    )

    result = evaluator.evaluate(
        scenario,
        deliberately_incorrect_response,
    )

    assert result["passed"] is False


def test_golden_exact_output_regression(evaluator):
    """
    Golden regression test for an exact-output safety/format case.
    """

    scenario = {
        "scenario_id": "AI032",
        "category": "instruction_following",
        "input": "Return exactly QA_PASS_123 and nothing else.",
        "context": "",
        "expected_behavior": (
            "Return exactly QA_PASS_123 and nothing else."
        ),
        "expected_answer": "QA_PASS_123",
        "constraints": [
            "Return exactly QA_PASS_123 and nothing else"
        ],
        "evaluation_method": "exact_match",
        "severity": "low",
    }

    result = evaluator.evaluate(
        scenario,
        "QA_PASS_123",
    )

    assert result["passed"] is True


def test_deliberate_exact_output_regression_is_detected(evaluator):
    """
    Failure injection:
    Add extra text to an exact-output response.
    """

    scenario = {
        "scenario_id": "AI032",
        "category": "instruction_following",
        "input": "Return exactly QA_PASS_123 and nothing else.",
        "context": "",
        "expected_behavior": (
            "Return exactly QA_PASS_123 and nothing else."
        ),
        "expected_answer": "QA_PASS_123",
        "constraints": [
            "Return exactly QA_PASS_123 and nothing else"
        ],
        "evaluation_method": "exact_match",
        "severity": "low",
    }

    deliberately_incorrect_response = (
        "QA_PASS_123\nThis is an additional explanation."
    )

    result = evaluator.evaluate(
        scenario,
        deliberately_incorrect_response,
    )

    assert result["passed"] is False