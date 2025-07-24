SHARED_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Collect contact info when user expresses interest in collaboration or hiring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "User's email address"},
                    "name": {"type": "string", "description": "User's full name"},
                    "notes": {"type": "string", "description": "User's message or interest details"}
                },
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_query",
            "description": "Log questions that cannot be answered from the provided resume or summary content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The exact user question that couldn't be answered"}
                },
                "required": ["question"]
            }
        }
    }
]
