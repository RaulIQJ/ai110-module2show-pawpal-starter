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
