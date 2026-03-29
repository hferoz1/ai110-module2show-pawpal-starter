from pawpal_system import Owner, Pet, Task

# Create an owner
owner = Owner("Alice", 120)

# Create pets
pet1 = Pet("Buddy", "Dog", owner)
pet2 = Pet("Whiskers", "Cat", owner)

# Add tasks with different times
task1 = Task("Feeding", 15, 8, "feeding")
task2 = Task("Walking", 30, 7, "exercise")
task3 = Task("Playtime", 20, 6, "enrichment")

pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)

# Print today's schedule
print("Today's Schedule")
print("=" * 50)
print(f"Owner: {owner.name}\n")

for pet in [pet1, pet2]:
    print(f"{pet.name} ({pet.species}):")
    for task in pet.tasks:
        print(f"  - {task.title} ({task.category}, {task.duration} min)")
    print()