class Owner:
    def __init__(self, name, available_time):
        self.name = name
        self.available_time = available_time
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def remove_task(self, task_name):
        self.tasks = [t for t in self.tasks if t.title != task_name]


class Pet:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
    
    def get_care_profile(self):
        return f"{self.name} ({self.species}), Age: {self.age}"


class Task:
    def __init__(self, title, duration, priority, category):
        self.title = title
        self.duration = duration
        self.priority = priority
        self.category = category
    
    def is_high_priority(self):
        return self.priority > 7


class Scheduler:
    def rank_tasks(self, tasks):
        return sorted(tasks, key=lambda t: t.priority, reverse=True)
    
    def generate_plan(self, available_time, tasks):
        ranked = self.rank_tasks(tasks)
        plan = []
        time_used = 0
        
        for task in ranked:
            if time_used + task.duration <= available_time:
                plan.append(task)
                time_used += task.duration
        
        return plan