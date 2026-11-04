
from datetime import datetime, timedelta

from backend.blackboard.board import Blackboard
from backend.blackboard.models import (
    Grievance,
    GrievanceCategory,
    GrievanceStatus
)

from backend.agents.sla_agent import SLAAgent


# Create shared Blackboard
board = Blackboard()

# Create grievance
grievance = Grievance(
    reference_id="GRV-SLA-001",
    complaint_text="Water leakage near Model Town"
)

grievance.category = GrievanceCategory.WATER
grievance.location = "Model Town"
grievance.department = "Water Department"

board.add_grievance(grievance)

# Initialize SLA Agent
sla_agent = SLAAgent(board)

# Scenario 1: Complaint is within deadline
now = datetime.now()

result = sla_agent.process(
    "GRV-SLA-001",
    current_time=now
)

print("SCENARIO 1: ON-TIME GRIEVANCE")
print(result)

assert result["sla_status"] == "on_time"

# Scenario 2: Deadline has passed
future_check = now + timedelta(hours=49)

result = sla_agent.process(
    "GRV-SLA-001",
    current_time=future_check
)

print("\nSCENARIO 2: BREACHED GRIEVANCE")
print(result)

assert result["sla_status"] == "breached"

# Verify shared Blackboard
updated = board.get_grievance("GRV-SLA-001")

print("\nSHARED BLACKBOARD")
print("Deadline:", updated.deadline_at)
print("Status:", updated.status.value)

assert updated.status == GrievanceStatus.SLA_BREACHED

print("\nSLA Agent test passed!")
