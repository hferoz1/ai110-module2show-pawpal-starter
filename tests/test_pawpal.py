import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pawpal_system import Pet, Task

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