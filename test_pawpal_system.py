"""Tests for PawPal+ scheduling behavior.

These define the intended contract for the Scheduler methods. They will FAIL
until the stubs in pawpal_system.py are implemented (TDD red -> green).

Assumed contracts (adjust here if you decide on different behavior):
  - sort_by_priority(): HIGH before LOW; ties broken by SHORTER duration first.
  - fits_in_time(budget): greedily walk tasks in their current order, keep a
    task if it fits the remaining budget, otherwise skip it and try the next.
  - make_schedule(): gather all the owner's tasks, sort by priority, then fit
    them into owner.available_minutes. Returns one combined plan (all pets).
"""

from datetime import date, timedelta

import pytest

from pawpal_system import (
    Frequency,
    Owner,
    Pet,
    Priority,
    Scheduler,
    Status,
    Task,
)


# --- fixtures / helpers ----------------------------------------------------


@pytest.fixture
def pet():
    return Pet(name="Biscuit", age=3)


@pytest.fixture
def other_pet():
    return Pet(name="Whiskers", age=5)


def make_task(name, duration, priority, pet):
    return Task(name=name, duration_min=duration, priority=priority, pet=pet)


# --- sort_by_priority ------------------------------------------------------


def test_sort_orders_high_priority_first(pet):
    low = make_task("nap watch", 10, Priority.LOW, pet)
    high = make_task("meds", 5, Priority.HIGH, pet)
    med = make_task("feed", 10, Priority.MEDIUM, pet)

    sched = Scheduler(Owner(name="Ada", age=30))
    sched.tasks = [low, high, med]

    ordered = sched.sort_by_priority()

    assert [t.priority for t in ordered] == [
        Priority.HIGH,
        Priority.MEDIUM,
        Priority.LOW,
    ]


def test_sort_breaks_ties_by_shorter_duration_first(pet):
    long_high = make_task("long walk", 40, Priority.HIGH, pet)
    short_high = make_task("quick meds", 5, Priority.HIGH, pet)

    sched = Scheduler(Owner(name="Ada", age=30))
    sched.tasks = [long_high, short_high]

    ordered = sched.sort_by_priority()

    assert ordered == [short_high, long_high]


def test_sort_does_not_mutate_original_list(pet):
    a = make_task("a", 10, Priority.LOW, pet)
    b = make_task("b", 5, Priority.HIGH, pet)
    sched = Scheduler(Owner(name="Ada", age=30))
    original = [a, b]
    sched.tasks = original

    sched.sort_by_priority()

    assert sched.tasks == original  # same objects, same order


# --- fits_in_time ----------------------------------------------------------


def test_fits_in_time_keeps_tasks_within_budget(pet):
    t1 = make_task("walk", 30, Priority.HIGH, pet)
    t2 = make_task("feed", 10, Priority.HIGH, pet)
    sched = Scheduler(Owner(name="Ada", age=30))
    sched.tasks = [t1, t2]

    plan = sched.fits_in_time(60)

    assert plan == [t1, t2]  # 40 min total fits in 60


def test_fits_in_time_drops_tasks_that_overflow_budget(pet):
    big = make_task("long walk", 50, Priority.HIGH, pet)
    small = make_task("meds", 5, Priority.HIGH, pet)
    sched = Scheduler(Owner(name="Ada", age=30))
    sched.tasks = [big, small]

    plan = sched.fits_in_time(40)

    # big (50) overflows and is skipped; small (5) still fits
    assert big not in plan
    assert small in plan


def test_fits_in_time_zero_budget_returns_empty(pet):
    sched = Scheduler(Owner(name="Ada", age=30))
    sched.tasks = [make_task("walk", 30, Priority.HIGH, pet)]

    assert sched.fits_in_time(0) == []


# --- make_schedule (combined plan across all pets) -------------------------


