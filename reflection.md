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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
