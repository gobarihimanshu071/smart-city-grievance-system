
from backend.blackboard.board import Blackboard

from backend.tools.routing_tools import (
    resolve_department,
    get_department_queue
)


class DepartmentRouterAgent:
    """
    Assigns grievances to the correct department queue.
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

        if grievance.category is None:
            raise ValueError(
                "Grievance must be classified before routing."
            )

        # Tool 1: Resolve department
        department = resolve_department(
            grievance.category.value
        )

        # Assign grievance to department
        self.blackboard.update_grievance(
            reference_id,
            action="Department assigned",
            details=f"Assigned to {department}",
            department=department
        )

        # Tool 2: Retrieve updated department queue
        queue = get_department_queue(
            self.blackboard,
            department
        )

        return {
            "reference_id": reference_id,
            "category": grievance.category.value,
            "department": department,
            "queue_size": len(queue)
        }
