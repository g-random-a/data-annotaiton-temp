from app import mongo
from bson import ObjectId
from app.services.email.email_service import send_email_with_template

def create_annotation(data):
    """Create an annotation document in the database."""
    try:
        annotation_document = {
            "questionId": ObjectId(data["questionId"]),
            "annotator_id": ObjectId(data["userId"]),
            "timestamp": data["timestamp"],
            "sourceUrl": data["sourceUrl"],
            "annotation": "",
            "status": "pending",
            "annotationType": data["annotationType"],
            "annotationClasses": data["annotationClasses"],
        }
        result = mongo.db.annotation_session.insert_one(annotation_document)
        return result.inserted_id
    except Exception as e:
        raise Exception(f"An error occurred while creating the annotation: {str(e)}")

def notify_user(user_email, annotation_id, base_url):
    """Send a notification email to the user."""
    link = f"{base_url}/{annotation_id}"
    context = {"link": link}
    send_email_with_template(
        subject="New Annotation Task Created",
        recipient=user_email,
        template="emails/annotation_email.html",
        context=context
    )
