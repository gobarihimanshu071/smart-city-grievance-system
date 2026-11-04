
from datetime import datetime, timedelta

from backend.blackboard.board import Blackboard
from backend.blackboard.models import (
    Grievance,
    GrievanceCategory,
    GrievanceStatus
)

from backend.agents.sla_agent import SLAAgent
from backend.agents.escalation_agent import EscalationAgent


# Create shared Blackboard
board = Blackboard()

# Create grievance
grievance = Grievance(
    reference_id="GRV-ESC-001",
    complaint_text="Water leakage near Model Town"
)

grievance.category = GrievanceCategory.WATER
grievance.location = "Model Town"
grievance.department = "Water Department"

board.add_grievance(grievance)

# Initialize SLA Agent
sla_agent = SLAAgent(board)

# Simulate a time 49 hours after submission
future_time = grievance.created_at + timedelta(hours=49)

sla_result = sla_agent.process(
    "GRV-ESC-001",
    current_time=future_time
)

print("SLA RESULT")
print(sla_result)

assert sla_result["sla_status"] == "breached"

# Initialize Escalation Agent
escalation_agent = EscalationAgent(board)

result = escalation_agent.process("GRV-ESC-001")

print("\nESCALATION RESULT")
print("-----------------")

print("Reference ID:", result["reference_id"])
print("Escalation Level:", result["escalation_level"])
print("Authority:", result["authority"])
print("Status:", result["status"])

print("\nESCALATION SUMMARY")
print("------------------")
print(result["summary"])

# Verify Blackboard
updated = board.get_grievance("GRV-ESC-001")

assert updated.status == GrievanceStatus.ESCALATED
assert updated.escalation_level == 1

print("\nSHARED BLACKBOARD")
print("Status:", updated.status.value)
print("Escalation Level:", updated.escalation_level)

print("\nEscalation Agent test passed!")
