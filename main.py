from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner("Alice", 120)
scheduler = Scheduler()

pet1 = Pet("Buddy", "Dog", 3)
pet2 = Pet("Whiskers", "Cat", 2)
owner.add_pet(pet1)
owner.add_pet(pet2)

# Tasks added out of order (low priority first, then high)
pet1.add_task(Task("Bath time",    25, 3, "grooming"))
pet1.add_task(Task("Walking",      30, 9, "exercise",  due_date=date.today()))
pet1.add_task(Task("Feeding",      15, 8, "feeding"))
pet1.add_task(Task("Vet check-up", 60, 5, "health"))

pet2.add_task(Task("Playtime",     20, 6, "enrichment"))
pet2.add_task(Task("Nail trim",    10, 2, "grooming",  frequency="weekly", due_date=date.today()))
pet2.add_task(Task("Feeding",      10, 9, "feeding"))

# Mark a couple tasks complete to test filtering
pet1.tasks[0].mark_complete()   # Bath time -> done
pet2.tasks[2].mark_complete()   # Whiskers' Feeding -> done


def print_tasks(label, tasks):
    """
    Print a labelled, formatted list of tasks to stdout.

    Args:
        label: heading string displayed above the task list
        tasks: iterable of Task objects to display; prints '(none)' if empty
    """
    print(f"\n{label}")
    print("-" * 50)
    if not tasks:
        print("  (none)")
    for t in tasks:
        print(f"  {t}")


# --- Sort by priority (high → low) ---
all_tasks = scheduler.get_all_tasks(owner)
print_tasks("All tasks sorted by priority (high → low):",
            scheduler.rank_tasks(all_tasks))

# --- Sort by duration (short → long) ---
print_tasks("All tasks sorted by duration (short → long):",
            scheduler.sort_by_time(all_tasks))

# --- Filter: pending tasks only ---
print_tasks("Pending tasks (all pets):",
            scheduler.filter_tasks(owner, completed=False))

# --- Filter: completed tasks only ---
print_tasks("Completed tasks (all pets):",
            scheduler.filter_tasks(owner, completed=True))

# --- Filter: all tasks for Buddy ---
print_tasks("All tasks for Buddy:",
            scheduler.filter_tasks(owner, pet_name="Buddy"))

# --- Filter: pending tasks for Whiskers ---
print_tasks("Pending tasks for Whiskers:",
            scheduler.filter_tasks(owner, completed=False, pet_name="Whiskers"))

# --- Daily plan ---
scheduler.print_plan(owner)

# --- mark_task_complete demo ---
daily_task  = pet1.tasks[1]   # Buddy's Walking (daily, due today)
weekly_task = pet2.tasks[1]   # Whiskers' Nail trim (weekly, due today)

print("=== mark_task_complete demo ===\n")
print(f"Completing daily task:  {daily_task}")
new_daily = scheduler.mark_task_complete(daily_task, pet1)
print(f"  -> New task created:  {new_daily}\n")

print(f"Completing weekly task: {weekly_task}")
new_weekly = scheduler.mark_task_complete(weekly_task, pet2)
print(f"  -> New task created:  {new_weekly}\n")

print_tasks("Buddy's tasks after completion:", pet1.tasks)
print_tasks("Whiskers' tasks after completion:", pet2.tasks)

# --- Conflict detection demo ---
# Create a fresh owner with tasks that have explicit start times
owner2 = Owner("Bob", 180)
dog = Pet("Rex", "Dog", 4)
cat = Pet("Luna", "Cat", 1)
owner2.add_pet(dog)
owner2.add_pet(cat)

today = date.today()

# Rex: Walk 09:00–09:30, Feeding 09:15–09:30  <-- overlap with Walk
# Luna: Grooming 09:20–09:50                  <-- overlap with Walk and Feeding
# Rex: Vet check-up 11:00–12:00               <-- no conflict
dog.add_task(Task("Walking",      30, 9, "exercise",    due_date=today, start_time=time(9, 0)))
dog.add_task(Task("Feeding",      15, 8, "feeding",     due_date=today, start_time=time(9, 15)))
cat.add_task(Task("Grooming",     30, 5, "grooming",    due_date=today, start_time=time(9, 20)))
dog.add_task(Task("Vet check-up", 60, 7, "health",      due_date=today, start_time=time(11, 0)))

print("\n=== Conflict Detection Demo ===\n")
print("Scheduled tasks:")
for pet in [dog, cat]:
    for task in pet.tasks:
        print(f"  [{pet.name}] {task}")

conflicts = scheduler.detect_conflicts(owner2)
print()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts detected.")
