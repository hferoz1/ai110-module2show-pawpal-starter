from datetime import date, timedelta


class Task:
    """Represents a single pet care activity."""

    def __init__(self, title, duration, priority, category, description="", frequency="daily", due_date=None, start_time=None):
        """
        Initialize a Task with scheduling and priority metadata.

        Args:
            title:       short name for the care activity
            duration:    estimated time in minutes
            priority:    integer 1–10 (higher = more urgent)
            category:    activity type, e.g. 'feeding', 'grooming', 'exercise'
            description: optional longer description (default "")
            frequency:   recurrence cadence — 'daily', 'weekly', or 'once' (default 'daily')
            due_date:    date the task is due, or None if unscheduled
            start_time:  datetime.time for the planned start, or None
        """
        self.title = title
        self.description = description
        self.duration = duration
        self.frequency = frequency
        self.priority = priority
        self.category = category
        self.completed = False
        self.due_date = due_date
        self.start_time = start_time

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Reset this task to pending (not yet completed)."""
        self.completed = False

    def is_high_priority(self):
        """Return True if priority is greater than 7, False otherwise."""
        return self.priority > 7

    def __str__(self):
        """Return a single-line human-readable summary of the task."""
        status = "Done" if self.completed else "Pending"
        due = f" | Due: {self.due_date}" if self.due_date else ""
        start = f" | Start: {self.start_time.strftime('%H:%M')}" if self.start_time else ""
        return (f"[{status}] {self.title} ({self.category}) | "
                f"Priority: {self.priority} | Duration: {self.duration}min | "
                f"Frequency: {self.frequency}{due}{start}")
class Pet:
    """Stores pet details and its list of care tasks."""

    def __init__(self, name, species, age):
        """
        Initialize a Pet with identifying information and an empty task list.

        Args:
            name:    the pet's name
            species: species or breed, e.g. 'dog', 'cat'
            age:     age in years
        """
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []   # list of Task objects belonging to this pet

    def add_task(self, task):
        """Append a Task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_title):
        """Remove all tasks whose title matches task_title."""
        self.tasks = [t for t in self.tasks if t.title != task_title]

    def get_pending_tasks(self):
        """Return only tasks that haven't been completed yet."""
        return [t for t in self.tasks if not t.completed]

    def get_care_profile(self):
        """Return a concise summary string: name, species, age, and task count."""
        return f"{self.name} ({self.species}), Age: {self.age}, Tasks: {len(self.tasks)}"

    def __str__(self):
        """Return the pet's care profile as a string."""
        return self.get_care_profile()


