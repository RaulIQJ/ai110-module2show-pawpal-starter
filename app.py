from datetime import time

import streamlit as st
from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Status, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** helps a pet owner plan a realistic day of pet care. Add your pets and
their tasks (each with a time, duration, priority, and an optional daily/weekly
repeat), then generate a schedule that fits your available time — ordered by
time, with any overlapping tasks flagged as conflicts.
"""
)

with st.expander("What PawPal+ can do"):
    st.markdown(
        """
- **Sort** tasks by priority, and display the day ordered by start time
- **Fit** tasks into your daily time budget (highest priority first)
- **Filter** tasks by pet or completion status
- **Flag conflicts** when two tasks overlap in time
- **Repeat** daily/weekly tasks — completing one schedules the next occurrence
- **Explain** why each task made it into the plan
"""
    )

# Maps the UI's priority strings to the Priority enum the Task/Scheduler expect.
PRIORITY_MAP = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
# Maps the UI's repeat choices to the Frequency enum.
FREQUENCY_MAP = {
    "one-off": Frequency.NONE,
    "daily": Frequency.DAILY,
    "weekly": Frequency.WEEKLY,
}

st.divider()

# ---------------------------------------------------------------------------
# 1. Owner — everything else is guarded behind this existing in the session.
# ---------------------------------------------------------------------------
st.subheader("1. Owner")

if "owner" not in st.session_state:
    # No owner yet: show the creation form, then stop so nothing below renders.
    with st.form("create_owner"):
        owner_name = st.text_input("Owner name", value="Jordan")
        owner_age = st.number_input("Owner age", min_value=0, max_value=120, value=30)
        owner_gender = st.text_input("Owner gender (optional)", value="")
        submitted = st.form_submit_button("Create owner")
    if submitted:
        st.session_state.owner = Owner(
            name=owner_name, age=int(owner_age), gender=owner_gender
        )
        st.rerun()
    st.info("Create an owner to get started.")
    st.stop()  # nothing below makes sense without an owner

owner = st.session_state.owner
st.success(f"Owner: **{owner.name}** (age {owner.age})")
if st.button("Reset owner"):
    del st.session_state.owner
    st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# 2. Pets — only reachable once an owner exists (st.stop() above).
# ---------------------------------------------------------------------------
st.subheader("2. Pets")

with st.form("add_pet"):
    pet_name = st.text_input("Pet name", value="Mochi")
    pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=2)
    pet_weight = st.number_input("Weight (kg, optional)", min_value=0.0, value=0.0)
    add_pet = st.form_submit_button("Add pet")
if add_pet:
    owner.add_pet(Pet(name=pet_name, age=int(pet_age), weight=float(pet_weight)))
    st.rerun()

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "age": p.age, "weight": p.weight} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# 3. Tasks — guarded behind at least one pet existing.
# ---------------------------------------------------------------------------
st.subheader("3. Tasks")

if not owner.pets:
    st.info("Add a pet first — every task must belong to a pet.")
else:
    with st.form("add_task"):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        # st.time_input returns a datetime.time, so no manual HH:MM parsing.
        start = st.time_input("Start time", value=time(8, 0))
        repeat = st.selectbox("Repeat", ["one-off", "daily", "weekly"])
        # Select by INDEX, not the Pet object: Streamlit returns a *copy* of a
        # selected object, so we must look the real pet back up in owner.pets.
        pet_index = st.selectbox(
            "For which pet?",
            options=range(len(owner.pets)),
            format_func=lambda i: owner.pets[i].name,
        )
        add_task = st.form_submit_button("Add task")
    if add_task:
        owner.add_task(
            Task(
                name=task_title,
                duration_min=int(duration),
                priority=PRIORITY_MAP[priority],
                pet=owner.pets[pet_index],  # the real, persisted Pet object
                start_time=start.strftime("%H:%M"),  # stored as "HH:MM"
                frequency=FREQUENCY_MAP[repeat],
            )
        )
        st.rerun()

    tasks = owner.list_tasks()
    # One-shot message after a recurring task spawned its next occurrence.
    recurrence_msg = st.session_state.pop("recurrence_msg", None)
    if recurrence_msg:
        st.success(recurrence_msg)
    if tasks:
        st.write("Current tasks:")
        sched = Scheduler(owner)

        # --- proactive conflict banner (visible while adding tasks) --------
        conflicts = sched.detect_conflicts()
        if conflicts:
            st.warning(f"⚠️ {len(conflicts)} time conflict(s) detected:")
            for c in conflicts:
                st.write(f"- {c}")

        # --- filters (use the Scheduler's filter methods) ------------------
        STATUS_FILTERS = {"pending": Status.PENDING, "done": Status.DONE}
        col_a, col_b = st.columns(2)
        with col_a:
            status_choice = st.selectbox("Filter by status", ["all", "pending", "done"])
        with col_b:
            pet_choice = st.selectbox(
                "Filter by pet", ["all"] + [p.name for p in owner.pets]
            )

        shown = tasks
        if status_choice != "all":
            shown = sched.filter_by_status(STATUS_FILTERS[status_choice], shown)
        if pet_choice != "all":
            shown = sched.filter_by_pet(pet_choice, shown)

        if shown:
            st.table(
                [
                    {
                        "task": t.name,
                        "pet": t.pet.name,
                        "start": t.start_time or "—",
                        "duration_min": t.duration_min,
                        "priority": t.priority.name,
                        "repeat": t.frequency.value,
                        "due": t.due_date.isoformat() if t.due_date else "—",
                        "status": t.status.value,
                    }
                    for t in shown
                ]
            )
        else:
            st.caption("No tasks match the current filters.")

        # --- mark a task complete -----------------------------------------
        # Index into the live task list (same copy-on-select caveat as above).
        pending_indexes = [i for i, t in enumerate(tasks) if t.status != Status.DONE]
        if pending_indexes:
            chosen = st.selectbox(
                "Mark a task complete",
                options=pending_indexes,
                format_func=lambda i: (
                    f"{tasks[i].name} ({tasks[i].pet.name}, "
                    f"{tasks[i].start_time or 'no time'})"
                ),
            )
            if st.button("Mark complete"):
                next_task = tasks[chosen].mark_done()  # real, persisted Task
                if next_task is not None:
                    st.session_state["recurrence_msg"] = (
                        f"'{next_task.name}' repeats {next_task.frequency.value} — "
                        f"next occurrence created for {next_task.due_date}."
                    )
                st.rerun()
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# 4. Schedule — runs the Scheduler over the owner's tasks + time budget.
# ---------------------------------------------------------------------------
st.subheader("4. Build Schedule")

available_minutes = st.number_input(
    "Available minutes today", min_value=0, max_value=1440, value=60
)

all_tasks = owner.list_tasks()
if st.button("Generate schedule", disabled=not all_tasks):
    owner.available_minutes = int(available_minutes)
    scheduler = Scheduler(owner)
    plan = scheduler.make_schedule()

    if not plan:
        st.warning("No tasks fit the available time.")
    else:
        # Priority + budget decide WHAT gets in; time decides the ORDER shown.
        plan_by_time = scheduler.sort_by_time()
        total = sum(t.duration_min for t in plan)
        st.write(f"### Today's plan for {owner.name}")
        st.table(
            [
                {
                    "#": i,
                    "start": t.start_time or "—",
                    "task": t.name,
                    "pet": t.pet.name,
                    "duration_min": t.duration_min,
                    "priority": t.priority.name,
                }
                for i, t in enumerate(plan_by_time, start=1)
            ]
        )
        st.metric("Scheduled", f"{total} / {owner.available_minutes} min")

        # Conflict warnings (overlapping start times) — informative, not fatal.
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(f"Time conflict: {warning}")
        else:
            st.success("No time conflicts. ✅")

        # Only count active tasks as "dropped" (DONE tasks are intentionally skipped).
        dropped = [t for t in all_tasks if t not in plan and t.status != Status.DONE]
        if dropped:
            st.write("**Dropped (did not fit / lower priority):**")
            for t in dropped:
                st.write(f"- {t.name} ({t.pet.name}) — {t.duration_min} min")

    with st.expander("Why this schedule?"):
        st.text(scheduler.explain())

if not all_tasks:
    st.info("Add at least one task to build a schedule.")