def test_make_schedule_combines_tasks_from_all_pets(pet, other_pet):
    owner = Owner(name="Ada", age=30, available_minutes=120)
    owner.add_pet(pet)
    owner.add_pet(other_pet)
    owner.add_task(make_task("Biscuit walk", 30, Priority.HIGH, pet))
    owner.add_task(make_task("Whiskers meds", 5, Priority.HIGH, other_pet))
    sched = Scheduler(owner)

    plan = sched.make_schedule()

    pets_in_plan = {t.pet.name for t in plan}
    assert pets_in_plan == {"Biscuit", "Whiskers"}


def test_make_schedule_orders_by_priority(pet):
    owner = Owner(name="Ada", age=30, available_minutes=120)
    owner.add_pet(pet)
    owner.add_task(make_task("enrichment", 20, Priority.LOW, pet))
    owner.add_task(make_task("meds", 5, Priority.HIGH, pet))
    sched = Scheduler(owner)

    plan = sched.make_schedule()

    assert plan[0].priority == Priority.HIGH


def test_make_schedule_respects_time_budget_dropping_low_priority(pet):
    owner = Owner(name="Ada", age=30, available_minutes=35)
    owner.add_pet(pet)
    must_do = make_task("meds", 5, Priority.HIGH, pet)
    walk = make_task("walk", 30, Priority.HIGH, pet)
    extra = make_task("long enrichment", 30, Priority.LOW, pet)
    for t in (extra, walk, must_do):
        owner.add_task(t)
    sched = Scheduler(owner)

    plan = sched.make_schedule()

    # 35 min budget fits the two HIGH tasks (35 total); LOW extra is dropped
    assert must_do in plan
    assert walk in plan
    assert extra not in plan


def test_make_schedule_with_no_tasks_returns_empty():
    owner = Owner(name="Ada", age=30, available_minutes=60)
    sched = Scheduler(owner)

    assert sched.make_schedule() == []


# --- Task / status sanity --------------------------------------------------


def test_task_starts_pending(pet):
    t = make_task("walk", 30, Priority.HIGH, pet)
    assert t.status == Status.PENDING


def test_mark_done_sets_status_done(pet):
    t = make_task("walk", 30, Priority.HIGH, pet)
    t.mark_done()
    assert t.is_done() is True
    assert t.status == Status.DONE


# --- Pet / Owner task ownership --------------------------------------------


def test_adding_task_to_pet_increases_task_count(pet):
    assert pet.task_count() == 0
    pet.add_task(make_task("walk", 30, Priority.HIGH, pet))
    assert pet.task_count() == 1
    pet.add_task(make_task("meds", 5, Priority.HIGH, pet))
    assert pet.task_count() == 2


def test_owner_list_tasks_aggregates_across_all_pets(pet, other_pet):
    owner = Owner(name="Ada", age=30)
    owner.add_pet(pet)
    owner.add_pet(other_pet)
    owner.add_task(make_task("Biscuit walk", 30, Priority.HIGH, pet))
    owner.add_task(make_task("Whiskers meds", 5, Priority.HIGH, other_pet))

    all_tasks = owner.list_tasks()

    assert len(all_tasks) == 2
    assert {t.pet.name for t in all_tasks} == {"Biscuit", "Whiskers"}


# --- sort_by_time ----------------------------------------------------------


def test_sort_by_time_orders_chronologically(pet):
    sched = Scheduler(Owner(name="Ada", age=30))
    late = Task("late", 10, Priority.LOW, pet, start_time="14:00")
    early = Task("early", 10, Priority.LOW, pet, start_time="08:30")
    mid = Task("mid", 10, Priority.LOW, pet, start_time="09:15")
    sched.tasks = [late, early, mid]

    assert sched.sort_by_time() == [early, mid, late]


def test_sort_by_time_puts_unscheduled_last(pet):
    sched = Scheduler(Owner(name="Ada", age=30))
    timed = Task("timed", 10, Priority.LOW, pet, start_time="10:00")
    untimed = Task("untimed", 10, Priority.LOW, pet)  # start_time == ""
    sched.tasks = [untimed, timed]

    assert sched.sort_by_time() == [timed, untimed]


# --- filtering -------------------------------------------------------------


