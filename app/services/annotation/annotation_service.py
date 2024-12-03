from app import mongo
from bson import ObjectId
from app.services.email.email_service import send_email_with_template


def notify_user(user_email, session_id, base_url):
    """Send a notification email to the user."""
    link = f"{base_url}?session={session_id}"
    context = {"link": link}
    send_email_with_template(
        subject="New Annotation Task Created",
        recipient=user_email,
        template="emails/annotation_email.html",
        context=context
    )
