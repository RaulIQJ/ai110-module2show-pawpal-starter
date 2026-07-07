# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    - Need to design a pet class that can contain all of the pets attributes and all the goals we want to accomplish. Also creating another class that will hold on the constraints priorities and needs that we want to accomplish so the goals. One last class that will take in the pet and the constraints to and all the needed info to design a plan.
- What classes did you include, and what responsibilities did you assign to each?
    - I have thought about using a pet class that holds the responsibility of putting all the pet's info into this and being able to track its description and attributes. Another class would be Goals and Constraints, in here I want to keep track of all the constraints that are placed on that day. Then being able to have all the constraints also add the priorities and minimums of what should be done or what is wanted to get done. This would be like goals or something that is needed to get done. Also adding a schedule class that would take in a pet object and constraints object that correspond to each other. Taking care of planning out the day, so taking in constraints, the pet and what can be done in that day and returning it. Lastly adding an Owner's class that holds information on the owner. Whether this may be something more about the description and attributes of the owner and the goals of the owner is what it would hold.

**b. Design changes**

- Did your design change during implementation?
    - During the implementation my design did change.
- If yes, describe at least one change and why you made it.
    - During my initial design I had a larger idea of adding multiple classes and subclasses to all account for different things. Inside of my Tasks class I wanted to make a subclass, that would track the state of a task was it done, pending, or not started. I asked the AI and it instead suggested to make it an Enum which would make it much easier to keep track of state of tasks. As I continued going through my tasks I asked for missing relationships and one of the biggest ideas I had forgotten was owners could have multiple pets. I did not take this into account and the AI pointed it out and helped me implement. At first I thought to only allow one pet per owner rather than a list of pets for the owner. I changed this to allow for multiple pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - My scheduler currently considers the owner's daily time budget, each task's priority (High/Medium/Low), and each task's start time ("HH:MM"). Priority decides what gets into the plan, the time budget decides how much fits, and start time orders the final plan and helps to flag overlapping tasks as conflicts.
- How did you decide which constraints mattered most?
    - Priority is what mattered most, on any given day the circumstances can always change. One day can be busier than the other but some tasks might be more important to get done. In some cases medicine might be something of HIGH priority that needs to get done and this could be placed later into the day and completely missed or forgotten. But with priority as the most important factor it is placed into the top tasks to look at before going onto lower priority tasks like enrichments. Next was time, because an owner only has so much time in a day, and placing too many tasks, will go over the amount of time and mess up their other plans. Using priority and time budget allow to cut down and trim the schedule to fit what matters most.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - One tradeoff my scheduler makes is it takes tasks in priority order and keeps each one if it still fits in the remaining budget, otherwise skips it. It does not search for the combination of best tasks, to get the most things done, but rather looks for the most important and what fits in the time budget.
- Why is that tradeoff reasonable for this scenario?
    - Why it's reasonable in this case is because it is simple, fast, and easy to explain to the owner. It takes in the tasks that fit into the schedule based on priority, and explains the most important tasks were scheduled first, until there was not time left for other tasks. Which matters more rather than a mathematically optimal plan, that aims to fit the most tasks possible instead of what may be important. Also warning instead of auto resolving conflicts allows the user to stay in control and add or remove whatever tasks are deemed more important.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI tools during this project to help me brainstorm the UML classes, generating the skeletons, implementing the scheduling logic in small increments, and reviewing my code as I moved through each phase. There were times I would ask for it to read my logic to me and point out any issues or logic that failed explain why it won't work and what would be a better implementation. It then helped me edit my designs and form a better structure.
- What kinds of prompts or questions were most helpful?
    - What I found most helpful was using prompts to explain logic back to me. If there were lines that were built and generated that I did not understand I would ask for it to read it and explain the logic. This was incredibly useful to become familiar with new code and libraries like Streamlit which I have not used before. Another question that was incredibly useful was for it to point out holes in my logic and what would work, how I can improve it and provide opinions on my ideas.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - One time I did not accept an AI suggestion as is was when I was rewriting my app.py logic. There were buttons and lines that I would instead go line by line through in order to find the bug and errors I found when my buttons would not work on the page, the logic was there but when it came to using them it wouldn't work. So instead of just reworking it all I went step by step. In order to break the problem up and commit small changes to not lose all progress and have a checkpoint that holds previous lines.
- How did you evaluate or verify what the AI suggested?
    - To evaluate or verify what AI suggested I would go and use the automated test as a form of testing to see that the functions and core logic work. If these test cases all ran and passed this meant that nothing was broken in the logic, so I used streamlit to further verify that the edits made and suggested worked. Whether that was making a new pet and adding tasks to verify the conflicting logic I would use the test cases and streamlit.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - I tested the following behaviors:
    - sorting by priority (HIGH→LOW, ties by shorter duration) and by time;
    - fits_in_time staying within budget; make_schedule combining all pets' tasks,
    - ordering by priority, respecting the budget, and skipping DONE tasks; task/pet
    - ownership (mark_done, task_count, list_tasks aggregation); filtering by status
    - and pet; conflict detection (overlaps flagged, back-to-back not flagged); and
    - recurrence (daily → next day, weekly → next week, one-off does not recur, and the
    - new occurrence is attached to the pet).
- Why were these tests important?
    - These tests were important because they are the "brain" of the app and any silent bug here would produce a wrong daily plan, not handle proper time conflicts, and create many errors without crashing. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - Confidence 4/5
- What edge cases would you test next if you had more time?
    I tested edge cases like empty task lists and back-to-back times, to verify that the time conflicts would display correctly. I also tested tasks scheduled near midnight, tasks with no start_time appearing in a schedule, weekly recurrence, conflicts and the UI interactions on Streamlit UI.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - I'm most satisfied with the algorithmic layer the sorting, filtering, conflict detection, and daily/weekly occurrences. This was something very interesting to see built and working with streamlit and although it was a bit tricky and catching the streamlit "copy of a selected object" bug it all brought a lot of learning and was a win.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - If I had another iteration I'd improve the scheduler beyond the greedy priority-first pass. Instead filtering the tasks on importance and being able to fit tasks in a more timely manner. Also possibly adding more features for the UI to look more personalized to the user and have more detail would be fun.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - I learned that the "lead architect" matters. AI can move fast, but I had to step in to own the design and decisions think for myself and plan out what I want to build. Verify its output instead of just trusting it and making sure that it all makes sense when running through the logic. AI is a powerful tool that can speed up the process. But I had to verify it all worked. Adding tasks or tests in small phases helped control all the work flow and make the code less bug prone.