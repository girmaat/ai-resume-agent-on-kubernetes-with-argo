from app.assistant.config.tools.base_tools import SHARED_TOOLS

POWER_PLATFORM_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_powerplatform_help",
            "description": "Provide technical guidance for Power Platform issues.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue": {"type": "string", "description": "User's technical question"},
                    "component": {
                        "type": "string",
                        "enum": ["Power Apps", "Power Automate", "Power BI", "SharePoint"],
                        "description": "Which component is involved?"
                    }
                },
                "required": ["issue", "component"]
            }
        }
    }
]

TOOLS = SHARED_TOOLS + POWER_PLATFORM_TOOLS  # Combine shared and Power Platform tools
