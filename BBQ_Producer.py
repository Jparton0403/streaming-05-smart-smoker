"""
    This program sends a message to a queue on the RabbitMQ server.
    Sends bbq information in segemeted time frames of 30 seconds

    Author: Joshua Parton
    Date: September 22nd, 2023

"""
import pika
import sys
import webbrowser
import csv
import time

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_to_queue(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to a queue on the RabbitMQ server.

    Parameters:
        host (str): the IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """
    try:
        # Create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))

        # Use the connection to create a communication channel
        ch = conn.channel()

        # Use the channel to declare a durable queue
        # A durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # Messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)

        # Use the channel to publish a message to the queue
        # Every message passes through an exchange
        ch.basic_publish(exchange='', routing_key=queue_name, body=message)

        # Print a message to the console for the user
        print(f" [x] Sent {message} to {queue_name}")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # Close the connection to the server
        conn.close()

if __name__ == "__main__":
    # Ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site()

    # Read tasks from smoker-temps.csv and send them one by one
    with open('smoker-temps.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 4:
                timestamp, smoker_temp, food_a_temp, food_b_temp = row
                # Send Smoker Temp to "01-smoker" queue
                send_to_queue("localhost", "01-smoker", f"{timestamp}, {smoker_temp}")
                # Send Food A Temp to "02-food-A" queue
                send_to_queue("localhost", "02-food-A", f"{timestamp}, {food_a_temp}")
                # Send Food B Temp to "03-food-B" queue
                send_to_queue("localhost", "03-food-B", f"{timestamp}, {food_b_temp}")
                # Sleep for 30 seconds
                time.sleep(0)