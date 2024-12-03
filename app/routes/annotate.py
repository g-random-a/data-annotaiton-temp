from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify, current_app
from app.services.annotation.annotation_service import create_annotation, notify_user
from datetime import datetime
import traceback
import app.validations.annotation.annotation as validation
from app import mongo
from pymongo.errors import PyMongoError


annotate_bp = Blueprint('annotate', __name__)

# @annotate_bp.route('/annotate', methods=['POST'])
# def annotate_image():
#     data = request.json
#     if not data or 'public_id' not in data or 'annotations' not in data:
#         return jsonify({"error": "Invalid annotation data"}), 400

#     try:
#         save_annotations(data['public_id'], data['annotations'])
#         return jsonify({"message": "Annotations saved successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @annotate_bp.route('/annotations/<public_id>', methods=['GET'])
# def fetch_annotations(public_id):
#     try:
#         annotations = get_annotations(public_id)
#         if not annotations:
#             return jsonify({"error": "Image not found"}), 404
#         return jsonify({"annotations": annotations}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@annotate_bp.route('/create-annotation', methods=['POST'])
def create_annotation_endpoint():
    try:
        data = request.json
        print(data)

        # Validate incoming data
        error = validation.validateCreateAnnotaiton(data)
        if error:
            return jsonify({"error": error}), 400

        # Prepare data
        data["timestamp"] = datetime.utcnow().isoformat() + "Z"

        # Use a database transaction
        with mongo.cx.start_session() as session:
            with session.start_transaction():
                try:
                    # Create database entry within the transaction
                    annotations_collection = mongo.db.annotations  # Adjust collection name if needed
                    result = annotations_collection.insert_one(data, session=session)
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
        return jsonify({"error": "Database operation failed"}), 500

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error occurred: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({"error": str(e)}), 500
