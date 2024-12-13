from flask import json
import logging
from app.configs.rabbitmq import channel

def consume_messages(queue_name, process_message_function):
    """
    Consume messages from a specified RabbitMQ queue and route them to the given processing function.

    Args:
        queue_name (str): The name of the RabbitMQ queue to consume messages from.
        process_message_function (function): A function that processes a single message.
                                             It takes a dictionary as input.

    """
    if not channel:
        raise Exception("RabbitMQ channel is not initialized")

    def wrapper(ch, method, properties, body):
        """
        Callback wrapper for consuming messages.
        """
        try:
            message = json.loads(body)
            print(f"Received message: {message}")
            process_message_function(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Failed to process message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    try:
        channel.basic_consume(queue=queue_name, on_message_callback=wrapper)
        print(f"Started consuming messages from queue '{queue_name}'")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping consumer...")
        channel.stop_consuming()
    except Exception as e:
        logging.error(f"Error while consuming messages: {e}")
    finally:
        print("RabbitMQ consumer stopped")
