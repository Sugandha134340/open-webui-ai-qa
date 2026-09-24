from framework.evaluators.dataset_loader import (
    load_ai_scenarios,
    load_golden_dataset,
    get_scenario_by_id,
)


# ============================================================
# AI scenario dataset
# ============================================================

def test_ai_scenarios_load_successfully():
    scenarios = load_ai_scenarios()

    assert isinstance(scenarios, list)
    assert len(scenarios) == 35


def test_ai_scenarios_have_required_fields():
    scenarios = load_ai_scenarios()

    required_fields = {
        "scenario_id",
        "category",
        "input",
        "context",
        "expected_behavior",
        "expected_tool",
        "constraints",
        "safety_requirement",
        "evaluation_method",
        "severity",
    }

    for scenario in scenarios:
        missing_fields = (
            required_fields
            - scenario.keys()
        )

        assert not missing_fields, (
            f"Scenario "
            f"{scenario.get('scenario_id')} "
            f"is missing fields: "
            f"{missing_fields}"
        )


def test_ai_scenario_ids_are_unique():
    scenarios = load_ai_scenarios()

    scenario_ids = [
        scenario["scenario_id"]
        for scenario in scenarios
    ]

    assert len(scenario_ids) == len(set(scenario_ids))


def test_ai_scenario_lookup():
    scenarios = load_ai_scenarios()

    scenario = get_scenario_by_id(
        scenarios,
        "AI001",
    )

    assert scenario["scenario_id"] == "AI001"


# ============================================================
# Golden dataset
# ============================================================

def test_golden_dataset_loads_successfully():
    golden = load_golden_dataset()

    assert isinstance(golden, list)
    assert len(golden) == 10


def test_golden_dataset_ids_are_unique():
    golden = load_golden_dataset()

    scenario_ids = [
        case["scenario_id"]
        for case in golden
    ]

    assert len(scenario_ids) == len(
        set(scenario_ids)
    )


def test_golden_cases_reference_valid_scenarios():
    scenarios = load_ai_scenarios()
    golden = load_golden_dataset()

    scenario_ids = {
        scenario["scenario_id"]
        for scenario in scenarios
    }

    for case in golden:
        assert case["scenario_id"] in scenario_ids


def test_golden_dataset_has_evaluation_definition():
    golden = load_golden_dataset()

    for case in golden:
        assert (
            "expected_answer" in case
            or "expected_answer_requirements" in case
        )
