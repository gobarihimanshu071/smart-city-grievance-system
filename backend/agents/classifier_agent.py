
from backend.tools.classifier_tools import (
    normalize_complaint,
    classify_category,
    extract_location
)

from backend.blackboard.board import Blackboard
from backend.blackboard.models import GrievanceCategory


class ClassifierAgent:
    """
    Identifies grievance category and location.
    Reads from and writes to the shared Blackboard.
    """

    def __init__(self, blackboard: Blackboard):
        self.blackboard = blackboard

    def process(self, reference_id: str) -> dict:

        # Read grievance from shared Blackboard
        grievance = self.blackboard.get_grievance(reference_id)

        if grievance is None:
            raise ValueError(
                f"Grievance {reference_id} not found."
            )

        # Tool 1: Normalize complaint
        normalized_text = normalize_complaint(
            grievance.complaint_text
        )

        # Tool 2: Classify complaint
        category = classify_category(normalized_text)

        # Tool 3: Extract location
        location = extract_location(
            grievance.complaint_text
        )

        # Convert category into our enum
        category_value = (
            GrievanceCategory(category)
            if category != "unknown"
            else None
        )

        # Write results to shared Blackboard
        self.blackboard.update_grievance(
            reference_id,
            action="Grievance classified",
            details=f"Category: {category}, Location: {location}",
            category=category_value,
            location=location
        )

        return {
            "reference_id": reference_id,
            "category": category,
            "location": location
        }
