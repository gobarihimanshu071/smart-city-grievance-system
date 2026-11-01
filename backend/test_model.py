
from backend.blackboard.models import (
    Grievance,
    GrievanceCategory,
    GrievanceStatus
)


complaint = Grievance(
    reference_id="GRV-2026-00001",
    complaint_text="Water leakage near Model Town"
)

complaint.category = GrievanceCategory.WATER
complaint.location = "Model Town"
complaint.department = "Water Department"

complaint.add_history(
    "Grievance created",
    "Citizen submitted a water leakage complaint"
)

print("Reference ID:", complaint.reference_id)
print("Category:", complaint.category.value)
print("Location:", complaint.location)
print("Department:", complaint.department)
print("Status:", complaint.status.value)
print("History:", complaint.history)
