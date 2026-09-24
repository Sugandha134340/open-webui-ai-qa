from framework.evaluators.semantic_evaluator import (
    SemanticEvaluator,
)


def test_semantic_evaluator_initializes():
    evaluator = SemanticEvaluator()

    assert evaluator.model == "llama3.2:3b"
    assert evaluator.ollama_url == "http://localhost:11434"


def test_semantic_evaluator_parses_valid_result():
    evaluator = SemanticEvaluator()

    raw_output = """
    {
        "criteria": [
            {
                "requirement": "Defines precision correctly",
                "passed": true,
                "reason": "The response gives the correct definition."
            },
            {
                "requirement": "Defines recall correctly",
                "passed": true,
                "reason": "The response gives the correct definition."
            },
            {
                "requirement": "Distinguishes precision from recall",
                "passed": true,
                "reason": "The response clearly distinguishes them."
            },
            {
                "requirement": "Does not introduce factual errors",
                "passed": true,
                "reason": "No factual errors were identified."
            }
        ],
        "score": 1.0,
        "passed": true,
        "reason": "All requirements are satisfied."
    }
    """

    result = evaluator._parse_result(raw_output)

    assert result["passed"] is True
    assert result["score"] == 1.0
    assert len(result["criteria"]) == 4


def test_semantic_evaluator_recalculates_score():
    evaluator = SemanticEvaluator()

    raw_output = """
    {
        "criteria": [
            {
                "requirement": "Requirement 1",
                "passed": true,
                "reason": "Satisfied."
            },
            {
                "requirement": "Requirement 2",
                "passed": false,
                "reason": "Not satisfied."
            },
            {
                "requirement": "Requirement 3",
                "passed": true,
                "reason": "Satisfied."
            },
            {
                "requirement": "Requirement 4",
                "passed": false,
                "reason": "Not satisfied."
            }
        ],
        "score": 1.0,
        "passed": true,
        "reason": "Example."
    }
    """

    result = evaluator._parse_result(raw_output)

    # 2 / 4 = 0.5
    assert result["score"] == 0.5
    assert result["passed"] is False


def test_semantic_evaluator_extracts_markdown_wrapped_json():
    evaluator = SemanticEvaluator()

    raw_output = """
    ```json
    {
        "criteria": [
            {
                "requirement": "Requirement 1",
                "passed": true,
                "reason": "Satisfied."
            }
        ],
        "score": 1.0,
        "passed": true,
        "reason": "Satisfied."
    }
    ```
    """

    result = evaluator._parse_result(raw_output)

    assert result["passed"] is True
    assert result["score"] == 1.0


import pytest

from framework.evaluators.semantic_evaluator import (
    SemanticEvaluator,
)


@pytest.mark.integration
def test_semantic_evaluator_with_real_ollama():
    evaluator = SemanticEvaluator(
        model="llama3.2:3b",
        timeout=120,
    )

    requirements = [
        "Defines precision correctly",
        "Defines recall correctly",
        "Distinguishes precision from recall",
        "Does not introduce factual errors",
    ]

    actual_response = (
        "Precision is the proportion of predicted positive "
        "cases that are actually positive. Recall is the "
        "proportion of actual positive cases that are "
        "correctly identified. Precision focuses on the "
        "correctness of positive predictions, while recall "
        "focuses on finding the actual positive cases."
    )

    result = evaluator.evaluate(
        requirements=requirements,
        actual_response=actual_response,
        context="General machine learning question.",
        expected_behavior=(
            "Give a concise and factually correct explanation "
            "of precision and recall and distinguish the two."
        ),
    )

    print("\n=== SEMANTIC JUDGE RESULT ===")
    print(result)

    assert "criteria" in result
    assert "score" in result
    assert "passed" in result

    assert len(result["criteria"]) == 4
    assert 0.0 <= result["score"] <= 1.0
