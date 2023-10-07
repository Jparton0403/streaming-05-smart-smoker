"""
    This program listens for work messages contiously. 
    Start multiple versions to add more workers.  

    Author: joshua parton
    Date: oct 1 2023

"""

import pika
from collections import deque

# RabbitMQ configuration
rabbit_host = 'localhost'
rabbit_port = 5672
queues = ['03-food-B']  # We're only focusing on Food-B

# Constants for food stall alert conditions
FOOD_TIME_WINDOW = 2.5  # minutes
FOOD_DEQUE_MAX_LENGTH = int(FOOD_TIME_WINDOW * 2)  # Assuming one reading every 0.5 minutes
FOOD_TEMP_CHANGE_THRESHOLD = 15  # degrees F

# Create a deque to store temperature readings for food A
food_b_temperature_deque = deque(maxlen=FOOD_DEQUE_MAX_LENGTH)

def generic_callback(ch, method, properties, body):
    """ Process messages for smoker and Food-B."""
    print(f" [x] Received {body.decode()} from queue '{method.routing_key}'")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def show_food_b_alert(timestamp):
    print(f"Food b Alert at: {timestamp}")

def food_b_callback(ch, method, properties, body):
    try:
        body_str = body.decode('utf-8')
        timestamp = body_str.split()[1]
        temperature = float(body_str.split(':')[3])
        food_b_temperature_deque.append(temperature)
        print(f"Received Food-B temperature: {temperature}°C")
        if len(food_b_temperature_deque) >= 5:
            temp_changes = [food_b_temperature_deque[i] - food_b_temperature_deque[i - 1] for i in range(-1, -5, -1)]
            if any(temp_change > FOOD_TEMP_CHANGE_THRESHOLD for temp_change in temp_changes):
                show_food_b_alert(timestamp)
            if len(food_b_temperature_deque) % 5 == 0:
                food_b_temperature_deque.clear()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except ValueError:
        print("Invalid temperature value in message body.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
    channel = connection.channel()

    # Set up consumers for each queue
    for queue in queues:
        channel.queue_declare(queue=queue, durable=True)
        if queue == 'Food-B':
            channel.basic_consume(queue=queue, on_message_callback=food_b_callback)
        else:
            channel.basic_consume(queue=queue, on_message_callback=generic_callback)
        print(f"Consumer for {queue} is waiting for messages. To exit, press Ctrl+C")

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser stopped consuming. Exiting...")