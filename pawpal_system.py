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
        self.fed = True

    def give_meds(self) -> None:
        """Record that this pet has had its medication."""
        self.needs_meds = False

    def record_weight(self, kg: float) -> None:
        """Update the pet's recorded weight."""
        self.weight = kg

    def care_summary(self) -> str:
        """Return a short human-readable summary of outstanding care needs."""
        print(f"Care summary for {self.name}:")
        needs = []
        if not self.fed:
            needs.append("needs feeding")
        if self.needs_meds:
            needs.append("needs medication")
        if self.needs_grooming:
            needs.append("needs grooming")
        if self.needs_enrichment:
            needs.append("needs enrichment")
        if not needs:
            return "All care needs are met."
        return ", ".join(needs)

@dataclass
class Task:
    """A single care action for one pet (walk, feeding, meds, etc.)."""

    name: str
    duration_min: int
    priority: Priority
    pet: Pet
    status: Status = Status.PENDING
    start_time: str = ""  # scheduled clock time, "HH:MM" (24-hour), e.g. "09:30"
    goal: str = ""
    constraints: list[str] = field(default_factory=list)

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.status = Status.DONE

    def is_done(self) -> bool:
        """Return True if the task has been completed."""
        return self.status == Status.DONE


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
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Assign a care task (for one of this owner's pets)."""
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets."""
        for task in self.tasks:
            print(f"Task: {task.name}, Pet: {task.pet.name}, Duration: {task.duration_min} min, Priority: {task.priority.name}, Status: {task.status.value}")


class Scheduler:
    """Builds one combined daily plan across all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for the given owner with an empty task plan."""
        self.owner = owner
        self.tasks: list[Task] = []

    def make_schedule(self) -> list[Task]:
        """Produce the ordered daily plan that fits the owner's time budget."""
        self.tasks = list(self.owner.tasks)
        self.tasks = self.sort_by_priority()
        self.tasks = self.fits_in_time(self.owner.available_minutes)
        return self.tasks

    def sort_by_priority(self) -> list[Task]:
        """Return tasks ordered HIGH -> LOW (tie-break by shorter duration)."""
        return sorted(self.tasks, key=lambda t: (-t.priority.value, t.duration_min))

    def sort_by_time(self) -> list[Task]:
        """Return tasks ordered by start_time ("HH:MM"), earliest first.

        The lambda key turns each "HH:MM" string into total minutes since
        midnight (HH * 60 + MM) so they compare as numbers. Tasks with no
        start_time set sort last.
        """
        return sorted(
            self.tasks,
            key=lambda t: (
                int(t.start_time.split(":")[0]) * 60 + int(t.start_time.split(":")[1])
                if t.start_time
                else 24 * 60  # unscheduled tasks go to the end
            ),
        )

    def fits_in_time(self, budget: int) -> list[Task]:
        """Return the subset of tasks that fits within the given minutes."""
        plan: list[Task] = []
        remaining = budget
        for task in self.tasks:
            if task.duration_min <= remaining:
                plan.append(task)
                remaining -= task.duration_min
        return plan

    def explain(self) -> str:
        """Explain why the schedule was built the way it was."""
        explanation = "Schedule Explanation:\n"
        explanation += f"Owner: {self.owner.name}, Available Minutes: {self.owner.available_minutes}\n"
        explanation += "Scheduled Tasks:\n"
        for task in self.tasks:
            explanation += f"- Task: {task.name}, Pet: {task.pet.name}, Duration: {task.duration_min} min, Priority: {task.priority.name}, Status: {task.status.value}\n"
        return explanation