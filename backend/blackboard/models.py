
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class GrievanceCategory(str, Enum):
    WATER = "water"
    ROADS = "roads"
    ELECTRICITY = "electricity"
    SANITATION = "sanitation"


class GrievanceStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    SLA_BREACHED = "sla_breached"
    ESCALATED = "escalated"


@dataclass
class Grievance:
    reference_id: str
    complaint_text: str

    category: Optional[GrievanceCategory] = None
    location: Optional[str] = None
    department: Optional[str] = None

    created_at: datetime = field(
        default_factory=datetime.now
    )

    deadline_at: Optional[datetime] = None

    status: GrievanceStatus = GrievanceStatus.OPEN

    acknowledgement: Optional[str] = None

    escalation_level: int = 0

    duplicate_of: Optional[str] = None

    history: list = field(default_factory=list)

    def add_history(self, action: str, details: str = ""):
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        })
