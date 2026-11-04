
from backend.blackboard.models import (
    Grievance,
    GrievanceStatus
)

from backend.blackboard.board import Blackboard


ESCALATION_HIERARCHY = {
    1: "Senior Department Officer",
    2: "Municipal Commissioner",
    3: "City Grievance Review Committee"
}


def find_breached_grievances(
    blackboard: Blackboard
) -> list[Grievance]:
    """Find grievances marked as SLA breached."""

    return [
        grievance
        for grievance in blackboard.get_all_grievances()
        if grievance.status == GrievanceStatus.SLA_BREACHED
    ]


def select_next_authority(
    current_escalation_level: int
) -> tuple[int, str]:
    """Select the next authority in the escalation hierarchy."""

    next_level = current_escalation_level + 1

    authority = ESCALATION_HIERARCHY.get(next_level)

    if authority is None:
        raise ValueError(
            "Maximum escalation level has been reached."
        )

    return next_level, authority


def create_escalation_summary(
    grievance: Grievance,
    authority: str
) -> str:
    """Prepare a summary for the higher authority."""

    if not grievance.reference_id:
        raise ValueError("Reference ID is missing.")

    return f"""
ESCALATION REPORT

Reference ID: {grievance.reference_id}
Complaint: {grievance.complaint_text}
Category: {grievance.category.value if grievance.category else "Unknown"}
Location: {grievance.location or "Unknown"}
Department: {grievance.department or "Unassigned"}
SLA Deadline: {
    grievance.deadline_at.isoformat()
    if grievance.deadline_at else "Unknown"
}
Current Status: {grievance.status.value}

Escalated To: {authority}

Reason:
The grievance has exceeded its configured SLA deadline
and requires intervention by the next authority.
""".strip()