class Owner:
    """Manages multiple pets and provides unified access to all their tasks."""

    def __init__(self, name, available_time):
        """
        Initialize an Owner with a name and daily time budget.

        Args:
            name:           the owner's name
            available_time: total minutes the owner can spend on pet care today
        """
        self.name = name
        self.available_time = available_time   # total minutes available today
        self.pets = []                         # list of Pet objects

    def add_pet(self, pet):
        """Add a Pet to this owner's roster."""
        self.pets.append(pet)

    def remove_pet(self, pet_name):
        """Remove the pet whose name matches pet_name from the roster."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_pet(self, pet_name):
        """Return a specific pet by name, or None if not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self):
        """Collect and return every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pending_tasks(self):
        """Return all incomplete tasks across every pet."""
        return [t for t in self.get_all_tasks() if not t.completed]

    def __str__(self):
        """Return a one-line summary of the owner, their pet count, and available time."""
        return f"Owner: {self.name} | Pets: {len(self.pets)} | Available time: {self.available_time}min"


class Scheduler:
    """The 'Brain' — retrieves, organizes, and manages tasks across all of an owner's pets."""

    # --- retrieval helpers ---

    def get_all_tasks(self, owner):
        """Ask the owner for every task across all pets."""
        return owner.get_all_tasks()

    def get_pending_tasks(self, owner):
        """Return only incomplete tasks across all pets."""
        return owner.get_pending_tasks()

    def filter_tasks(self, owner, completed=None, pet_name=None):
        """
        Filter tasks by completion status and/or pet name.

        Args:
            owner:      the Owner whose tasks to search
            completed:  True → only completed, False → only pending,
                        None → both (no filter)
            pet_name:   name of a specific pet to filter by,
                        or None to include all pets
        Returns:
            list of Task objects matching all supplied criteria
        """
        results = []
        for pet in owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def get_tasks_by_category(self, owner, category):
        """Filter all tasks down to a specific category (e.g. 'feeding')."""
        return [t for t in self.get_all_tasks(owner) if t.category == category]

    def get_high_priority_tasks(self, owner):
        """Return tasks with priority > 7 across all pets."""
        return [t for t in self.get_all_tasks(owner) if t.is_high_priority()]

    # --- organisation ---

    def rank_tasks(self, tasks):
        """Sort tasks from highest to lowest priority."""
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def sort_by_time(self, tasks):
        """Sort tasks by their time attribute in HH:MM format."""
        return sorted(tasks, key=lambda t: t.duration)

    # --- planning ---

    def generate_plan(self, owner):
        """
        Build a time-boxed daily plan from the owner's pending tasks.

        Selects as many high-priority pending tasks as possible without
        exceeding the owner's available time.
        Returns the list of scheduled tasks and total minutes used.
        """
        pending = self.get_pending_tasks(owner)
        ranked = self.rank_tasks(pending)

        plan = []
        time_used = 0

        for task in ranked:
            if time_used + task.duration <= owner.available_time:
                plan.append(task)
                time_used += task.duration

        return plan, time_used

    def print_plan(self, owner):
        """Print a formatted daily care plan for the owner."""
        plan, time_used = self.generate_plan(owner)
        print(f"\n=== Daily Plan for {owner.name} ===")
        print(f"Available time: {owner.available_time}min | Scheduled: {time_used}min\n")
        if not plan:
            print("No tasks scheduled.")
        for i, task in enumerate(plan, 1):
            print(f"  {i}. {task}")
        print()

    def mark_task_complete(self, task, pet):
        """
        Mark a task complete and, for recurring tasks, add a new instance
        to the pet's task list with the next due date.

        Args:
            task: the Task to mark complete
            pet:  the Pet that owns the task
        Returns:
            the newly created Task, or None if no recurrence
        """
        task.mark_complete()

        if task.frequency == "daily":
            base_date = task.due_date if task.due_date is not None else date.today()
            next_due = base_date + timedelta(days=1)
        elif task.frequency == "weekly":
            base_date = task.due_date if task.due_date is not None else date.today()
            next_due = base_date + timedelta(weeks=1)
        else:
            return None

        new_task = Task(
            title=task.title,
            duration=task.duration,
            priority=task.priority,
            category=task.category,
            description=task.description,
            frequency=task.frequency,
            due_date=next_due,
        )
        pet.add_task(new_task)
        return new_task

    def detect_conflicts(self, owner):
        """
        Check whether any two scheduled tasks overlap in time.

        Lightweight strategy: represent each task's window as
        [start_minutes, end_minutes) using minutes-since-midnight integers,
        then check every pair for overlap on the same due_date.
        Tasks without a start_time or due_date are skipped.

        Returns:
            list of warning strings (empty list = no conflicts)
        """
        # Build a flat list of (pet_name, task) for tasks that are schedulable
        scheduled = []
        for pet in owner.pets:
            for task in pet.tasks:
                if task.start_time is not None and task.due_date is not None:
                    scheduled.append((pet.name, task))

        warnings = []
        for i in range(len(scheduled)):
            for j in range(i + 1, len(scheduled)):
                pet_a, task_a = scheduled[i]
                pet_b, task_b = scheduled[j]

                # Only compare tasks on the same day
                if task_a.due_date != task_b.due_date:
                    continue

                # Convert to minutes-since-midnight
                a_start = task_a.start_time.hour * 60 + task_a.start_time.minute
                a_end   = a_start + task_a.duration
                b_start = task_b.start_time.hour * 60 + task_b.start_time.minute
                b_end   = b_start + task_b.duration

                # Overlap when one window starts before the other ends
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"WARNING: '{task_a.title}' ({pet_a}, "
                        f"{task_a.start_time.strftime('%H:%M')}–"
                        f"{divmod(a_end, 60)[0]:02d}:{divmod(a_end, 60)[1]:02d}) "
                        f"overlaps with '{task_b.title}' ({pet_b}, "
                        f"{task_b.start_time.strftime('%H:%M')}–"
                        f"{divmod(b_end, 60)[0]:02d}:{divmod(b_end, 60)[1]:02d}) "
                        f"on {task_a.due_date}"
                    )

        return warnings
