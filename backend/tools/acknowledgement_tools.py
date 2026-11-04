
from datetime import datetime


def format_expected_timeline(deadline: datetime) -> str:
    """Convert a deadline into a readable citizen-facing timeline."""

    if not isinstance(deadline, datetime):
        raise ValueError("A valid SLA deadline is required.")

    return deadline.strftime("%d %B %Y at %I:%M %p")


def draft_acknowledgement(
    reference_id: str,
    category: str,
    location: str,
    department: str,
    expected_timeline: str
) -> str:
    """Generate a citizen grievance acknowledgement."""

    required_fields = {
        "reference_id": reference_id,
        "category": category,
        "location": location,
        "department": department,
        "expected_timeline": expected_timeline
    }

    for field, value in required_fields.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing required field: {field}")

    message = f"""
Dear Citizen,

Your grievance has been successfully registered with our
Smart City Grievance Redressal System.

Reference ID: {reference_id}
Category: {category.title()}
Location: {location}
Assigned Department: {department}
Expected Resolution Deadline: {expected_timeline}

Your complaint has been forwarded to the concerned department.
Please use your reference ID to track its progress.

Thank you for helping us improve our city.

Smart City Grievance Redressal System
""".strip()

    return message
