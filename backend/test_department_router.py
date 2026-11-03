
from backend.blackboard.board import Blackboard
from backend.blackboard.models import (
    Grievance,
    GrievanceCategory
)

from backend.agents.classifier_agent import ClassifierAgent
from backend.agents.department_router import DepartmentRouterAgent


# Create shared Blackboard
board = Blackboard()

# Create a grievance
grievance = Grievance(
    reference_id="GRV-ROUTE-001",
    complaint_text="There is a water leakage near Model Town."
)

board.add_grievance(grievance)

# Agent 1: Classify grievance
classifier = ClassifierAgent(board)

classification = classifier.process("GRV-ROUTE-001")

print("CLASSIFIER RESULT")
print(classification)


# Agent 2: Route grievance
router = DepartmentRouterAgent(board)

routing = router.process("GRV-ROUTE-001")

print("\nDEPARTMENT ROUTER RESULT")

for key, value in routing.items():
    print(f"{key}: {value}")


# Verify shared Blackboard
updated = board.get_grievance("GRV-ROUTE-001")

print("\nSHARED BLACKBOARD")
print("Category:", updated.category.value)
print("Department:", updated.department)

assert updated.category == GrievanceCategory.WATER
assert updated.department == "Water Department"

print("\nDepartment Router test passed!")
