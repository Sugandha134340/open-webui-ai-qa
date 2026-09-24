import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = PROJECT_ROOT / "datasets"


def load_json(filename):
    """
    Load a JSON dataset from the project's datasets directory.
    """
    path = DATASET_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_ai_scenarios():
    """
    Load the complete AI evaluation scenario dataset.
    """
    return load_json("ai_scenarios.json")


def load_golden_dataset():
    """
    Load the golden regression dataset.
    """
    return load_json("golden_dataset.json")


def get_scenario_by_id(scenarios, scenario_id):
    """
    Retrieve a scenario using its scenario_id.
    """
    for scenario in scenarios:
        if scenario.get("scenario_id") == scenario_id:
            return scenario

    raise KeyError(
        f"Scenario not found: {scenario_id}"
    )
