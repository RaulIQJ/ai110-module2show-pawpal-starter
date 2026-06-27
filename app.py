from datetime import time

import streamlit as st
from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Status, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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
        # Choosing a pet here is what assigns the Task to that pet.
        pet = st.selectbox(
            "For which pet?", options=owner.pets, format_func=lambda p: p.name
        )
        add_task = st.form_submit_button("Add task")
    if add_task:
        owner.add_task(
            Task(
                name=task_title,
                duration_min=int(duration),
                priority=PRIORITY_MAP[priority],
                pet=pet,
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

        # --- filters (use the Scheduler's filter methods) ------------------
        sched = Scheduler(owner)
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
        pending = [t for t in tasks if t.status != Status.DONE]
        if pending:
            to_complete = st.selectbox(
                "Mark a task complete",
                options=pending,
                format_func=lambda t: f"{t.name} ({t.pet.name}, {t.start_time or 'no time'})",
            )
            if st.button("Mark complete"):
                next_task = to_complete.mark_done()
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
        st.caption(f"Total scheduled: {total}/{owner.available_minutes} min")

        # Conflict warnings (overlapping start times) — informative, not fatal.
        for warning in scheduler.detect_conflicts():
            st.warning(f"Time conflict: {warning}")

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
