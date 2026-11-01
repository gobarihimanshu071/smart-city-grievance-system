
from typing import Optional
from threading import RLock

from backend.blackboard.models import Grievance
from backend.database.sqlite_store import SQLiteStore


class Blackboard:
    """
    Shared grievance state for all agents.

    Supports both in-memory operation and SQLite persistence.
    """

    def __init__(
        self,
        store: Optional[SQLiteStore] = None
    ):
        self._grievances: dict[str, Grievance] = {}
        self._lock = RLock()
        self.store = store

        # Load existing records from SQLite
        if self.store:
            for grievance in self.store.get_all_grievances():
                self._grievances[grievance.reference_id] = grievance

    def add_grievance(self, grievance: Grievance) -> None:

        with self._lock:

            if grievance.reference_id in self._grievances:
                raise ValueError(
                    f"Grievance {grievance.reference_id} already exists."
                )

            grievance.add_history(
                "Added to Blackboard",
                "Grievance stored in shared memory"
            )

            # Persist before publishing to shared memory
            if self.store:
                self.store.save_grievance(grievance)

            self._grievances[grievance.reference_id] = grievance

    def get_grievance(
        self,
        reference_id: str
    ) -> Optional[Grievance]:

        with self._lock:
            return self._grievances.get(reference_id)

    def update_grievance(
        self,
        reference_id: str,
        action: str,
        details: str = "",
        **updates
    ) -> Grievance:

        with self._lock:

            grievance = self._grievances.get(reference_id)

            if grievance is None:
                raise KeyError(
                    f"Grievance {reference_id} not found."
                )

            allowed_fields = {
                "category",
                "location",
                "department",
                "deadline_at",
                "status",
                "acknowledgement",
                "escalation_level",
                "duplicate_of"
            }

            invalid_fields = set(updates) - allowed_fields

            if invalid_fields:
                raise ValueError(
                    f"Invalid fields: {invalid_fields}"
                )

            # Apply changes
            for field_name, value in updates.items():
                setattr(grievance, field_name, value)

            grievance.add_history(action, details)

            # Persist updated grievance
            if self.store:
                self.store.save_grievance(grievance)

            return grievance

    def get_all_grievances(self) -> list[Grievance]:

        with self._lock:
            return list(self._grievances.values())

    def find_by_location(
        self,
        location: str
    ) -> list[Grievance]:

        normalized_location = location.strip().casefold()

        with self._lock:
            return [
                grievance
                for grievance in self._grievances.values()
                if grievance.location
                and grievance.location.strip().casefold()
                == normalized_location
            ]

    def count(self) -> int:

        with self._lock:
            return len(self._grievances)
