# Smart Smoker Data Streaming Project

This program streams data from a smart smoker using a CSV file named `smoker-temps`. The data is sent to RabbitMQ server in segmented time frames of 30-second intervals.

- **Author:** Joshua Parton
- **Date:** September 22nd, 2023

## Problem Statement

We need to stream information from a smart smoker. Read one value every half minute (sleep_secs = 30).

**CSV Columns:**
- [0] **Time:** Date-time stamp for the sensor reading
- [1] **Channel1:** Smoker Temp → Sent to message queue "01-smoker"
- [2] **Channel2:** Food A Temp → Sent to message queue "02-food-A"
- [3] **Channel3:** Food B Temp → Sent to message queue "03-food-B"

### Requirements

- RabbitMQ server running
- `pika` installed in your active environment
- RabbitMQ Admin Access: [http://localhost:15672/](http://localhost:15672/)

## General Design Questions

- **How many producer processes do you need to read the temperatures?**
- **How many queues do we use?**
- **How many listening callback functions do we need?** *(Hint: one per queue)*

## Getting Started

### Task 1: Set Up the Repository

1. Create a new GitHub repository named `streaming-05-smart-smoker`.
2. Add a `README.md` file during the creation process. *(If not, you can always add it later.)*
3. Clone the repository to your local machine.
4. In VS Code, add a `.gitignore` file (you can use one from an earlier module).
5. Start working on the `README.md`. Create it if you didn't earlier.
6. Add the `smoker-temps.csv` data file to your repository.
7. Create a file for your BBQ producer.

### Task 2: Work on the Project

- Implement the producer processes to read temperatures.
- Set up RabbitMQ queues based on the requirements.
- Create listening callback functions for each queue.
- Apply everything you've learned previously.

## Screenshots

![Screenshot 1](path/to/Screenshot%202023-10-01%20133602.png)

![Screenshot 2](path/to/Screenshot%202023-10-01%20133618.png)
