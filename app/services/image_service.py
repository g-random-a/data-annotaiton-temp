import cloudinary
import cloudinary.uploader
from app import mongo

def upload_image_service(image):
    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(image)
    image_data = {
        "filename": image.filename,
        "cloudinary_url": upload_result.get('secure_url'),
        "public_id": upload_result.get('public_id'),
        "created_at": upload_result.get('created_at'),
    }
    # Save metadata to MongoDB
    mongo.db.images.insert_one(image_data)
    return {
        "message": "Image uploaded successfully",
        "data": image_data
    }
