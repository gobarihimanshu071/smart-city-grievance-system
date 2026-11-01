
import tempfile
from pathlib import Path

from backend.blackboard.board import Blackboard
from backend.blackboard.models import (
    Grievance,
    GrievanceCategory,
    GrievanceStatus
)
from backend.database.sqlite_store import SQLiteStore


with tempfile.TemporaryDirectory() as temp_dir:

    db_path = Path(temp_dir) / "test_grievances.db"

    # First application instance
    database1 = SQLiteStore(db_path)
    board1 = Blackboard(store=database1)

    # Create and store a grievance
    grievance = Grievance(
        reference_id="GRV-PERSIST-001",
        complaint_text="Water leakage near Model Town"
    )

    grievance.category = GrievanceCategory.WATER
    grievance.location = "Model Town"

    board1.add_grievance(grievance)

    board1.update_grievance(
        "GRV-PERSIST-001",
        action="Department assigned",
        details="Assigned to Water Department",
        department="Water Department"
    )

    print("First Blackboard:")
    print("Total grievances:", board1.count())

    # Simulate application restart:
    # Create a completely new Blackboard instance
    database2 = SQLiteStore(db_path)
    board2 = Blackboard(store=database2)

    print("\nAfter simulated restart:")

    recovered = board2.get_grievance("GRV-PERSIST-001")

    print("Reference ID:", recovered.reference_id)
    print("Location:", recovered.location)
    print("Department:", recovered.department)
    print("Status:", recovered.status.value)
    print("History entries:", len(recovered.history))

    assert recovered is not None
    assert recovered.department == "Water Department"
    assert recovered.category == GrievanceCategory.WATER
    assert recovered.status == GrievanceStatus.OPEN

    print("\nPersistence test passed!")
