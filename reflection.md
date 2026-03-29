# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
ANSWER: My initial UML design centered on a pet care app with four classes: Owner, Pet, Task, and Scheduler. The model connected them so one Owner has one Pet and a list of Task objects, while Scheduler consumes the owner's time budget and tasks to produce a daily care plan.
- What classes did you include, and what responsibilities did you assign to each?
ANSWER: Owner stores the user's name, available time, and task list. Pet stores identity and profile fields (name, species, age) used for care context. Task represents each care activity with duration, priority, and category metadata. Scheduler is responsible for ranking tasks and generating a feasible plan that stays within available time.

**b. Design changes**

- Did your design change during implementation?
ANSWER: Yes. After asking Copilot to review #file:pawpal_system.py for missing relationships and logic bottlenecks, I made targeted design changes.
- If yes, describe at least one change and why you made it.
ANSWER: I updated the design to make the Owner-to-Pet relationship explicit in the class model, since the skeleton code currently tracks tasks under Owner but does not directly store a pet reference. I also refined Scheduler ranking rules to include tie-breaking (for example, favoring shorter tasks when priorities match) because the current greedy priority-first approach can create less efficient daily plans. These changes improve model clarity and reduce scheduling bottlenecks without making the system much more complex.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
ANSWER: My scheduler considers the owner's available time, task priority, and task duration as constraints. It also factors in task categories (like feeding or exercise) to ensure a balanced daily plan.
- How did you decide which constraints mattered most?
ANSWER: I prioritized time and task priority as the most critical constraints because they directly impact the feasibility and quality of the daily care plan. Time is a hard constraint since the owner cannot exceed their available hours, while priority helps ensure that the most important tasks are scheduled first. Preferences and categories were secondary but still influenced task selection to create a more personalized and effective care routine.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
ANSWER: One tradeoff my scheduler makes is that it uses a greedy approach to select tasks based on priority and duration, which can lead to suboptimal plans in certain scenarios (for example, if a high-priority task is very long and consumes most of the available time, leaving no room for other important tasks). This tradeoff was made to keep the scheduling logic simple and efficient, as implementing a more complex optimization algorithm would require significantly more development time and computational resources.
- Why is that tradeoff reasonable for this scenario?
ANSWER: This tradeoff is reasonable for the PawPal+ scenario because pet care tasks often have clear priorities (like feeding and medication) that should be addressed first, and the owner's time constraints are a hard limit. While the greedy approach may not always yield the optimal schedule, it provides a practical solution that can be implemented quickly and still meets the core needs of the user. Additionally, the app can be iteratively improved in future versions to incorporate more sophisticated scheduling algorithms if needed.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
ANSWER: I used AI tools primarily for design brainstorming and code review. I asked Copilot to analyze my initial UML design and suggest improvements, which helped me identify missing relationships and potential bottlenecks in the scheduling logic. I also used AI to generate test cases and refactor code for better readability and maintainability.
- What kinds of prompts or questions were most helpful?
ANSWER: Prompts that asked for specific feedback on my UML design, such as "What relationships are missing in this class diagram?" or "How can I improve the scheduling logic to handle edge cases?" were particularly helpful. Additionally, prompts that requested code snippets for common patterns (like sorting tasks by priority) or test case generation were valuable for accelerating development and ensuring code quality.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
ANSWER: There was a moment when Copilot suggested a scheduling algorithm that prioritized tasks solely based on their duration, which I felt would not align well with the user's needs since it could lead to important but longer tasks being consistently deprioritized. Instead of accepting this suggestion, I modified the algorithm to first sort tasks by priority and then use duration as a tiebreaker, ensuring that critical tasks are scheduled while still considering efficiency.
- How did you evaluate or verify what the AI suggested?
ANSWER: I evaluated the AI's suggestions by considering the user experience and the core requirements of the app. I also ran tests to verify that the scheduling logic produced reasonable plans under various scenarios, such as when multiple high-priority tasks were present or when the available time was limited. By comparing the AI's suggestions against my understanding of the problem and testing outcomes, I was able to make informed decisions about which suggestions to implement and which to modify.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
ANSWER: I tested several key behaviors of the scheduler, including:
Task completion state updates: ensuring that marking a task as complete correctly updates its status and rollss over recurring tasks.
Adding tasks to pets: verifying that tasks can be added to pets and that they are correctly associated with the pet's profile.
Priority sorting correctness: confirming that tasks are sorted by priority in the generated plan.
Chronological sorting correctness: ensuring that tasks with start times are sorted correctly in the daily plan.
Daily plan generation: testing that the generated plan respects the owner's available time and includes the highest priority tasks possible.
- Why were these tests important?
ANSWER: These tests were important because they validate the core features of the app that directly impact the user experience. If tasks cannot be added or marked complete correctly, or if the scheduling logic fails to produce a reasonable plan, the app would not serve its intended purpose. By testing these behaviors, I can ensure that the app is functional and provides value to pet owners, ultimately leading to better care for their pets.

**b. Confidence**

- How confident are you that your scheduler works correctly?
ANSWER: I am reasonably confident that my scheduler works correctly for the tested scenarios, as the tests cover a range of important behaviors and edge cases. However, I recognize that there may still be untested scenarios or edge cases that could reveal bugs or limitations in the scheduling logic. Therefore, while I believe the core functionality is solid, I would want to conduct further testing and gather user feedback to identify any additional issues or areas for improvement.
- What edge cases would you test next if you had more time?
ANSWER: If I had more time, I would test edge cases such as:

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
ANSWER: I am most satisfied with the overall design and implementation of the scheduling logic. The Scheduler class effectively balances task priorities and time constraints to generate a feasible daily plan, which is the core functionality of the app. Additionally, I am pleased with how the AI tools helped me refine my design and identify potential issues early in the development process, leading to a more robust and user-friendly application.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
ANSWER: If I had another iteration, I would improve the scheduling algorithm to handle more complex scenarios, such as tasks with dependencies (e.g., a pet must be fed before going for a walk) or incorporating user preferences for certain task categories. I would also redesign the UI to provide more interactive features, such as allowing users to drag and drop tasks in the schedule or providing visual indicators of task importance and time requirements. Additionally, I would implement more comprehensive testing to cover a wider range of edge cases and ensure the app's robustness in various real-world scenarios.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
ANSWER: One important thing I learned about designing systems and working with AI on this project is the value of iterative design and feedback. By starting with a clear UML design and then using AI tools to review and refine that design, I was able to identify potential issues and make informed decisions about how to improve the system. This iterative process allowed me to create a more effective and user-friendly application while also gaining insights into how AI can augment human creativity and problem-solving in software development.