def test_filter_by_status_splits_pending_and_done(pet):
    owner = Owner(name="Ada", age=30)
    owner.add_pet(pet)
    done = make_task("done", 10, Priority.LOW, pet)
    done.mark_done()
    pending = make_task("pending", 10, Priority.LOW, pet)
    owner.add_task(done)
    owner.add_task(pending)
    sched = Scheduler(owner)

    assert sched.filter_by_status(Status.DONE) == [done]
    assert sched.filter_by_status(Status.PENDING) == [pending]


def test_filter_by_pet_returns_only_that_pets_tasks(pet, other_pet):
    owner = Owner(name="Ada", age=30)
    owner.add_pet(pet)
    owner.add_pet(other_pet)
    biscuit_task = make_task("walk", 10, Priority.LOW, pet)
    whiskers_task = make_task("meds", 10, Priority.LOW, other_pet)
    owner.add_task(biscuit_task)
    owner.add_task(whiskers_task)
    sched = Scheduler(owner)

    assert sched.filter_by_pet("Biscuit") == [biscuit_task]


# --- conflict detection ----------------------------------------------------


def test_detect_conflicts_flags_overlapping_tasks(pet):
    owner = Owner(name="Ada", age=30)
    owner.add_pet(pet)
    # 08:00-08:30 overlaps a task that starts at 08:15
    owner.add_task(Task("walk", 30, Priority.HIGH, pet, start_time="08:00"))
    owner.add_task(Task("meds", 5, Priority.HIGH, pet, start_time="08:15"))
    sched = Scheduler(owner)

    assert len(sched.detect_conflicts()) == 1


def test_detect_conflicts_none_when_back_to_back(pet):
    owner = Owner(name="Ada", age=30)
    owner.add_pet(pet)
    # 08:00-08:30 then 08:30 start: touching, not overlapping
    owner.add_task(Task("walk", 30, Priority.HIGH, pet, start_time="08:00"))
    owner.add_task(Task("meds", 5, Priority.HIGH, pet, start_time="08:30"))
    sched = Scheduler(owner)

    assert sched.detect_conflicts() == []


# --- make_schedule skips completed tasks -----------------------------------


def test_make_schedule_skips_done_tasks(pet):
    owner = Owner(name="Ada", age=30, available_minutes=120)
    owner.add_pet(pet)
    done = make_task("done walk", 30, Priority.HIGH, pet)
    done.mark_done()
    pending = make_task("meds", 5, Priority.HIGH, pet)
    owner.add_task(done)
    owner.add_task(pending)
    sched = Scheduler(owner)

    plan = sched.make_schedule()

    assert done not in plan
    assert pending in plan


# --- recurring tasks -------------------------------------------------------


def test_marking_daily_task_complete_creates_next_day_occurrence(pet):
    task = Task("walk", 20, Priority.HIGH, pet, frequency=Frequency.DAILY)

    nxt = task.mark_done()

    assert task.is_done()
    assert nxt is not None
    assert nxt.status == Status.PENDING
    assert nxt.due_date == date.today() + timedelta(days=1)
    assert nxt.frequency == Frequency.DAILY


def test_marking_weekly_task_complete_creates_next_week_occurrence(pet):
    task = Task("groom", 30, Priority.MEDIUM, pet, frequency=Frequency.WEEKLY)

    nxt = task.mark_done()

    assert nxt is not None
    assert nxt.due_date == date.today() + timedelta(weeks=1)


def test_one_off_task_does_not_recur(pet):
    task = Task("vet visit", 60, Priority.HIGH, pet)  # frequency defaults to NONE

    nxt = task.mark_done()

    assert nxt is None


def test_recurrence_attaches_next_occurrence_to_the_pet(pet):
    task = Task("walk", 20, Priority.HIGH, pet, frequency=Frequency.DAILY)
    pet.add_task(task)
    assert pet.task_count() == 1

    task.mark_done()

    # the original (now DONE) plus the freshly spawned occurrence
    assert pet.task_count() == 2
    assert any(t.status == Status.PENDING for t in pet.tasks)
