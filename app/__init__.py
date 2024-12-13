import logging
import threading
import time
import cloudinary
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_mail import Mail

from app.configs.rabbitmq import connect_rabbitmq

mail = Mail()
mongo = PyMongo()
db = None

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, methods=["GET", "POST", "PUT", "DELETE"])

    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )

    # Initialize MongoDB
    mongo.init_app(app)
    mail.init_app(app)

    db = mongo.db

    # lets test the mongo here
    collection = db.annotation_session
    docs = collection.find()

    print(docs)
    print(docs.to_list(length=100))

    try:
        connect_rabbitmq()
        print('RabbitMQ connected')
        # start_consumer_thread('annotation-microservice-events', process_question_messages)
        print('RabbitMQ consumer started')
    except Exception as e:
        logging.error(f'Error initializing RabbitMQ: {e}')
        raise e

    # Register Blueprints
    from app.routes import register_routes
    # from app.test import register_test_routes
    register_routes(app)
    # register_test_routes(app)

    with app.app_context():
        from app.services.rabbitmq.messageConsumer import consume_messages
        from app.services.rabbitmq.messageProcesser import process_question_messages
        def run_consumer():
            with app.app_context():
                print("Starting RabbitMQ consumer thread...")
                consume_messages('annotation-microservice-events', process_question_messages)
        consumer_thread = threading.Thread(target=run_consumer, daemon=True)
        consumer_thread.start() 

    return app
