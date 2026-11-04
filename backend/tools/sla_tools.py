
from datetime import datetime, timedelta


# Demonstration policy, not official municipal SLA values.
SLA_POLICY = {
    "water": 48,
    "roads": 168,
    "electricity": 24,
    "sanitation": 24
}


def calculate_deadline(
    created_at: datetime,
    category: str
) -> datetime:
    """Calculate a grievance deadline using its category."""

    if category not in SLA_POLICY:
        raise ValueError(
            f"No SLA policy configured for: {category}"
        )

    duration_hours = SLA_POLICY[category]

    return created_at + timedelta(hours=duration_hours)


def evaluate_sla(
    deadline_at: datetime,
    current_time: datetime | None = None
) -> str:
    """Determine whether the grievance deadline has passed."""

    if current_time is None:
        current_time = datetime.now()

    if current_time >= deadline_at:
        return "breached"

    return "on_time"
