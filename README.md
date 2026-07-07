# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Owner & multiple pets** — create an owner and add several pets, each with their own tasks.
- **Rich tasks** — every task has a duration, a priority (HIGH / MEDIUM / LOW), a start time (`HH:MM`), and an optional daily/weekly repeat.
- **Priority-aware daily plan** — builds a schedule that fits your available minutes, keeping the highest-priority tasks first (`Scheduler.make_schedule`).
- **Sorting by time** — the generated plan is shown in chronological order (`Scheduler.sort_by_time`).
- **Filtering** — view tasks by pet or by completion status (`Scheduler.filter_by_pet` / `filter_by_status`).
- **Conflict warnings** — overlapping task times are flagged both while adding tasks and in the schedule, without blocking you (`Scheduler.detect_conflicts`).
- **Daily / weekly recurrence** — completing a repeating task automatically creates its next occurrence (`Task.mark_done` → `Task.next_occurrence`).
- **Plan explanation** — see why each task was included in the day's plan (`Scheduler.explain`).

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Running `python main.py` produces the following plan:

```
=== Today's Schedule for Ada ===
Time budget: 60 min

1. Give meds (Whiskers) - 5 min [HIGH]
2. Morning walk (Biscuit) - 30 min [HIGH]
3. Brush coat (Biscuit) - 15 min [MEDIUM]

Total scheduled: 50/60 min

Dropped (did not fit / lower priority):
- Puzzle feeder enrichment (Whiskers) - 25 min

Schedule Explanation:
Owner: Ada, Available Minutes: 60
Scheduled Tasks:
- Task: Give meds, Pet: Whiskers, Duration: 5 min, Priority: HIGH, Status: pending
- Task: Morning walk, Pet: Biscuit, Duration: 30 min, Priority: HIGH, Status: pending
- Task: Brush coat, Pet: Biscuit, Duration: 15 min, Priority: MEDIUM, Status: pending
```

## 🧪 Testing PawPal+

Run the full automated test suite from the project root:

```bash
python -m pytest
```

The suite (`test_pawpal_system.py`) covers the system's most important behaviors:

- **Sorting** — `sort_by_priority` (HIGH → LOW, ties broken by shorter duration) and `sort_by_time` (chronological by `start_time`, unscheduled tasks last).
- **Time-budget fitting** — `fits_in_time` keeps tasks within budget and drops overflow; `make_schedule` combines all pets' tasks, orders by priority, respects the budget, and skips completed (DONE) tasks.
- **Task & pet ownership** — tasks start PENDING, `mark_done` sets DONE, adding a task to a pet increases its task count, and `Owner.list_tasks` aggregates across all pets.
- **Filtering** — `filter_by_status` and `filter_by_pet` return the correct subsets.
- **Conflict detection** — overlapping start times are flagged; back-to-back tasks are not.
- **Recurring tasks** — completing a DAILY/WEEKLY task creates the next occurrence (today + 1 day / + 1 week) and attaches it to the pet; one-off tasks do not recur.

Sample output from a successful run:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\qjuni\OneDrive\Desktop\CodePath\AI110\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 25 items

test_pawpal_system.py .........................                          [100%]

============================= 25 passed in 0.04s ==============================
```

**Confidence Level: 4 / 5** — All 25 tests pass and exercise the core scheduling logic (priority/time sorting, budget fitting, filtering, conflict detection, recurrence) plus edge cases such as empty task lists and back-to-back times. I would like to test more on streamlit, and see what other test cases there are and this is the reason I am holding back on the fifth star. Further more in the case of adding tasks around the time of midnight there might be some confusion on the wrap around and time placement of the task and so I need to test that. While also experiementing a bit more on streamlit.

## 📐 Smarter Scheduling

PawPal+ adds a layer of scheduling intelligence on top of the basic data model.
Each feature below is implemented by a specific method in `pawpal_system.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by priority | `Scheduler.sort_by_priority()` | Orders tasks HIGH → LOW, tie-broken by shorter duration first. |
| Sort by time | `Scheduler.sort_by_time()` | Orders tasks chronologically by `start_time` ("HH:MM"); unscheduled tasks sort last. Used to display the final plan in clock order. |
| Time-budget fitting | `Scheduler.fits_in_time()` / `Scheduler.make_schedule()` | Greedily keeps tasks (in priority order) while they fit the owner's `available_minutes`; completed (DONE) tasks are skipped. |
| Filter by status | `Scheduler.filter_by_status(status)` | Returns only tasks with a given status (e.g. PENDING or DONE). Chainable via an optional `tasks` argument. |
| Filter by pet | `Scheduler.filter_by_pet(pet_name)` | Returns only the tasks belonging to a named pet. Chainable with `filter_by_status`. |
| Conflict detection | `Scheduler.detect_conflicts()` | Lightweight overlap check using `start_time` + `duration_min`; returns warning strings (never raises). Back-to-back tasks are not flagged. |
| Recurring tasks | `Task.mark_done()` / `Task.next_occurrence()` | Marking a DAILY/WEEKLY task complete auto-creates the next occurrence (due `today + 1 day` or `+ 1 week`, via `timedelta`) and attaches it to the pet. |

