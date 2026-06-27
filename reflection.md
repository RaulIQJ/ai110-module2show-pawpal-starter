# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    - Need to design a pet class that can contain all of the pets attributes and all the goals we want to accomplish. Also creating another class that will hold on the constriaints priorities and needs that we want to accomplish so the goals. One last class that will take in the pet and the constraints to and all the needed info to design a plan.
- What classes did you include, and what responsibilities did you assign to each?
    - I have thought about using a pet class the holds the responsibilty of putting all the pet's info into this and being able to track it's description and attributes. Another class would be Goals and Constraints, in here I want to keep track of all the constraints that are placed on that day. Than being able to have all the constraints also add the priorities and minimums of what should be done or what is wanted to get done. This would be likr goals or something that is needed to get done. Also adding a schedule class that would take in a pet object and constraints object that correspond to each other. Takin care of planning out the day, so taking in constraints, the pet and what can be done in that day and returning it. Lastly adding an Owner's class that holds information on the owner. Whether this may be something more aobut the descroption and attributes of the owner and the goals od the owner is what it would hold. 

**b. Design changes**

- Did your design change during implementation?
    - During the implementation my design did chage.
- If yes, describe at least one change and why you made it.
    - During my initial design I had a larger idea of adding multiple classes and subclasses to all account for different things. Inside of my Tasks class I wanted to make a subclass, that would track the state of a task was it done, pending, or not started. I asked the AI and it instead suggested to make it an Enum which would make it much easier to keep track of state of tasks. As I continued going through my tasks I asked for missing relationships and one of the biggest ideas i had forgotten was owners could have multiple pets. I did not take this into account and the AI pointed it out and helped me implement. At first I thought to only allow one pet per owner rather than a list of pets for the owner. I changed this to allow for multiple pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - My scheduler currently considers the owner's daily time budget, each task's priority (High/Medium/Low), and each task's start time ("HH:MM"). Priority decides what gets into the plan, the time budget decides how much fits, and start time orders the final plan and helps to flag overlapping tasks as conflicts.
- How did you decide which constraints mattered most?
    - Priority is what mattered most, on any given day the circumstances can always change. One day can be busier than the other but some tasks might be more important to get done. In some cases medicine might be something of HIGH priority that needs to get down and this could be placed later into the day and completley missed or forgotten. But with priority as the most important factor it is placed into the top tasks to look at before going onto lower priority tasks like enrichments. Next was time, because an owner only has so much time in a day, and placing to many tasks, will go over the amount of time and mess up their other plans. Using priority and time budget allow to cut down and trim the schedule to fit what matters most.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - One tradeoff my scheduler makes is it takes tasks in priority order and keeps each one if it still fits in the remaning budget, otherwise skips it. It does not seatch for the combination of best tasks, to get the most things done, but rather looks for the most important and what fits in the time budget.
- Why is that tradeoff reasonable for this scenario?
    - Why it's reasonable in this case is because it is simple, fast, and easy to explain to the owner. It takes in the tasks that fit into the schedule based on priority, and explains the most important tasks were scheduled first, until there was not time left for other tasks. Which matters more rather than a mathematically optimal plan, that aims to fit the most tasks possible instead of what may be important. Also warning instead of auto resolving conflicts allows the user to stay in control and add or remove whatever tasks are deemed more important.


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
