
from backend.blackboard.board import Blackboard

from backend.tools.acknowledgement_tools import (
    format_expected_timeline,
    draft_acknowledgement
)


class AcknowledgementAgent:
    """
    Generates and stores citizen-facing acknowledgements.
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

        # Validate that previous agents completed their work
        if grievance.category is None:
            raise ValueError("Grievance has not been classified.")

        if not grievance.location:
            raise ValueError("Grievance location is missing.")

        if not grievance.department:
            raise ValueError("Department has not been assigned.")

        if not grievance.deadline_at:
            raise ValueError("SLA deadline has not been calculated.")

        # Tool 1: Format the deadline
        timeline = format_expected_timeline(
            grievance.deadline_at
        )

        # Tool 2: Draft acknowledgement
        message = draft_acknowledgement(
            reference_id=grievance.reference_id,
            category=grievance.category.value,
            location=grievance.location,
            department=grievance.department,
            expected_timeline=timeline
        )

        # Save acknowledgement on shared Blackboard
        self.blackboard.update_grievance(
            reference_id,
            action="Acknowledgement generated",
            details="Citizen acknowledgement drafted successfully",
            acknowledgement=message
        )

        return {
            "reference_id": reference_id,
            "expected_timeline": timeline,
            "acknowledgement": message
        }
