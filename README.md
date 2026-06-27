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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
