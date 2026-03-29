"""
app.py — PawPal+ Streamlit UI
=============================
Entry point for the PawPal+ interactive web app.

Responsibilities:
  - Collect owner, pet, and task information from the user via Streamlit widgets.
  - Store task data across reruns using st.session_state.
  - Build Owner / Pet / Task domain objects from the collected data and pass
    them to the Scheduler backend (pawpal_system.py).
  - Display the generated daily care plan, conflict warnings, and skipped tasks
    using Streamlit layout components (st.table, st.metric, st.warning, etc.).

Run with:
    streamlit run app.py
"""

import streamlit as st
from datetime import date, time as dtime
from pawpal_system import Task, Pet, Owner, Scheduler

# ── Page configuration ────────────────────────────────────────────────────────
# Sets the browser tab title, favicon, and overall page width.
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling for busy owners.")

# ── Session state initialisation ──────────────────────────────────────────────
# raw_tasks persists the list of task dicts across Streamlit reruns so that
# tasks added in one interaction are still available when the user clicks
# "Generate Schedule" later.
if "raw_tasks" not in st.session_state:
    st.session_state.raw_tasks = []  # each item is a plain dict (not a Task object)

# ── Section 1 — Owner & Pet Info ──────────────────────────────────────────────
# Collects the owner's name, daily time budget, and basic pet details.
# These values are used to construct Owner and Pet objects at schedule-generation
# time so the Scheduler can apply the time constraint correctly.
with st.expander("👤 Owner & Pet Info", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        # Owner's display name — passed straight to Owner(name, …)
        owner_name = st.text_input("Owner name", value="Jordan")
        # Total minutes the owner can spend on pet care today; becomes
        # Owner.available_time and acts as the Scheduler's time budget.
        available_time = st.number_input(
            "Available time today (min)", min_value=10, max_value=480, value=120
        )
    with col2:
        # Pet's display name — passed to Pet(name, …)
        pet_name = st.text_input("Pet name", value="Mochi")
        # Species string stored on the Pet object for profile display
        species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
        # Age in years — stored on the Pet object
        pet_age = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)

st.divider()

# ── Section 2 — Task Entry Form ───────────────────────────────────────────────
# Lets the owner describe a care activity (title, category, duration, priority,
# due date, optional start time) and appends it to st.session_state.raw_tasks.
# Using st.form batches all widget values and only triggers a rerun when the
# submit button is pressed — preventing premature reruns while the user types.
st.subheader("📋 Add Care Tasks")

