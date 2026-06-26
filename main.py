"""Temporary manual test harness for the PawPal+ system.

Run with:  python main.py

Builds an owner with a couple of pets and several care tasks, then prints the
schedule the Scheduler produces so we can eyeball the method behavior.
"""

from pawpal_system import Owner, Pet, Priority, Scheduler, Status, Task


def main() -> None:
    # --- pets --------------------------------------------------------------
    biscuit = Pet(name="Biscuit", age=3, weight=12.5, gender="M")
    whiskers = Pet(name="Whiskers", age=5, weight=4.2, gender="F", needs_meds=True)

    # --- owner with a limited daily time budget ----------------------------
    owner = Owner(name="Ada", age=30, gender="F", available_minutes=60)
    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    # --- tasks added OUT OF ORDER (by time) to exercise sort_by_time -------
    # "Morning walk" 08:00-08:30 and "Give meds" 08:15 intentionally overlap
    # so detect_conflicts() has something to flag.
    owner.add_task(Task("Puzzle feeder enrichment", 25, Priority.LOW, whiskers, start_time="09:30"))
    owner.add_task(Task("Morning walk", 30, Priority.HIGH, biscuit, start_time="08:00"))
    owner.add_task(Task("Brush coat", 15, Priority.MEDIUM, biscuit, start_time="09:00"))
    owner.add_task(Task("Give meds", 5, Priority.HIGH, whiskers, start_time="08:15"))

    # --- build and print the schedule --------------------------------------
    scheduler = Scheduler(owner)
    plan = scheduler.make_schedule()

    total = sum(task.duration_min for task in plan)

    print(f"\n=== Today's Schedule for {owner.name} ===")
    print(f"Time budget: {owner.available_minutes} min\n")

    if not plan:
        print("(no tasks fit the available time)")
    else:
        for i, task in enumerate(plan, start=1):
            print(
                f"{i}. {task.name} ({task.pet.name}) "
                f"- {task.duration_min} min "
                f"[{task.priority.name}]"
            )

    print(f"\nTotal scheduled: {total}/{owner.available_minutes} min")

    # tasks that did not make the cut
    skipped = [t for t in owner.list_tasks() if t not in plan]
    if skipped:
        print("\nDropped (did not fit / lower priority):")
        for task in skipped:
            print(f"- {task.name} ({task.pet.name}) - {task.duration_min} min")

    print("\n" + scheduler.explain())

    # --- sort_by_time: chronological view of the whole day -----------------
    scheduler.tasks = owner.list_tasks()  # sort over ALL tasks, not just the plan
    print("=== All tasks sorted by start time ===")
    for task in scheduler.sort_by_time():
        print(f"- {task.start_time}  {task.name} ({task.pet.name})")

    # --- filtering ---------------------------------------------------------
    print("\n=== Filter: Biscuit's tasks ===")
    for task in scheduler.filter_by_pet("Biscuit"):
        print(f"- {task.name} ({task.start_time})")

    print("\n=== Filter: still pending ===")
    for task in scheduler.filter_by_status(Status.PENDING):
        print(f"- {task.name} ({task.pet.name})")

    # --- conflict detection ------------------------------------------------
    print("\n=== Conflict check ===")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"WARNING: {warning}")
    else:
        print("No scheduling conflicts.")


if __name__ == "__main__":
    main()
