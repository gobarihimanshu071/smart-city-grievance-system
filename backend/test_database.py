
from backend.database.sqlite_store import SQLiteStore

from backend.blackboard.models import (
    Grievance,
    GrievanceCategory
)


# Initialize SQLite
database = SQLiteStore()

# Create a grievance
grievance = Grievance(
    reference_id="GRV-2026-00010",
    complaint_text="Water leakage near Model Town"
)

grievance.category = GrievanceCategory.WATER
grievance.location = "Model Town"
grievance.department = "Water Department"

grievance.add_history(
    "Grievance created",
    "Saved to SQLite database"
)

# Save grievance
database.save_grievance(grievance)

print("Grievance saved successfully!")

# Retrieve grievance
retrieved = database.get_grievance("GRV-2026-00010")

print("\nRetrieved from SQLite:")
print("Reference ID:", retrieved.reference_id)
print("Complaint:", retrieved.complaint_text)
print("Category:", retrieved.category.value)
print("Location:", retrieved.location)
print("Department:", retrieved.department)
print("Status:", retrieved.status.value)

# Search location history
previous = database.find_by_location("model town")

print("\nGrievances found at Model Town:", len(previous))

# Display all records
print("\nTotal database records:", len(database.get_all_grievances()))
