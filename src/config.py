"""Configuration loader for TRiP-Light.

This module loads configuration from config.yaml and provides the same interface
as the previous variables.py module. It reads Excel cell mappings and file paths
from the YAML configuration file.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml


def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml file.

    Returns:
        Dictionary containing all configuration values.

    Raises:
        FileNotFoundError: If config.yaml is not found.
        yaml.YAMLError: If config.yaml is malformed.
    """
    # Look for config.yaml in the project root (parent of src/)
    config_path = Path(__file__).parent.parent / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found at {config_path}. "
            "Please ensure config.yaml exists in the project root."
        )

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


# Load configuration at module import
_config = load_config()

# Constants for file processing (matching variables.py interface)
numTrips: int = _config["numTrips"]
prefsSheetIndex: int = _config["prefsSheetIndex"]
tripLeaderInfoIndex: int = _config["tripLeaderInfoIndex"]
folderPath: str = _config["folderPath"]

# Trip information cell mappings
tripInfoDict: Dict[str, Union[str, int]] = {
    "datesCell": _config["tripInfo"]["datesCell"],
    "tripCell": _config["tripInfo"]["tripCell"],
    "tripCategoryCell": _config["tripInfo"]["tripCategoryCell"],
    "tripStatusFileName": _config["tripInfo"]["tripStatusFileName"],
    "numTrips": numTrips,
}

# Trip leader information cell mappings
leaderInfoDict: Dict[str, Union[str, int, List[str]]] = {
    "leaderTripCell": _config["leaderInfo"]["leaderTripCell"],
    "leaderPrefsCell": _config["leaderInfo"]["leaderPrefsCell"],
    "nameCell": _config["leaderInfo"]["nameCell"],
    # Numerical Questions
    "semestersLeftCell": _config["leaderInfo"]["semestersLeftCell"],
    "tripSatisfactionCell": _config["leaderInfo"]["tripSatisfactionCell"],
    "tripsAssignedCell": _config["leaderInfo"]["tripsAssignedCell"],
    "tripDropCell": _config["leaderInfo"]["tripDropCell"],
    "tripPickupCell": _config["leaderInfo"]["tripPickupCell"],
    "tripCancelledCell": _config["leaderInfo"]["tripCancelledCell"],
    # Short Answer Questions
    "tripInvolvementCell": _config["leaderInfo"]["tripInvolvementCell"],
    "mainGoalCell": _config["leaderInfo"]["mainGoalCell"],
    "interestedCategoriesCell": _config["leaderInfo"]["interestedCategoriesCell"],
    "threeLeadersCell": _config["leaderInfo"]["threeLeadersCell"],
    "additionalNotesCell": _config["leaderInfo"]["additionalNotesCell"],
    "numTrips": numTrips,
    "nameCellGuideStatus": _config["leaderInfo"]["nameCellGuideStatus"],
    "firstPromotionalCategoryCell": _config["leaderInfo"][
        "firstPromotionalCategoryCell"
    ],
    "leaderGuideStatusFileName": _config["leaderInfo"]["leaderGuideStatusFileName"],
}
