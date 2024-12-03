from flask import current_app, render_template
from flask_mail import Message
from app import mail

def send_email_with_template(subject, recipient, template, context):
    """Send an email with an HTML template."""
    body_html = render_template(template, **context)
    print(current_app.extensions)
    msg = Message(subject, recipients=[recipient], html=body_html, sender="hgemmechu@qena.dev")
    mail.send(msg)
