from bson import ObjectId

def validateCreateAnnotaiton(data):
    required_fields = ["userEmail", "questionId", "userId", "sourceUrl", "annotationType", "annotationClasses"]
    if not all(field in data for field in required_fields):
        return "Missing required fields"

    if not ObjectId.is_valid(data["questionId"]):
        return "Invalid question ID"

    if not ObjectId.is_valid(data["userId"]):
        return "Invalid user ID"
    
    if not isinstance(data["sourceUrl"], str):
        return "Invalid source URL"
    
    if not isinstance(data["annotationType"], str):
        return "Invalid annotation type"
    
    if not isinstance(data["annotationClasses"], list):
        return "Invalid annotation classes"
    
    return None
    


    