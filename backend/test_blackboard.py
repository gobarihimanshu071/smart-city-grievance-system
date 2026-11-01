
from backend.blackboard.models import Grievance
from backend.blackboard.board import Blackboard


# Create one shared Blackboard
board = Blackboard()


# Create two grievances from the same location
grievance1 = Grievance(
    reference_id="GRV-2026-00001",
    complaint_text="Water leakage near Model Town"
)

grievance1.location = "Model Town"

grievance2 = Grievance(
    reference_id="GRV-2026-00002",
    complaint_text="Drainage problem near Model Town"
)

grievance2.location = "Model Town"


# Store both grievances
board.add_grievance(grievance1)
board.add_grievance(grievance2)


# Retrieve one grievance
result = board.get_grievance("GRV-2026-00001")

print("Retrieved grievance:")
print(result.reference_id, result.complaint_text)


# Update a grievance
board.update_grievance(
    "GRV-2026-00001",
    action="Department assigned",
    details="Assigned to Water Department",
    department="Water Department"
)

print("\nUpdated department:")
print(board.get_grievance("GRV-2026-00001").department)


# Search previous grievances by location
previous = board.find_by_location("model town")

print("\nPrevious grievances from Model Town:")

for grievance in previous:
    print(grievance.reference_id, "-", grievance.complaint_text)


# Count grievances
print("\nTotal grievances:", board.count())
