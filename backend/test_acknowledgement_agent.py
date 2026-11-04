
from datetime import datetime

from backend.blackboard.board import Blackboard
from backend.blackboard.models import Grievance

from backend.agents.classifier_agent import ClassifierAgent
from backend.agents.department_router import DepartmentRouterAgent
from backend.agents.sla_agent import SLAAgent
from backend.agents.acknowledgement_agent import AcknowledgementAgent


# Create shared Blackboard
board = Blackboard()

# Create grievance
grievance = Grievance(
    reference_id="GRV-ACK-001",
    complaint_text="There is a water leakage near Model Town."
)

board.add_grievance(grievance)

# Agent 1: Classification
classifier = ClassifierAgent(board)
classifier.process("GRV-ACK-001")

# Agent 2: Department routing
router = DepartmentRouterAgent(board)
router.process("GRV-ACK-001")

# Agent 3: SLA processing
sla_agent = SLAAgent(board)
sla_agent.process(
    "GRV-ACK-001",
    current_time=datetime.now()
)

# Agent 4: Acknowledgement
ack_agent = AcknowledgementAgent(board)
result = ack_agent.process("GRV-ACK-001")

print("ACKNOWLEDGEMENT AGENT RESULT")
print("----------------------------")
print("Reference ID:", result["reference_id"])
print("Expected Timeline:", result["expected_timeline"])

print("\nCITIZEN ACKNOWLEDGEMENT")
print("-----------------------")
print(result["acknowledgement"])

# Verify Blackboard
updated = board.get_grievance("GRV-ACK-001")

assert updated.acknowledgement is not None
assert "GRV-ACK-001" in updated.acknowledgement
assert "Water Department" in updated.acknowledgement

print("\nAcknowledgement Agent test passed!")
