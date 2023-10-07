# streaming-06-smart-smoker

# this is intended to stream data via rabbit mq utilzing a csv named smoker-temps

   
    ###This program sends a message to a queue on the RabbitMQ server.
    Sends bbq information in segemeted time frames of 30 second intervals

    Author: Joshua Parton
    Date: September 22nd, 2023
## The Problem / Challenge To Solve
Please read about the Smart Smoker system here: Smart Smoker
Access the smoker data file here Download smoker data file here.
We want to stream information from a smart smoker. Read one value every half minute. (sleep_secs = 30)

##Smart Smoker System
Read about the Smart Smoker system here: Smart Smoker
We read one value every half minute. (sleep_secs = 30)
smoker-temps.csv has 4 columns:

[0] Time = Date-time stamp for the sensor reading
[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
[2] Channe2 = Food A Temp --> send to message queue "02-food-A"
[3] Channe3 = Food B Temp --> send to message queue "02-food-B"
We want know if:

###The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
Any food temperature changes less than 1 degree F in 10 minutes (food stall!)
Time Windows

Smoker time window is 2.5 minutes
Food time window is 10 minutes
Deque Max Length

At one reading every 1/2 minute, the smoker deque max length is 5 (2.5 min * 1 reading/0.5 min)
At one reading every 1/2 minute, the food deque max length is 20 (10 min * 1 reading/0.5 min) 
Condition To monitor

If smoker temp decreases by 15 F or more in 2.5 min (or 5 readings)  --> smoker alert!
If food temp change in temp is 1 F or less in 10 min (or 20 readings)  --> food stall alert!
Requirements

###RabbitMQ server running
pika installed in your active environment
RabbitMQ Admin

See http://localhost:15672/Links to an external site.
General Design 

How many producer processes do you need to read the temperatures: One producer, built last project.
How many listening queues do we use: three queues, named as listed above.
How many listening callback functions do we need (Hint: one per queue): Three callback functions are needed.
 

Task 1. Open Your Existing Project
On your machine, open your existing streaming-05-getting-started repo in VS Code.
Create a file for your consumer (or 3 files if you'd like to use 3 consumers).
 

Task 2. Design and Implement Each Consumer
Design and implement each bbq consumer. You could have one. You could have 3.  More detailed help provided in links below. 
Use the logic, approach, and structure from prior modules (use the recommended versions).
Modifying them to serve your purpose IS part of the assignment.
Do not start from scratch - do not search for code - do not use a notebook.
Use comments in the code and repo to explain your work. 
Use docstring comments and add your name and date to your README and your code files. 
 

Task 3. Professionally Present your Project
Explain your project in the README.
Include your name, date.
Include prerequisites and how to run your code. 
Explain and show how your project works. 
Tell us what commands are needed. Use code fencing in GitHub or backtics for inline code to share commands.
Display screenshots of your console with the producer and consumer running.
Display screenshots of at least one interesting part of the RabbitMQ console. 
More Guidance
To be guided through the consumer design, read Module 6.1: Guided Consumer Design
For guidance on consumer implementation, read Module 6.2: Guided Consumer Implementation
For guidance on implementing a consumer callback, read Module 6.3: Implementing a Callback Function
Use the discussion forum when you get stuck.
Try to help without giving away code. 
Requirements
In your callback function, make sure you generate alerts - there will be a smoker alert and both Food A and Food B will stall. 

Your README.md screenshots must show 4 concurrent processes:

Producer (getting the temperature readings)
Smoker monitor
Food A monitor
Food B monitor
In addition, you must show at least 3 significant events.

Run each terminal long enough that you can show the significant events in your screenshots:

Visible Smoker Alert with timestamp
Visible Food A stall with timestamp
Visible Food B stall with timestamp
Submission Instructions
Read Project Submission Instructions
Submit
Part 1 - Project 
Clickable link to your public GitHub repo(s) with custom README and displayed screenshots: 
About how long did you spend this module:
Did you use one consumer with 3 queues (or 3 consumers each with one queue):
Why:
When did a Smoker Alert occur:
When did a Food A stall occur:
When did a Food B stall occur:
What was most difficult about this module:
What was most interesting:
In a real system, you'd want to get alerts from your smart smoker - maybe a text message.
Did you experiment with adding alerts to the project and getting an email or text when the smoker alerted? 
Would you be able to add this feature if implementing a similar system in real life?
Optional bonus: Did you successfully implement an alert (and clearly show it in your README.md and repo)?

all three consumers.png

 
