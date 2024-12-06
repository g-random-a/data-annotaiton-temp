from bson import ObjectId

def validateCreateAnnotaiton(data):
    required_fields = ["questionId", "inputId", "sourceUrls", "fileType", "attributes"]
    if not all(field in data for field in required_fields):
        return "Missing required fields"
    
    if not isinstance(data["inputId"], str):
        return "Invalid input ID"

    if not ObjectId.is_valid(data["questionId"]):
        return "Invalid question ID"
    
    if not isinstance(data["sourceUrls"], list) and len(data['sourceUrls']) == 0:
        return "Invalid source URL"
    
    for url in data["sourceUrls"]:
        if not isinstance(url, str):
            return "Invalid source URL"
    
    if not isinstance(data["fileType"], str):
        return "Invalid annotation type"
    
    if not isinstance(data["attributes"], dict):
        return "Invalid attributes"
    
    for key, value in data["attributes"].items():
        if not isinstance(key, str):
            return "Invalid attributes"

        if not isinstance(value, dict):
            return "Invalid attributes"
        
        required_keys = ["aname", "anchor_id", "type", "desc", "options", "default_option_id"]
        if not all(key in value for key in required_keys):
            return "Missing required fields"
        
        if not isinstance(value["aname"], str):
            return "Invalid attributes aname"
        
        if not isinstance(value["anchor_id"], str):
            return "Invalid attributes anchor_id"
        
        if not isinstance(value["type"], str):
            return "Invalid attributes type"
        
        if not isinstance(value["desc"], str):
            return "Invalid attributes desc"
        
        if not isinstance(value["options"], dict):
            return "Invalid attributes options"
        
        for key, optionvalue in value["options"].items():
            if not isinstance(key, str):
                return "Invalid attributes options"
            
            if not isinstance(optionvalue, str):
                return "Invalid attributes options"
        
        if not isinstance(value["default_option_id"], str):
            return "Invalid attributes default_option_id"
     
    return None
    

    
def validateCreateUserSession(data):
    required_fields = ["userEmail", "annotationId"]
    if not all(field in data for field in required_fields):
        return "Missing required fields"
    
    # if not ObjectId.is_valid(data["userId"]):
    #     return "Invalid user ID"
    
    if not ObjectId.is_valid(data["annotationId"]):
        return "Invalid annotaion ID"

    if not isinstance(data["userEmail"], str):
        return "Invalid user email"
    
    return None