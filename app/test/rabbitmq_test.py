import pika
import traceback
from flask import Blueprint, request, jsonify

test_R_MQQT_bp = Blueprint('test-mqtt', __name__)

@test_R_MQQT_bp.route('/send_message', methods=['POST'])
def send_message():
    try:
        # Ensure the message is properly formatted
        message = str(request.json.get('message', 'Default Message'))  # Convert to string

        # RabbitMQ connection and setup
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue='test_queue', durable=True)

        # Send message to the queue
        channel.basic_publish(
            exchange='',
            routing_key='test_queue',
            body=message.encode('utf-8'),  # Ensure it's encoded as bytes
            properties=pika.BasicProperties(
                delivery_mode=2,  # make the message persistent
            )
        )

        connection.close()
        return jsonify({'status': 'Message sent to queue'}), 200

    except Exception as e:
        error_message = traceback.format_exc()  # Get formatted exception string
        print(error_message)  # Log or print the error
        return jsonify({'error': str(e)}), 500


@test_R_MQQT_bp.route('/receive_message', methods=['POST'])
def receive_message():
    try:
        # RabbitMQ connection and setup
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Declare the queue (ensure it exists)
        channel.queue_declare(queue='test_queue', durable=True)

        # Get a single message from the queue
        method_frame, header_frame, body = channel.basic_get(queue='test_queue', auto_ack=True)

        if method_frame:
            message = body.decode('utf-8')  # Decode the message
            print(f"Received message: {message}")
            return jsonify({'message': message}), 200
        else:
            print("No messages in the queue")
            return jsonify({'message': 'No messages in the queue'}), 200

    except Exception as e:
        error_message = traceback.format_exc()  # Get formatted exception string
        print(error_message)  # Log or print the error
        return jsonify({'error': str(e)}), 500