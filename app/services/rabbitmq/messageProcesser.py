import logging
from app.routes.annotate import create_annotation

def process_question_messages(message):
    print("Processing message", message)
    print(f"Processing message with type: {message.get('type')}")
    if message.get("type") == "QUESTION_CREATED":
        annotation = create_annotation(message.get("payload"))
        print(annotation)
        print("HANDELED QUESTION_CREATED")
    elif message.get("type") == "QUESTION_UPDATED":
        print("Handling QUESTION_UPDATED")
    else:
        logging.warning("Unknown message type")
