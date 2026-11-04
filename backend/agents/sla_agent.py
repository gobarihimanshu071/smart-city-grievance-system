
from datetime import datetime

from backend.blackboard.board import Blackboard
from backend.blackboard.models import GrievanceStatus

from backend.tools.sla_tools import (
    calculate_deadline,
    evaluate_sla
)


class SLAAgent:
    """
    Calculates grievance deadlines and monitors SLA status.
    """

    def __init__(self, blackboard: Blackboard):
        self.blackboard = blackboard

    def process(
        self,
        reference_id: str,
        current_time: datetime | None = None
    ) -> dict:

        # Read grievance from shared Blackboard
        grievance = self.blackboard.get_grievance(reference_id)

        if grievance is None:
            raise ValueError(
                f"Grievance {reference_id} not found."
            )

        if grievance.category is None:
            raise ValueError(
                "Grievance must be classified before SLA processing."
            )

        # Do not breach an already resolved grievance
        if grievance.status == GrievanceStatus.RESOLVED:
            return {
                "reference_id": reference_id,
                "deadline": (
                    grievance.deadline_at.isoformat()
                    if grievance.deadline_at else None
                ),
                "sla_status": "resolved"
            }

        now = current_time or datetime.now()

        # Tool 1: Calculate deadline if not already assigned
        if grievance.deadline_at is None:
            deadline = calculate_deadline(
                grievance.created_at,
                grievance.category.value
            )
        else:
            deadline = grievance.deadline_at

        # Tool 2: Evaluate deadline
        sla_result = evaluate_sla(deadline, now)

        new_status = (
            GrievanceStatus.SLA_BREACHED
            if sla_result == "breached"
            else GrievanceStatus.OPEN
        )

        # Update shared Blackboard
        self.blackboard.update_grievance(
            reference_id,
            action="SLA evaluated",
            details=(
                f"Deadline: {deadline.isoformat()}, "
                f"Result: {sla_result}"
            ),
            deadline_at=deadline,
            status=new_status
        )

        return {
            "reference_id": reference_id,
            "deadline": deadline.isoformat(),
            "sla_status": sla_result,
            "grievance_status": new_status.value
        }
