import cloudinary
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_mail import Mail

mail = Mail()
mongo = PyMongo()
db = None

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

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

    # Register Blueprints
    from app.routes import register_routes
    from app.test import register_test_routes
    register_routes(app)
    # register_test_routes(app)

    return app
