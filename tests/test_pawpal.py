from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task

def test_mark_complete_changes_status():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task("Walk the dog", duration=30, priority=5, category="exercise")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet("Buddy", species="dog", age=3)
    initial_count = len(pet.tasks)
    task = Task("Feed the pet", duration=10, priority=8, category="feeding")
    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1


def test_rank_tasks_orders_descending_priority():
    """Ensure rank_tasks returns tasks from highest to lowest priority."""
    scheduler = Scheduler()
    low = Task("Brush", duration=10, priority=2, category="grooming")
    high = Task("Medication", duration=5, priority=9, category="health")
    mid = Task("Walk", duration=20, priority=5, category="exercise")

    ranked = scheduler.rank_tasks([low, high, mid])

    assert [task.title for task in ranked] == ["Medication", "Walk", "Brush"]


def test_sort_by_time_returns_chronological_order():
    """Ensure sort_by_time returns tasks ordered from earliest to latest start_time."""
    scheduler = Scheduler()
    t1 = Task("Late walk", duration=20, priority=5, category="exercise", start_time=time(11, 30))
    t2 = Task("Breakfast", duration=10, priority=8, category="feeding", start_time=time(8, 0))
    t3 = Task("Midday meds", duration=5, priority=9, category="health", start_time=time(10, 15))

    ordered = scheduler.sort_by_time([t1, t2, t3])

    assert [task.title for task in ordered] == ["Breakfast", "Midday meds", "Late walk"]


def test_generate_plan_respects_available_time_budget():
    """Ensure generate_plan selects tasks without exceeding owner's available time."""
    owner = Owner("Hafsa", available_time=40)
    pet = Pet("Buddy", "dog", 3)
    owner.add_pet(pet)

    pet.add_task(Task("Long walk", duration=30, priority=9, category="exercise"))
    pet.add_task(Task("Feed", duration=10, priority=8, category="feeding"))
    pet.add_task(Task("Bath", duration=20, priority=4, category="grooming"))

    scheduler = Scheduler()
    plan, time_used = scheduler.generate_plan(owner)

    assert time_used <= owner.available_time
    assert [task.title for task in plan] == ["Long walk", "Feed"]
    assert time_used == 40


def test_generate_plan_returns_empty_for_owner_with_no_tasks():
    """Ensure generate_plan returns an empty plan when there are no tasks."""
    owner = Owner("Hafsa", available_time=60)
    owner.add_pet(Pet("Buddy", "dog", 3))
    scheduler = Scheduler()

    plan, time_used = scheduler.generate_plan(owner)

    assert plan == []
    assert time_used == 0


def test_generate_plan_ignores_completed_tasks():
    """Ensure completed tasks are excluded from generated plans."""
    owner = Owner("Hafsa", available_time=60)
    pet = Pet("Buddy", "dog", 3)
    owner.add_pet(pet)

    done_task = Task("Already done", duration=20, priority=10, category="health")
    done_task.mark_complete()
    pending_task = Task("Pending feed", duration=10, priority=6, category="feeding")
    pet.add_task(done_task)
    pet.add_task(pending_task)

    scheduler = Scheduler()
    plan, _ = scheduler.generate_plan(owner)

    assert [task.title for task in plan] == ["Pending feed"]


def test_mark_task_complete_creates_next_daily_task():
    """Ensure completing a daily task creates a new task due the next day."""
    scheduler = Scheduler()
    pet = Pet("Mochi", "cat", 2)
    task = Task(
        "Feed breakfast",
        duration=10,
        priority=8,
        category="feeding",
        frequency="daily",
        due_date=date(2026, 3, 29),
    )
    pet.add_task(task)

    new_task = scheduler.mark_task_complete(task, pet)

    assert task.completed is True
    assert new_task is not None
    assert new_task.title == task.title
    assert new_task.due_date == date(2026, 3, 30)


def test_mark_task_complete_creates_next_weekly_task():
    """Ensure completing a weekly task creates a new task due in one week."""
    scheduler = Scheduler()
    pet = Pet("Mochi", "cat", 2)
    task = Task(
        "Nail trim",
        duration=15,
        priority=7,
        category="grooming",
        frequency="weekly",
        due_date=date(2026, 3, 29),
    )

    new_task = scheduler.mark_task_complete(task, pet)

    assert task.completed is True
    assert new_task is not None
    assert new_task.due_date == date(2026, 4, 5)


