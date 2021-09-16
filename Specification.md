### Git Hub Repository

https://github.com/anhquangsjsu/team3_cs131

### Team members:

Quang - anhquangsjsu

Jason - jasonofiana

Kim - kimnguyen4497

### Product name: 

Unforgettable

### Use cases name:

##### Memorizing:

Import file and convert to flashcards

Share flashcards (add to their account)

Create pdf of flash cards to print

Sort flashcards by names

Organize flash/cards into sections/topics (folders).

##### Notes:

Add a new empty note 

Convert markdown notes to pdf

Share notes with other people (add to their account)

Add lock to the note ( enter password to unlock)

Search for words or phrases in a note ( list note name, for each name will tell the positions of the matches)

##### Time Management:

View time spent on tasks in a day

Add a task to the Pomodoro timer 

Change order of tasks in the timer

Start the timer

Edit a task 

#### Use Case Description:

##### Date: 

9/12/2021

##### Product Name: 

Unforgettable

##### Problem Statement: 

Studying and working effectively require proper methods. Unforgettable would be able to provide such methods by providing Memorization, Notes and Time Management features to help individual enhance productivities via memory enhancement, scheduling and storing valuable information.

##### Non-functional Requirements:

1. Display properly among browsers
2. Responsively display in different window sizes
3. Loading time between features should be under 2 seconds

##### **Use Case Name:** View time spent on tasks in a day

###### **Summary**

Users can see how many hours they spent on a day for their tasks

###### **Actors**

User

###### **Preconditions**

Users need to do at least one task using the timer

###### **Trigger**

User click on the &quot;Time Analysis&quot; button

###### **Primary Sequence**

1. Systems prompt user options &quot;By day&quot;, &quot;By Tasks&quot;, or &quot;By Month&quot;
2. Users choose &quot;By day&quot;.
3. The system displays a list of days the user has done tasks on with hours spent displayed on the Day UI
4. User choose a specific day
5. The system displays a graph with hours spent on each task

###### **Primary Postcondition**

User retrieved the time analysis in chart form from the system based on their choice of day

###### **Alternate Sequences**

2. The user did not do any task yet

3. System displays &quot;No task added&quot;

##### **Use Case Name:** add a task to the Pomodoro timer

###### **Summary**

Users can add a task to a Pomodoro timer to start the countdown

###### **Actors**

User

###### **Preconditions**

###### **Trigger**

User click &quot;Add a task&quot; in the Time Management view

###### **Primary Sequence**

1. The System asks the user to enter the name of the task
2. User enter the task name
3. The system prompts the user to enter the duration of the task
4. The User enters the duration
5. The system prompts the user to enter break duration
6. The user enters break duration
7. User click &quot;Add&quot; to add the task to the timer

###### **Primary Postcondition**

The user owns a task in their agenda and is ready to start the timer

##### **Use Case Name:** start the timer

###### **Summary**

After adding a task to the timer, the user can start the timer to start working on those tasks

###### **Actors**

User

###### **Preconditions**

User must have at least one task added to the timer

###### **Trigger**

User select &quot;Start timer&quot;

###### **Primary Sequence**

1. System start countdown timer for the first task
2. The system reached the end time then notify the user of the end of the task
3. System start countdown timer for the break
4. The system notifies the end of the break when the timer reached 0 and start the countdown for the next task

###### **Primary Postcondition**

User will have all the tasks associated with the timer finished, which will be saved to the finished tasks section

###### **Alternate Trigger**

User click &quot;Stop

###### **Alternate Sequences**

2. User click &quot;stop&quot; before the timer ended

3. The system stops the timer
4. The system displays the &quot;Resume&quot; button
5. User click &quot;resume&quot;
6. The system continues the countdown timer

**Alternate Postconditions**

The timer will be on hold until the user resume

The task is masked as unfinished until the timer finishes

##### **Use Case Name:** Change the order of the tasks in the timer

###### **Summary**

After adding tasks to the timer, the user can swap the tasks within

###### **Actors**

User

###### **Preconditions**

Must be at least one task added to the user

###### **Trigger**

User selects &quot;Selection mode&quot;

###### **Primary Sequence**

1. The system indicates that the user entered the manual selection mode
2. User click on the first task
3. The systems highlight the selected task
4. User click on the second task he/she wants to swap with
5. System swap the order of the tasks

###### **Primary Postcondition**

The tasks list is updated with a new order

###### **Alternate Trigger**

User click &quot;Manual sort&quot; after selecting a task in the manual selection mode

###### **Alternate Sequences**

4. User toggle off the manual sort by clicking the &quot;Manual sort&quot; again

a. System change the task list back to view mode

###### **Alternate Postconditions**

The task list remains in the same order as it was before

##### **Use Case Name: Edit a task**

###### **Summary**

After adding tasks to a timer, the user has an option to go back to the task to edit its name or duration

###### **Actors**

User

###### **Preconditions**

A task must be created

###### **Trigger**

User click &quot;Edit&quot; after hovering over the task

###### **Primary Sequence**

1. System Prompt the user to enter the new name
2. The user enters the new name
3. The system prompts the user to enter the new duration
4. The user enters the new duration
5. The system display two options &quot;Confirm&quot; or &quot;Cancel&quot;
6. User select &quot;Confirm&quot;
7. System update the task to the user&#39;s will

###### **Primary Postcondition**

The old task is replaced by the new task

###### **Alternate Trigger**

For 5 (alternate), the user clicks &quot;Cancel&quot;

###### **Alternate Sequences**

4. User keeps the same duration and proceed instead of changing it

a. The system display two options &quot;Confirm&quot; or &quot;Cancel&quot;

b. User select &quot;Confirm&quot;

5. User select &quot;Cancel&quot;

6. The system keeps the old task&#39;s information

###### **Alternate Postconditions**

4 System update the task with new durations but same name

5 The task remain the same as before
