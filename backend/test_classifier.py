
from backend.blackboard.board import Blackboard
from backend.blackboard.models import Grievance
from backend.agents.classifier_agent import ClassifierAgent


# Create shared Blackboard
board = Blackboard()

# Create a citizen grievance
grievance = Grievance(
    reference_id="GRV-CLASS-001",
    complaint_text=(
        "There is a huge water leakage near Model Town."
    )
)

# Add grievance to Blackboard
board.add_grievance(grievance)

# Initialize Classifier Agent
classifier = ClassifierAgent(board)

# Process grievance
result = classifier.process("GRV-CLASS-001")

print("CLASSIFIER AGENT RESULT")
print("-----------------------")

for key, value in result.items():
    print(f"{key}: {value}")

# Verify shared Blackboard update
updated = board.get_grievance("GRV-CLASS-001")

print("\nSHARED BLACKBOARD")
print("-----------------")
print("Category:", updated.category.value)
print("Location:", updated.location)

assert result["category"] == "water"
assert result["location"] == "Model Town"

print("\nClassifier test passed!")