with st.form("task_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        # Short name for the care activity; becomes Task.title
        task_title = st.text_input("Task title", value="Morning walk")
        # Activity type used by Scheduler.get_tasks_by_category(); becomes Task.category
        category = st.selectbox(
            "Category",
            ["feeding", "exercise", "grooming", "medication", "play", "vet", "other"],
        )
        # How often the task recurs; used by Scheduler.mark_task_complete() to
        # schedule the next occurrence automatically.  Becomes Task.frequency.
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        # Free-text notes; stored as Task.description (not shown in the schedule table)
        description = st.text_input("Description (optional)", value="")
    with col2:
        # Estimated time in minutes; used by generate_plan() to fit tasks within
        # the owner's available_time budget.  Becomes Task.duration.
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        # Integer urgency score 1–10; higher scores are scheduled first by
        # Scheduler.rank_tasks().  Becomes Task.priority.
        priority = st.slider("Priority (1–10)", min_value=1, max_value=10, value=5)
        # Calendar date the task is due; used by detect_conflicts() to compare
        # only same-day tasks.  Becomes Task.due_date.
        task_date = st.date_input("Due date", value=date.today())

    # Optional start-time inputs — rendered every run but only applied when
    # the checkbox is ticked.  If provided, the values become Task.start_time
    # (a datetime.time object) and enable sort_by_time() and detect_conflicts().
    col3, col4, col5 = st.columns([1, 1, 1])
    with col3:
        # Toggle that controls whether start_hour / start_min are used
        use_time = st.checkbox("Set a start time?")
    with col4:
        # 24-hour clock hour component of the planned start time
        start_hour = st.number_input("Hour (0–23)", min_value=0, max_value=23, value=8)
    with col5:
        # Minute component of the planned start time
        start_min = st.number_input("Minute (0–59)", min_value=0, max_value=59, value=0)

    # Submitting the form appends one dict to raw_tasks and triggers a rerun
    submitted = st.form_submit_button("➕ Add Task")

# ── Handle form submission ────────────────────────────────────────────────────
# Runs only on the rerun immediately after the user clicks "Add Task".
# Converts widget values into a plain dict and stores it in session state.
# We store dicts (not Task objects) because Streamlit session state must be
# serialisable, and dicts are simpler to inspect / mutate.
if submitted:
    # Build a datetime.time only when the owner explicitly set a start time;
    # None means the task is "flexible" and will appear last in sort_by_time().
    start_time_val = dtime(int(start_hour), int(start_min)) if use_time else None
    st.session_state.raw_tasks.append(
        {
            "title": task_title,
            "duration": int(duration),
            "priority": int(priority),
            "category": category,
            "description": description,
            "frequency": frequency,
            "due_date": task_date,       # kept as datetime.date for Task constructor
            "start_time": start_time_val,  # datetime.time or None
            "completed": False,          # new tasks always start as pending
        }
    )
    st.success(f"Task '{task_title}' added!")

# ── Current task table ────────────────────────────────────────────────────────
# Shows the full list of raw_tasks in a readable table so the owner can review
# what they've entered before generating the schedule.
if st.session_state.raw_tasks:
    st.markdown("**Current tasks:**")
    # Build display-friendly dicts; format start_time as "HH:MM" or "—"
    display_rows = [
        {
            "Title": t["title"],
            "Category": t["category"],
            "Priority": t["priority"],
            "Duration (min)": t["duration"],
            "Frequency": t["frequency"],
            "Due Date": str(t["due_date"]),
            "Start Time": t["start_time"].strftime("%H:%M") if t["start_time"] else "—",
        }
        for t in st.session_state.raw_tasks
    ]
    st.table(display_rows)

    # Gives the owner a way to start fresh without restarting the app
    if st.button("🗑️ Clear all tasks"):
        st.session_state.raw_tasks = []
        st.rerun()
else:
    # Shown when raw_tasks is empty so the owner knows what to do next
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Section 3 — Schedule Generation ──────────────────────────────────────────
# The main scheduling surface.  Clicking the button triggers the full pipeline:
#   1. Build Owner / Pet / Task domain objects from session-state dicts.
#   2. Run detect_conflicts() — highlight overlapping timed tasks.
#   3. Run generate_plan() — select and rank tasks within the time budget.
#   4. Display the plan, high-priority callouts, and any skipped tasks.
st.subheader("📅 Generate Daily Schedule")

if st.button("⚡ Generate Schedule", type="primary"):
    # Guard: require at least one task before attempting to build a plan
    if not st.session_state.raw_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        # Reconstruct domain objects each time the button is clicked so the
        # schedule always reflects the current state of raw_tasks.
        owner = Owner(owner_name, int(available_time))
        pet = Pet(pet_name, species, int(pet_age))

        # Convert each raw dict back into a Task object and attach it to the pet.
        # mark_complete() is called for any tasks the owner has already finished
        # so the Scheduler's get_pending_tasks() filters them out correctly.
        for raw in st.session_state.raw_tasks:
            task = Task(
                title=raw["title"],
                duration=raw["duration"],
                priority=raw["priority"],
                category=raw["category"],
                description=raw["description"],
                frequency=raw["frequency"],
                due_date=raw["due_date"],
                start_time=raw["start_time"],
            )
            if raw["completed"]:
                task.mark_complete()
            pet.add_task(task)

        # Wire up the ownership graph so get_all_tasks() traverses correctly
        owner.add_pet(pet)
        scheduler = Scheduler()

        # ── Conflict detection ────────────────────────────────────────────────
        # detect_conflicts() compares every pair of timed tasks on the same date
        # and returns a list of human-readable warning strings for any overlaps.
        # We show these BEFORE the plan so the owner can fix conflicts before
        # acting on the schedule — an unresolved conflict means two tasks are
        # literally scheduled at the same time and one will be skipped.
        conflicts = scheduler.detect_conflicts(owner)
        if conflicts:
            # Top-level error banner: draws the eye immediately
            st.error(
                f"⚠️ **{len(conflicts)} scheduling conflict(s) found!**  \n"
                "Two or more tasks overlap in time. Resolve these before you start "
                "your day so nothing gets missed."
            )
            for c in conflicts:
                # Strip the "WARNING: " prefix that detect_conflicts() prepends
                # and show each conflict as its own yellow warning box so each
                # one is individually readable.
                friendly = c.replace("WARNING: ", "")
                st.warning(f"🕐 {friendly}")
            # Actionable tip so the owner knows exactly how to fix the problem
            st.markdown("**Tip:** Adjust a task's start time or shorten its duration to fix the overlap.")
            st.markdown("---")

        # ── Plan generation ───────────────────────────────────────────────────
        # generate_plan() returns (plan, time_used):
        #   plan      — list of Task objects that fit within available_time,
        #               sorted highest-priority-first by rank_tasks()
        #   time_used — total minutes consumed by the scheduled tasks
        plan, time_used = scheduler.generate_plan(owner)
        time_remaining = int(available_time) - time_used  # slack for ad-hoc tasks

        # Summary metrics row — gives the owner a quick quantitative overview
        # before they read the full table
        col1, col2, col3 = st.columns(3)
        col1.metric("Tasks Scheduled", len(plan))
        col2.metric("Time Used (min)", time_used)
        col3.metric("Time Remaining (min)", time_remaining)

        if not plan:
            # Edge case: every task exceeds the available time budget on its own
            st.warning(
                "No tasks fit within your available time. "
                "Try increasing your available time or reducing task durations."
            )
        else:
            st.success(
                f"Here's **{pet_name}'s** care plan for today, {owner_name}! "
                "Tasks are sorted by priority, then by start time."
            )

            # Choose sort order: chronological when any task has a concrete start
            # time (so the owner can follow the plan top-to-bottom throughout the
            # day); otherwise keep the priority-ranked order from generate_plan().
            has_times = any(t.start_time is not None for t in plan)
            sorted_plan = scheduler.sort_by_time(plan) if has_times else plan

            # Build table rows with a human-readable priority badge so urgency
            # is scannable at a glance without reading the raw number.
            rows = []
            for i, task in enumerate(sorted_plan, 1):
                # Map the numeric priority to a colour-coded label
                if task.priority > 7:
                    badge = "🔴 High"
                elif task.priority >= 4:
                    badge = "🟡 Medium"
                else:
                    badge = "🟢 Low"

                rows.append(
                    {
                        "#": i,
                        "Task": task.title,
                        "Category": task.category.capitalize(),
                        "Priority": f"{badge} ({task.priority})",
                        "Duration": f"{task.duration} min",
                        # Show the clock time when available; "Flexible" signals
                        # the owner can slot this in whenever suits them.
                        "Start Time": (
                            task.start_time.strftime("%H:%M")
                            if task.start_time
                            else "Flexible"
                        ),
                        "Frequency": task.frequency,
                    }
                )

            # Render the full plan as a static table (no interactivity needed)
            st.table(rows)

            # High-priority callout — tasks with priority > 7 get a second,
            # prominent mention below the table so they can't be accidentally
            # overlooked (is_high_priority() checks task.priority > 7).
            high_pri = [t for t in sorted_plan if t.is_high_priority()]
            if high_pri:
                st.error(
                    f"🚨 **Don't skip these — {len(high_pri)} high-priority "
                    f"task(s) need your attention today:**"
                )
                for t in high_pri:
                    # Inline the start time only when one was set
                    st.markdown(
                        f"- **{t.title}** · {t.category} · {t.duration} min"
                        + (
                            f" · starts at {t.start_time.strftime('%H:%M')}"
                            if t.start_time
                            else ""
                        )
                    )

        # ── Skipped tasks ─────────────────────────────────────────────────────
        # Tasks that were pending but didn't make it into the plan (because
        # adding them would exceed available_time).  Shown in a collapsed
        # expander so they don't clutter the main view but are still accessible.
        all_pending = scheduler.get_pending_tasks(owner)
        skipped = [t for t in all_pending if t not in plan]
        if skipped:
            with st.expander(
                f"⏭️ {len(skipped)} task(s) couldn't fit today — see what was skipped"
            ):
                st.caption(
                    "These tasks were left out because there wasn't enough time. "
                    "Consider scheduling them tomorrow or freeing up more time."
                )
                for t in skipped:
                    st.markdown(
                        f"- **{t.title}** ({t.category}) — "
                        f"{t.duration} min | Priority: {t.priority}"
                    )
