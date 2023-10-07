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
queue = '01-smoker'

# Constants for smoker alert conditions
SMOKER_TIME_WINDOW = 2.5  # minutes
SMOKER_DEQUE_MAX_LENGTH = 5  # 2.5 minutes * 1 reading every 0.5 minutes
SMOKER_TEMP_DROP_THRESHOLD = 15  # degrees F

# Create a deque to store temperature readings for the smoker
smoker_temperature_deque = deque(maxlen=SMOKER_DEQUE_MAX_LENGTH)

def show_smoker_alert(timestamp):
    print(f"SMOKER ALERT: Rapid temperature decrease detected at {timestamp}!")

def smoker_callback(ch, method, properties, body):
    try:
        body_str = body.decode('utf-8')
        csv_parts = body_str.split(',')
        
        if len(csv_parts) < 2:
            raise ValueError(f"Message has fewer columns than expected. Message: {body_str}")

        # Get timestamp and try to convert the temperature from the CSV message
        timestamp = csv_parts[0]
        
        # Trim whitespace from the temperature string and check if it's empty
        temperature_str = csv_parts[1].strip()
        if not temperature_str:
            raise ValueError(f"Temperature value is empty or just whitespace. Message: {body_str}")
        
        temperature = float(temperature_str)  # Convert to float after trimming
        
        smoker_temperature_deque.append(temperature)
        print(f"Received smoker temperature: {temperature}°F")

        # Check the last 5 temperature readings for a rapid decrease
        if len(smoker_temperature_deque) >= 5:
            temp_changes = [smoker_temperature_deque[i] - smoker_temperature_deque[i - 1] for i in range(-1, -6, -1)]
            if any(temp_change <= -SMOKER_TEMP_DROP_THRESHOLD for temp_change in temp_changes):
                show_smoker_alert(timestamp)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except ValueError as ve:
        print(f"Invalid temperature value or message format in smoker message body. Error: {str(ve)}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing smoker message: {str(e)}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
    channel = connection.channel()

    # Set up a consumer for the smoker queue
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_consume(queue=queue, on_message_callback=smoker_callback)
    print(f"Consumer for {queue} is waiting for messages. To exit, press Ctrl+C")

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser stopped consuming. Exiting...")