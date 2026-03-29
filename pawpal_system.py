class Task:
    """Represents a single pet care activity."""

    def __init__(self, title, duration, priority, category, description="", frequency="daily"):
        self.title = title
        self.description = description   # what the task involves
        self.duration = duration         # estimated time in minutes
        self.frequency = frequency       # e.g. "daily", "weekly", "as-needed"
        self.priority = priority         # 1–10 scale (10 = most urgent)
        self.category = category         # e.g. "feeding", "exercise", "grooming"
        self.completed = False           # completion status

    def mark_complete(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False

    def is_high_priority(self):
        return self.priority > 7

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return (f"[{status}] {self.title} ({self.category}) | "
                f"Priority: {self.priority} | Duration: {self.duration}min | "
                f"Frequency: {self.frequency}")


class Pet:
    """Stores pet details and its list of care tasks."""

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []   # list of Task objects belonging to this pet

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_title):
        self.tasks = [t for t in self.tasks if t.title != task_title]

    def get_pending_tasks(self):
        """Return only tasks that haven't been completed yet."""
        return [t for t in self.tasks if not t.completed]

    def get_care_profile(self):
        return f"{self.name} ({self.species}), Age: {self.age}, Tasks: {len(self.tasks)}"

    def __str__(self):
        return self.get_care_profile()


class Owner:
    """Manages multiple pets and provides unified access to all their tasks."""

    def __init__(self, name, available_time):
        self.name = name
        self.available_time = available_time   # total minutes available today
        self.pets = []                         # list of Pet objects

    def add_pet(self, pet):
        self.pets.append(pet)

    def remove_pet(self, pet_name):
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