def test_mark_task_complete_once_task_does_not_recur():
    """Ensure one-time tasks do not generate a recurring follow-up task."""
    scheduler = Scheduler()
    pet = Pet("Mochi", "cat", 2)
    task = Task("Vet visit", duration=45, priority=9, category="health", frequency="once")

    new_task = scheduler.mark_task_complete(task, pet)

    assert task.completed is True
    assert new_task is None
    assert len(pet.tasks) == 0


def test_mark_task_complete_daily_without_due_date_uses_next_day():
    """Ensure daily recurrence still works when the completed task has no due date."""
    scheduler = Scheduler()
    pet = Pet("Mochi", "cat", 2)
    task = Task("Dinner", duration=10, priority=8, category="feeding", frequency="daily", due_date=None)

    before = date.today()
    new_task = scheduler.mark_task_complete(task, pet)
    after = date.today()

    assert new_task is not None
    assert before + timedelta(days=1) <= new_task.due_date <= after + timedelta(days=1)


def test_detect_conflicts_flags_overlapping_tasks_same_day():
    """Ensure detect_conflicts reports overlaps for tasks on the same date/time window."""
    owner = Owner("Hafsa", available_time=120)
    dog = Pet("Buddy", "dog", 3)
    owner.add_pet(dog)
    scheduler = Scheduler()

    dog.add_task(
        Task(
            "Walk",
            duration=30,
            priority=6,
            category="exercise",
            due_date=date(2026, 3, 29),
            start_time=time(9, 0),
        )
    )
    dog.add_task(
        Task(
            "Feeding",
            duration=20,
            priority=7,
            category="feeding",
            due_date=date(2026, 3, 29),
            start_time=time(9, 15),
        )
    )

    warnings = scheduler.detect_conflicts(owner)

    assert len(warnings) == 1
    assert "overlaps" in warnings[0]


def test_detect_conflicts_flags_duplicate_start_times():
    """Ensure detect_conflicts flags tasks scheduled at the exact same start time."""
    owner = Owner("Hafsa", available_time=120)
    pet = Pet("Mochi", "cat", 2)
    owner.add_pet(pet)
    scheduler = Scheduler()

    pet.add_task(
        Task(
            "Feed",
            duration=15,
            priority=7,
            category="feeding",
            due_date=date(2026, 3, 29),
            start_time=time(9, 0),
        )
    )
    pet.add_task(
        Task(
            "Medication",
            duration=10,
            priority=9,
            category="health",
            due_date=date(2026, 3, 29),
            start_time=time(9, 0),
        )
    )

    warnings = scheduler.detect_conflicts(owner)

    assert len(warnings) == 1
    assert "overlaps" in warnings[0]


def test_detect_conflicts_does_not_flag_adjacent_tasks():
    """Ensure back-to-back tasks are not treated as overlapping conflicts."""
    owner = Owner("Hafsa", available_time=120)
    cat = Pet("Mochi", "cat", 2)
    owner.add_pet(cat)
    scheduler = Scheduler()

    cat.add_task(
        Task(
            "Play",
            duration=30,
            priority=6,
            category="exercise",
            due_date=date(2026, 3, 29),
            start_time=time(10, 0),
        )
    )
    cat.add_task(
        Task(
            "Brush",
            duration=15,
            priority=5,
            category="grooming",
            due_date=date(2026, 3, 29),
            start_time=time(10, 30),
        )
    )

    warnings = scheduler.detect_conflicts(owner)

    assert warnings == []


def test_detect_conflicts_skips_unscheduled_tasks():
    """Ensure tasks missing start_time or due_date are ignored by conflict detection."""
    owner = Owner("Hafsa", available_time=120)
    pet = Pet("Buddy", "dog", 3)
    owner.add_pet(pet)
    scheduler = Scheduler()

    pet.add_task(Task("No time", duration=20, priority=4, category="health", due_date=date(2026, 3, 29), start_time=None))
    pet.add_task(Task("No date", duration=20, priority=4, category="health", due_date=None, start_time=time(11, 0)))

    warnings = scheduler.detect_conflicts(owner)

    assert warnings == []