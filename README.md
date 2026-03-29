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
