
from backend.blackboard.board import Blackboard


DEPARTMENT_MAPPING = {
    "water": "Water Department",
    "roads": "Road Maintenance Department",
    "electricity": "Electricity Department",
    "sanitation": "Sanitation Department"
}


def resolve_department(category: str) -> str:
    """Find the responsible department for a category."""

    if not category:
        raise ValueError("Grievance category is missing.")

    department = DEPARTMENT_MAPPING.get(category.lower())

    if department is None:
        raise ValueError(
            f"No department configured for category: {category}"
        )

    return department


def get_department_queue(
    blackboard: Blackboard,
    department: str
) -> list:
    """Retrieve grievances assigned to a department."""

    return [
        grievance
        for grievance in blackboard.get_all_grievances()
        if grievance.department == department
    ]
