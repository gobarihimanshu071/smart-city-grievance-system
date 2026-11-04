
from backend.blackboard.board import Blackboard
from backend.blackboard.models import GrievanceStatus

from backend.tools.escalation_tools import (
    find_breached_grievances,
    select_next_authority,
    create_escalation_summary
)


class EscalationAgent:
    """
    Handles SLA-breached grievances and escalates them
    to the next authority.
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

        # Tool 1: Find breached grievances
        breached = find_breached_grievances(
            self.blackboard
        )

        breached_ids = {
            item.reference_id for item in breached
        }

        if reference_id not in breached_ids:
            raise ValueError(
                "This grievance has not breached its SLA."
            )

        # Determine next escalation authority
        next_level, authority = select_next_authority(
            grievance.escalation_level
        )

        # Tool 2: Generate escalation report
        summary = create_escalation_summary(
            grievance,
            authority
        )

        # Update shared Blackboard
        self.blackboard.update_grievance(
            reference_id,
            action="Grievance escalated",
            details=(
                f"Escalation Level: {next_level}; "
                f"Escalated To: {authority}"
            ),
            escalation_level=next_level,
            status=GrievanceStatus.ESCALATED
        )

        return {
            "reference_id": reference_id,
            "escalation_level": next_level,
            "authority": authority,
            "summary": summary,
            "status": "escalated"
        }
