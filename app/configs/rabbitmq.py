import pika
import time
import logging

from app.config import Config

MAX_RETRIES = 5
RETRY_DELAY_MS = 5000
queue = 'question-response-microservice-events'

connection = None
channel = None

def connect_rabbitmq():
    global connection, channel
    retries = 0

    while retries < MAX_RETRIES:
        try:
            print(Config.RABBITMQ_HOST, Config.RABBITMQ_USERNAME, Config.RABBITMQ_PASSWORD)
            credentials = pika.PlainCredentials(Config.RABBITMQ_USERNAME, Config.RABBITMQ_PASSWORD)
            parameters = pika.ConnectionParameters(host=Config.RABBITMQ_HOST, credentials=credentials)

            # Establish connection
            connection = pika.BlockingConnection(parameters)
            print('RabbitMQ connected')
            print('RabbitMQ connected')

            # Create channel
            channel = connection.channel()
            print('RabbitMQ channel created')

            # Declare queue
            channel.queue_declare(queue=queue, durable=True)
            print(f'Queue "{queue}" is ready')

            return
        except Exception as error:
            logging.error(f'RabbitMQ connection attempt failed: {error}')
            retries += 1
            if retries < MAX_RETRIES:
                print(f'Retrying connection in {RETRY_DELAY_MS * retries / 1000} seconds...')
                time.sleep(RETRY_DELAY_MS * retries / 1000)
            else:
                logging.error('Max retries reached. RabbitMQ connection failed.')
                raise error

def attempt_reconnect():
    print('Reconnecting to RabbitMQ...')
    try:
        connect_rabbitmq()
    except Exception as err:
        logging.error('RabbitMQ reconnection failed:', err)

def close_rabbitmq():
    global connection, channel
    try:
        if channel:
            channel.close()
        if connection:
            connection.close()
        print('RabbitMQ connection closed')
    except Exception as error:
        logging.error(f'Failed to close RabbitMQ connection: {error}')

def get_channel():
    global channel
    if not channel:
        raise Exception('RabbitMQ channel is not initialized')
    return channel