"""PawPal+ system classes.

Skeleton generated from diagrams/uml.mmd. Method bodies are stubs for now —
fill in the scheduling logic incrementally (README workflow step 4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    """How important a task is, used by the scheduler to order tasks."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Status(Enum):
    """Lifecycle state of a task."""

    PENDING = "pending"
    DONE = "done"
    SKIPPED = "skipped"


@dataclass
class Pet:
    """An animal the owner cares for."""

    name: str
    age: int
    weight: float = 0.0
    gender: str = ""
    fed: bool = False
    needs_meds: bool = False
    needs_grooming: bool = False
    needs_enrichment: bool = False

    def feed(self) -> None:
        """Mark this pet as fed."""
        raise NotImplementedError

    def give_meds(self) -> None:
        """Record that this pet has had its medication."""
        raise NotImplementedError

    def record_weight(self, kg: float) -> None:
        """Update the pet's recorded weight."""
        raise NotImplementedError

    def care_summary(self) -> str:
        """Return a short human-readable summary of outstanding care needs."""
        raise NotImplementedError


@dataclass
class Task:
    """A single care action for one pet (walk, feeding, meds, etc.)."""

    name: str
    duration_min: int
    priority: Priority
    pet: Pet
    status: Status = Status.PENDING
    goal: str = ""
    constraints: list[str] = field(default_factory=list)

    def mark_done(self) -> None:
        """Mark this task as completed."""
        raise NotImplementedError

    def is_done(self) -> bool:
        """Return True if the task has been completed."""
        raise NotImplementedError


@dataclass
class Owner:
    """A pet owner with one or more pets and a daily time budget."""

    name: str
    age: int
    gender: str = ""
    available_minutes: int = 0
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet as belonging to this owner."""
        raise NotImplementedError

    def add_task(self, task: Task) -> None:
        """Assign a care task (for one of this owner's pets)."""
        raise NotImplementedError

    def list_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets."""
        raise NotImplementedError


class Scheduler:
    """Builds one combined daily plan across all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.tasks: list[Task] = []

    def make_schedule(self) -> list[Task]:
        """Produce the ordered daily plan that fits the owner's time budget."""
        raise NotImplementedError

    def sort_by_priority(self) -> list[Task]:
        """Return tasks ordered HIGH -> LOW (tie-break by duration)."""
        raise NotImplementedError

    def fits_in_time(self, budget: int) -> list[Task]:
        """Return the subset of tasks that fits within the given minutes."""
        raise NotImplementedError

    def explain(self) -> str:
        """Explain why the schedule was built the way it was."""
        raise NotImplementedError
