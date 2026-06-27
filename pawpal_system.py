"""PawPal+ system classes.

Skeleton generated from diagrams/uml.mmd. Method bodies are stubs for now —
fill in the scheduling logic incrementally (README workflow step 4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum


def hhmm_to_minutes(value: str) -> int:
    """Convert a "HH:MM" string to minutes since midnight.

    An empty string returns 24*60 (end of day) so unscheduled tasks sort last.
    """
    if not value:
        return 24 * 60
    hours, minutes = value.split(":")
    return int(hours) * 60 + int(minutes)


def minutes_to_hhmm(total: int) -> str:
    """Convert minutes since midnight back into a "HH:MM" string."""
    return f"{total // 60:02d}:{total % 60:02d}"


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


class Frequency(Enum):
    """How often a task repeats. NONE means a one-off task."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"


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
    # This pet's own care tasks. repr/compare disabled to break the
    # Pet <-> Task reference cycle (Task.pet points back here), which would
    # otherwise make the dataclass __repr__ / __eq__ recurse forever.
    tasks: list[Task] = field(default_factory=list, repr=False, compare=False)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet (keeps task.pet pointing back here)."""
        task.pet = self
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return how many tasks this pet currently has."""
        return len(self.tasks)

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
    frequency: Frequency = Frequency.NONE
    due_date: date | None = None
    goal: str = ""
    constraints: list[str] = field(default_factory=list)

    def mark_done(self) -> Task | None:
        """Mark this task complete; if recurring, spawn its next occurrence.

        Returns the newly created next-occurrence Task (already attached to the
        same pet), or None for a one-off (NONE) task.
        """
        self.status = Status.DONE
        nxt = self.next_occurrence()
        if nxt is not None:
            self.pet.add_task(nxt)
        return nxt

    def next_occurrence(self) -> Task | None:
        """Build the next occurrence of a recurring task (None if one-off).

        Per the brief, the new due date is today + 1 day (DAILY) or today + 1
        week (WEEKLY), computed with timedelta. The new task starts PENDING.
        """
        if self.frequency == Frequency.NONE:
            return None
        step = timedelta(days=1) if self.frequency == Frequency.DAILY else timedelta(weeks=1)
        return Task(
            name=self.name,
            duration_min=self.duration_min,
            priority=self.priority,
            pet=self.pet,
            start_time=self.start_time,
            frequency=self.frequency,
            due_date=date.today() + step,
            goal=self.goal,
            constraints=list(self.constraints),  # copy so occurrences don't share
        )

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

    def add_pet(self, pet: Pet) -> None:
        """Register a pet as belonging to this owner."""
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Assign a care task by routing it to its pet (task.pet)."""
        task.pet.add_task(task)

    def list_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets (flattened)."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Builds one combined daily plan across all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for the given owner with an empty task plan."""
        self.owner = owner
        self.tasks: list[Task] = []

    def make_schedule(self) -> list[Task]:
        """Produce the ordered daily plan that fits the owner's time budget.

        Already-completed (DONE) tasks are skipped so they are never re-planned.
        """
        self.tasks = [t for t in self.owner.list_tasks() if t.status != Status.DONE]
        self.tasks = self.sort_by_priority()
        self.tasks = self.fits_in_time(self.owner.available_minutes)
        return self.tasks

    def sort_by_priority(self) -> list[Task]:
        """Return tasks ordered HIGH -> LOW (tie-break by shorter duration)."""
        return sorted(self.tasks, key=lambda t: (-t.priority.value, t.duration_min))

    def sort_by_time(self) -> list[Task]:
        """Return tasks ordered by start_time ("HH:MM"), earliest first.

        The lambda key turns each "HH:MM" string into minutes since midnight
        (via hhmm_to_minutes) so the times compare as numbers. Tasks with no
        start_time sort last.
        """
        return sorted(self.tasks, key=lambda t: hhmm_to_minutes(t.start_time))

    def filter_by_status(
        self, status: Status, tasks: list[Task] | None = None
    ) -> list[Task]:
        """Return only the tasks with the given status (e.g. PENDING or DONE).

        Reads all of the owner's tasks by default, or filters a list you pass in
        (so filters can be chained, e.g. by status then by pet).
        """
        source = self.owner.list_tasks() if tasks is None else tasks
        return [t for t in source if t.status == status]

    def filter_by_pet(
        self, pet_name: str, tasks: list[Task] | None = None
    ) -> list[Task]:
        """Return only the tasks belonging to the pet with the given name."""
        source = self.owner.list_tasks() if tasks is None else tasks
        return [t for t in source if t.pet.name == pet_name]

    def detect_conflicts(self) -> list[str]:
        """Return a warning string for each pair of tasks whose times overlap.

        Lightweight: only considers active (non-DONE) tasks that have a
        start_time. Two tasks overlap when one starts before the other ends,
        using start_time + duration_min. Returns [] when there are no
        conflicts — it never raises.
        """
        timed = sorted(
            (
                t
                for t in self.owner.list_tasks()
                if t.start_time and t.status != Status.DONE
            ),
            key=lambda t: hhmm_to_minutes(t.start_time),
        )
        warnings: list[str] = []
        for i, earlier in enumerate(timed):
            earlier_end = hhmm_to_minutes(earlier.start_time) + earlier.duration_min
            for later in timed[i + 1 :]:
                # list is sorted by start, so later starts >= earlier starts
                if hhmm_to_minutes(later.start_time) < earlier_end:
                    warnings.append(
                        f"'{earlier.name}' ({earlier.pet.name}, "
                        f"{earlier.start_time}-{minutes_to_hhmm(earlier_end)}) "
                        f"overlaps '{later.name}' ({later.pet.name}, "
                        f"starts {later.start_time})"
                    )
        return warnings

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