Supporting helpers: `hhmm_to_minutes()` / `minutes_to_hhmm()` convert between
"HH:MM" strings and minutes-since-midnight for sorting and conflict math.

## 📸 Demo Walkthrough

PawPal+ runs as a Streamlit app (`streamlit run app.py`). The page is organized
top-to-bottom into four steps, and each one unlocks the next.

**Main UI features & what you can do**

1. **Owner** — create an owner (name, age). Nothing else appears until an owner exists.
2. **Pets** — add one or more pets (name, age, optional weight).
3. **Tasks** — add tasks for a chosen pet, each with a duration, priority, start time, and repeat (one-off / daily / weekly). Filter the task list by pet or status, and mark a task complete.
4. **Build Schedule** — enter your available minutes and generate the day's plan.

**Example workflow**

1. Create owner **Ada**.
2. Add pets **Biscuit** and **Whiskers**.
3. Add tasks: *Morning walk* (Biscuit, 08:00, 30 min, HIGH), *Give meds* (Whiskers, 08:15, 5 min, HIGH), *Brush coat* (Biscuit, 09:00, 15 min, MEDIUM).
4. Set **Available minutes = 60** and click **Generate schedule**.
5. View today's plan — ordered by time — with a conflict warning for the overlapping 08:00 and 08:15 tasks.

**Key Scheduler behaviors shown**

- **Priority + time-budget fitting** — the higher-priority tasks are kept until the 60-minute budget runs out; lower-priority ones are dropped.
- **Sort by time** — the plan is displayed 08:00 → 09:00 → …
- **Conflict warning** — *Morning walk (08:00–08:30)* overlaps *Give meds (08:15)*.
- **Recurrence** — marking a daily task complete schedules the next day's occurrence.
- **Explanation** — the "Why this schedule?" expander lists each scheduled task.

**Sample CLI output** (`python main.py`), which exercises the same backend the UI uses:

```text
=== Today's Schedule for Ada ===
Time budget: 60 min

1. Give meds (Whiskers) - 5 min [HIGH]
2. Morning walk (Biscuit) - 30 min [HIGH]
3. Brush coat (Biscuit) - 15 min [MEDIUM]

Total scheduled: 50/60 min

Dropped (did not fit / lower priority):
- Puzzle feeder enrichment (Whiskers) - 25 min

Schedule Explanation:
Owner: Ada, Available Minutes: 60
Scheduled Tasks:
- Task: Give meds, Pet: Whiskers, Duration: 5 min, Priority: HIGH, Status: pending
- Task: Morning walk, Pet: Biscuit, Duration: 30 min, Priority: HIGH, Status: pending
- Task: Brush coat, Pet: Biscuit, Duration: 15 min, Priority: MEDIUM, Status: pending

=== All tasks sorted by start time ===
- 08:00  Morning walk (Biscuit)
- 08:15  Give meds (Whiskers)
- 09:00  Brush coat (Biscuit)
- 09:30  Puzzle feeder enrichment (Whiskers)

=== Filter: Biscuit's tasks ===
- Morning walk (08:00)
- Brush coat (09:00)

=== Filter: still pending ===
- Morning walk (Biscuit)
- Brush coat (Biscuit)
- Puzzle feeder enrichment (Whiskers)
- Give meds (Whiskers)

=== Conflict check ===
WARNING: 'Morning walk' (Biscuit, 08:00-08:30) overlaps 'Give meds' (Whiskers, starts 08:15)

=== Recurring task ===
Before: Biscuit has 3 tasks; 'Evening walk' is pending
After marking done: 'Evening walk' is done
Auto-created next occurrence due 2026-07-07 (status pending)
Biscuit now has 4 tasks
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
