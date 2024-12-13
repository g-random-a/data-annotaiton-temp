import pika
from app.configs.rabbitmq import get_channel

def publish_message(queue, message, messageType):
    try:
        channel = get_channel()
        
        # Ensure the queue is declared before publishing
        channel.queue_declare(queue=queue, durable=True)
        print(f"Queue '{queue}' declared.")

        standardBody = {
            "message": message,
            "type": messageType,
        }

        # Publish the message
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=standardBody,
            properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
        )
        print(f" [x] Sent '{message}' to queue '{queue}'")

    except Exception as e:
        print(f"Error publishing message: {e}")
        raise e
