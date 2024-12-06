from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify, current_app
from app.services.annotation.annotation_service import  notify_user
import datetime
import traceback
import app.validations.annotation.annotation as validation
from app import mongo
from pymongo.errors import PyMongoError
from bson import ObjectId

annotate_bp = Blueprint('annotate', __name__)

def create_annotation(data):
    try:

        print("Creating annotation...")

        # Validate incoming data
        error = validation.validateCreateAnnotaiton(data)
        if error:
            print(f"Validation failed: {error}")
            return jsonify({"error": error}), 400

        data["createdAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"

        for atr in data["attributes"].values():
            print(atr)
            if atr['type'] == 'TEXT':
                atr['type'] = 1
            elif atr['type'] == 'CHECKBOX':
                atr['type'] = 2
            elif atr['type'] == 'RADIO':
                atr['type'] = 3

        # Use a database transaction
        with mongo.cx.start_session() as session:
            with session.start_transaction():
                try:
                    # Create database entry within the transaction
                    annotations_collection = mongo.db.annotations  # Adjust collection name if needed
                    result = annotations_collection.insert_one(data, session=session)
                    annotation_id = result.inserted_id

                    # If email succeeds, transaction will commit automatically
                    print("Annotation created successfully", annotation_id)
                    return jsonify({
                        "message": "Annotation created successfully",
                        "annotationId": str(annotation_id)
                    }), 201

                except Exception as email_error:
                    # If email fails, the transaction will automatically roll back
                    print(f"Email sending failed: {str(email_error)}")
                    error_trace = traceback.format_exc()
                    print(f"Traceback: {error_trace}")
                    raise email_error  # This will cause the transaction to roll back

    except PyMongoError as db_error:
        print(f"Database operation failed: {str(db_error)}")
        error_trace = traceback.format_exc()
        print(f"Traceback: {error_trace}")
        return jsonify({"error": "Database operation failed"}), 500

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error occurred: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({"error": str(e)}), 500
    
@annotate_bp.route('/create-user-session', methods=['POST'])
def create_user_session():
    try:
        data = request.json
        print(data)

        # Validate incoming data
        error = validation.validateCreateUserSession(data)
        if error:
            return jsonify({"error": error}), 400

        # Prepare data
        data["createdAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
        data["status"] = "active"
        data["lastUpdatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"

        # Use a database transaction
        with mongo.cx.start_session() as session:
            with session.start_transaction():
                try:
                    annotations_collection = mongo.db.annotations  # Adjust collection name if needed
                    annotation_result = annotations_collection.find_one({"_id": ObjectId(data["annotationId"])})

                    if annotation_result is None:
                        return jsonify({"error": "Annotation not found"}), 404

                    # Create database entry within the transaction
                    annotation_session = mongo.db.annotation_session  # Adjust collection name if needed
                    result = annotation_session.insert_one(data, session=session)
                    annotation_id = result.inserted_id

                    # Notify user via email
                    base_url = current_app.config["BASE_URL"]
                    notify_user(data["userEmail"], str(annotation_id), base_url)

                    # If email succeeds, transaction will commit automatically
                    return jsonify({
                        "message": "Annotation created successfully",
                        "annotationId": str(annotation_id)
                    }), 201

                except Exception as email_error:
                    # If email fails, the transaction will automatically roll back
                    print(f"Email sending failed: {str(email_error)}")
                    error_trace = traceback.format_exc()
                    print(f"Traceback: {error_trace}")
                    raise email_error  # This will cause the transaction to roll back

    except PyMongoError as db_error:
        print(f"Database operation failed: {str(db_error)}")
        error_trace = traceback.format_exc()
        print(f"Traceback: {error_trace}")


@annotate_bp.route('/get-annotation/<string:sessionId>', methods=['GET'])
def get_annotation(sessionId):
    try:
        # Query the database for the provided sessionId
        annotations_session = mongo.db.annotation_session  # Adjust collection name if needed
        annotation_session_res = annotations_session.find_one({"_id": ObjectId(sessionId)})

        annotaion_documents = mongo.db.annotations
        annotation = annotaion_documents.find_one({"_id": ObjectId(annotation_session_res["annotationId"])})
        
        if not annotation:
            return jsonify({"error": "Annotation not found"}), 404

        # Construct the response
        response = {
            "sourceUrls": annotation.get("sourceUrls", ""),
            "fileType": annotation.get("fileType", "unknown"),  # Default to 'unknown' if not provided
            "attributes": annotation.get("attributes", {})  # Default to empty dictionary if not provided
        }

        return jsonify(response), 200

    except PyMongoError as db_error:
        print(f"Database operation failed: {str(db_error)}")
        error_trace = traceback.format_exc()
        print(f"Traceback: {error_trace}")
        return jsonify({"error": "Database operation failed"}), 500

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error occurred: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({"error": str(e)}), 500
    

@annotate_bp.route('/save-annotation', methods=['POST'])
def save_project():
    try:
        # Parse incoming JSON data
        project_data = request.json

        if not project_data:
            return jsonify({"error": "No project data provided"}), 400

        # Generate a unique filename or use an identifier from the project data
        project_id = project_data.get('project', {}).get('pid', 'unknown_project')
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
        filename = f"{project_id}_{timestamp}.json"

        # Save project data to the database
        projects_collection = mongo.db.projects  # Adjust collection name if needed
        result = projects_collection.insert_one({
            "filename": filename,
            "project_data": project_data,
            "timestamp": timestamp
        })

        return jsonify({
            "message": "Project saved successfully",
            "projectId": str(result.inserted_id),
            "filename": filename
        }), 201

    except PyMongoError as db_error:
        print(f"Database operation failed: {str(db_error)}")
        error_trace = traceback.format_exc()
        print(f"Traceback: {error_trace}")
        return jsonify({"error": "Database operation failed"}), 500

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error occurred: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({"error": "Failed to save project"}), 500