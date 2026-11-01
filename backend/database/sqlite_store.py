
import sqlite3
import json

from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

from backend.blackboard.models import (
    Grievance,
    GrievanceCategory,
    GrievanceStatus
)


# Database file will be created inside backend/database/
DB_PATH = Path(__file__).parent / "grievances.db"


class SQLiteStore:

    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.create_tables()

    @contextmanager
    def get_connection(self):
        connection = sqlite3.connect(self.db_path)

        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def create_tables(self):
        """Create the grievance table if it does not exist."""

        with self.get_connection() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS grievances (
                    reference_id TEXT PRIMARY KEY,
                    complaint_text TEXT NOT NULL,
                    category TEXT,
                    location TEXT,
                    department TEXT,
                    created_at TEXT NOT NULL,
                    deadline_at TEXT,
                    status TEXT NOT NULL,
                    acknowledgement TEXT,
                    escalation_level INTEGER DEFAULT 0,
                    duplicate_of TEXT,
                    history TEXT
                )
            """)

    def save_grievance(self, grievance: Grievance):
        """Insert or update a grievance."""

        with self.get_connection() as connection:

            connection.execute("""
                INSERT OR REPLACE INTO grievances (
                    reference_id,
                    complaint_text,
                    category,
                    location,
                    department,
                    created_at,
                    deadline_at,
                    status,
                    acknowledgement,
                    escalation_level,
                    duplicate_of,
                    history
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                grievance.reference_id,
                grievance.complaint_text,
                grievance.category.value if grievance.category else None,
                grievance.location,
                grievance.department,
                grievance.created_at.isoformat(),
                grievance.deadline_at.isoformat()
                if grievance.deadline_at else None,
                grievance.status.value,
                grievance.acknowledgement,
                grievance.escalation_level,
                grievance.duplicate_of,
                json.dumps(grievance.history)
            ))

    def get_grievance(self, reference_id: str):
        """Retrieve a grievance from SQLite."""

        with self.get_connection() as connection:

            connection.row_factory = sqlite3.Row

            row = connection.execute(
                "SELECT * FROM grievances WHERE reference_id = ?",
                (reference_id,)
            ).fetchone()

        if row is None:
            return None

        return self._row_to_grievance(row)

    def get_all_grievances(self):
        """Retrieve all stored grievances."""

        with self.get_connection() as connection:

            connection.row_factory = sqlite3.Row

            rows = connection.execute(
                "SELECT * FROM grievances"
            ).fetchall()

        return [
            self._row_to_grievance(row)
            for row in rows
        ]

    def find_by_location(self, location: str):
        """Find previous grievances from a location."""

        with self.get_connection() as connection:

            connection.row_factory = sqlite3.Row

            rows = connection.execute("""
                SELECT * FROM grievances
                WHERE LOWER(TRIM(location)) = LOWER(TRIM(?))
            """, (location,)).fetchall()

        return [
            self._row_to_grievance(row)
            for row in rows
        ]

    @staticmethod
    def _row_to_grievance(row):
        """Convert a database row into a Grievance object."""

        return Grievance(
            reference_id=row["reference_id"],
            complaint_text=row["complaint_text"],
            category=(
                GrievanceCategory(row["category"])
                if row["category"] else None
            ),
            location=row["location"],
            department=row["department"],
            created_at=datetime.fromisoformat(row["created_at"]),
            deadline_at=(
                datetime.fromisoformat(row["deadline_at"])
                if row["deadline_at"] else None
            ),
            status=GrievanceStatus(row["status"]),
            acknowledgement=row["acknowledgement"],
            escalation_level=row["escalation_level"],
            duplicate_of=row["duplicate_of"],
            history=json.loads(row["history"] or "[]")
        )
