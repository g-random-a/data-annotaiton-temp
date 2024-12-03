
from flask import Blueprint, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus


test_bp = Blueprint('test-mongdb', __name__)

# MongoDB connection details
username = "abibgemmechu"
password = "Habibmike@1"
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)
connection_string = "mongodb+srv://hgemmechu:XMNeRveGd9oTrtpW@cluster0.agrcx.mongodb.net/Annotation_db"

@test_bp.route('/test-mongodb', methods=['GET'])
def test_mongodb_connection():
    try:
        # Initialize the MongoDB client
        print("Testing connection to MongoDB...")
        client = MongoClient(connection_string)

        # Test the connection
        print("Testing connection to MongoDB...")
        client.admin.command("ping")

        print("Connection successful!")

        # List available databases
        # databases = client.list_database_names()
        # documents = client.db.collection.find()

        # query annotation_session document
        documents = client.Annotation_db.annotation_session.find()
        print(documents)
        documents_list = list(documents)
        print(documents_list)
        return jsonify({
            "status": "success",
            "message": "Connected to MongoDB successfully!",
            # "databases": databases
            # "documents": documents
        })

    except ConnectionFailure as e:
        return jsonify({
            "status": "error",
            "message": f"Connection failed: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

    finally:
        try:
            client.close()
        except NameError:
            pass