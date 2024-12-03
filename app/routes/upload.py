from flask import Blueprint, request, jsonify
from app.services.image_service import upload_image_service
from app.utils.file_utils import allowed_file
from app import mongo

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(image.filename):
        return jsonify({"error": "Invalid file type"}), 400

    try:
        result = upload_image_service(image)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@upload_bp.route('/test-db', methods=['GET'])
def test_db():
    try:
        # List all collections as a test
        collections = mongo.db.list_collection_names()
        return jsonify({"status": "Connected to DB", "collections": collections}), 200
    except Exception as e:
        return jsonify({"status": "Failed to connect", "error": str(e)}), 500