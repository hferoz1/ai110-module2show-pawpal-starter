# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Features

PawPal+ includes a scheduler that supports practical planning algorithms for day-to-day pet care:

- **Priority-based planning**: Builds a daily plan by ranking pending tasks from highest to lowest priority.
- **Sorting by time**: Orders tasks chronologically by `start_time` for timeline-style views.
- **Time-budget constraints**: Only schedules tasks that fit within the owner's available minutes.
- **Conflict warnings**: Detects overlaps and duplicate start-time collisions on the same date.
- **Daily and weekly recurrence**: Completing recurring tasks automatically creates the next due instance.
- **Smart task filtering**: Filters by completion status, pet name, and category for focused views.
- **Multi-pet aggregation**: Collects tasks across all pets under one owner for unified scheduling.

## 📸 Demo

<a href="/course_images/ai110/StreamlitAppScreenshot.png" target="_blank"><img src='/course_images/ai110/StreamlitAppScreenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

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

## Smarter Scheduling

The `Scheduler` class goes beyond a simple to-do list with several algorithmic features:

- **Priority-ranked daily plan** — `generate_plan` greedily selects pending tasks from highest to lowest priority, fitting as many as possible within the owner's available time budget.
- **Conflict detection** — `detect_conflicts` converts each task's start time and duration into a minutes-since-midnight window and flags any two tasks on the same date whose windows overlap.
- **Recurring task rollover** — `mark_task_complete` automatically creates the next occurrence of a `daily` or `weekly` task with the correct future due date, so the schedule stays populated without manual re-entry.
- **Flexible filtering** — `filter_tasks` lets callers slice tasks by completion status, pet name, or both, enabling targeted views (e.g. "pending tasks for Buddy only").

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

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

Current test coverage includes core scheduler behavior and edge cases, including:

- Task completion state updates.
- Adding tasks to pets.
- Priority sorting correctness.
- Chronological sorting correctness by start time.
- Daily plan generation within owner time constraints.
- Empty-plan behavior when no tasks are available.
- Excluding completed tasks from planning.
- Recurrence rollover for daily and weekly tasks.
- Non-recurrence behavior for one-time tasks.
- Conflict detection for overlapping and duplicate-time tasks.
- No-conflict behavior for adjacent tasks.
- Skipping unscheduled tasks in conflict checks.

Test status: `15 passed`.

Confidence Level: `★★★★★` (5/5)
