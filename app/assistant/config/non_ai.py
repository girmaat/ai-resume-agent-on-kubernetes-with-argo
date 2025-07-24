from pathlib import Path
import os
class ResumeConfig:
    """Central configuration for all resume profiles"""
    
    CURRENT_PROFILE = "power_platform"  # Switch between "ai" and "power_platform"
    
    # Complete profile configurations
    PROFILE_CONFIGS = {
        "ai": {
            "PERSONAL": {
                "name": "Girma Debella",
                "title": "AI Engineer",
                "description": "I specialize in building intelligent systems using LLM.",
                "blog_url": "https://yourblog.com",
                "resume_button_text": "Download the PDF"
            },
            "UI": {
                "theme": {
                    "primary": "#10B981",  # Emerald green
                    "primary_dark": "#059669",
                    "background": "#1F2937",
                    "surface": "#374151",
                    "text": "#F9FAFB",
                    "border": "#4B5563",
                    "divider": "#4B5563"
                },
                "titles": {
                    "assistant_title": "AI-Powered Resume Assistant",
                    "start_chatting_title": "Chat With My AI Expertise",
                    "blog_link_text": "My AI Blog"
                },
                "descriptions": {
                    "assistant_description": (
                        "This AI assistant showcases my expertise in artificial intelligence, "
                        "machine learning, and LLM systems. Built with cutting-edge technologies, "
                        "it demonstrates my skills in AI engineering and deployment."
                    )
                },
                "chat": {
                    "initial_message": "Ask about Girma's projects, ML models, or engineering experience. Start typing in the box below ...",
                    "input_placeholder": "Question about Girma's work...",
                    "start_chatting_text": "Discuss my AI projects and research...",
                    "typing_delay": 0.02,
                    "thinking_message": "<span class='spinner'></span> Thinking..."
                }
            }
        },
        "power_platform": {
            "PERSONAL": {
                "name": "Girma Debella",
                "title": "Sr. Power Platform/SharePoint Developer",
                "description": "I specialize in building intelligent systems for business automation...",
                "blog_url": "https://your-powerplatform-blog.com",
                "resume_button_text": "Download Resume"
            },
            "UI": {
                "theme": {
                    "primary": "#3B82F6",  # Blue
                    "primary_dark": "#2563EB",
                    "background": "#1E3A8A",
                    "surface": "#1E40AF",
                    "text": "#EFF6FF",
                    "border": "#1E3A8A",
                    "divider": "#1E40AF"
                },
                "titles": {
                    "assistant_title": "Power Platform Solutions Expert",
                    "start_chatting_title": "Chat about my Power Platform Projects?",
                    "blog_link_text": "Power Platform Blog"
                },
                "descriptions": {
                    "assistant_description": (
                        "This assistant demonstrates my expertise in Power Platform solutions, "
                        "including Power Apps, Power Automate, and SharePoint integrations. "
                        "It showcases my ability to transform business processes through automation."
                    )
                },
                "chat": {
                    "initial_message": "Ask about Girma's Power Platform implementations or SharePoint solutions and projects. Start typing in the box below ...",
                    "input_placeholder": "Question about Power Platform...",
                    "start_chatting_text": "Let's discuss about my business automation solutions...",
                    "typing_delay": 0.03,
                    "thinking_message": "<span class='spinner'></span> Thinking..."
                }
            }
        }
    }

    @property
    def first_name(self):
        full_name = self.PERSONAL['name']
        return full_name.split()[0] if ' ' in full_name else full_name

    @property
    def PERSONAL(self):
        """Returns personal data for current profile"""
        return self.PROFILE_CONFIGS[self.CURRENT_PROFILE]["PERSONAL"]

    @property
    def UI(self):
        """Returns UI configuration for current profile"""
        return self.PROFILE_CONFIGS[self.CURRENT_PROFILE]["UI"]

    def __init__(self):
        # Set profile-specific paths
        self.PERSONAL["resume_pdf"] = str(self.resume_path)
        self.PERSONAL["summary_file"] = str(self.summary_path)
        self.validate_paths()
    
    @property
    def BASE_PATH(self):
        return Path("me")
    
    @property
    def profile_image(self):
        return self.BASE_PATH / "profile.png"
    
    @property
    def resume_pdf(self):
        """Compatibility property - points to current profile's resume"""
        return str(self.BASE_PATH / self.CURRENT_PROFILE / "gi.pdf")
    
    @property
    def resume_path(self):
        return self.BASE_PATH / self.CURRENT_PROFILE / "gi.pdf"
    
    @property
    def summary_path(self):
        return self.BASE_PATH / self.CURRENT_PROFILE / "summary.txt"
    
    # Dynamic imports
    @property
    def prompts_module(self):
        return f"app.assistant.config.prompts.gi_{self.CURRENT_PROFILE}"
    
    @property
    def tools_module(self):
        return f"app.assistant.config.tools.gi_{self.CURRENT_PROFILE}"
    # UI and other configurations remain here
    
    # ============ Assistant Configuration ============
    ASSISTANT = {
        "system_prompt_intro": (            
            "You are an AI assistant representing {name}. "
            "Always refer to {name} in third person. "
            "When users say 'you' they mean you (the AI assistant).\n\n"
            "Answer questions about {name}'s experience as {title}:\n"
            "You are acting as {name}, a professional {title}.\n\n"
            "Your job is to answer questions about {name}'s experience, skills, background, and projects using the context below.\n\n"
        ),
        "tool_instructions": (
            "If a user expresses interest (e.g., wants to follow up, collaborate, hire, or get in touch), then:\n"
            "- Use the tool `record_user_details` and collect their email, name, and notes (if given).\n\n"
            "If a user asks something that cannot be confidently answered using the provided resume or summary:\n"
            "- Use the tool `record_unknown_query` to log what was asked.\n\n"
            "Do not guess or fabricate answers — if unsure, escalate using the appropriate tool.\n"
        ),
        "content_markers": {
            "summary": "## Summary:\n{content}\n\n---\n\n",
            "resume": "## Resume:\n{content}"
        }
    }
    

    # ============ Chat Configuration ============
    @property
    def CHAT(self):
        return {
            "thinking_message": "<span class='spinner'></span> Thinking...",
            "pronoun_replacements": {
                # User message replacements
                " your ": f" {self.first_name}'s ",
                " you ": " this assistant ",
                " my ": f" {self.first_name}'s ",
                " me ": f" {self.first_name} ",
                
                # Response replacements
                " his ": f" {self.first_name}'s ",
                " him ": f" {self.first_name} ",
                " he ": f" {self.first_name} "
            },
            "typing_delay": 0.02,
            "response_delay": 0.02,
        }
    
    # ============ Notification Messages ============
    NOTIFICATIONS = {
        "unknown_question": "[Unknown Question] {question}",
        "user_interest": "[Interest] Email: {email} | Name: {name} | Notes: {notes}",
        "email_subject": "AI Assistant Alert",
    }
    
    # ============ Error Messages ============
    ERRORS = {
        "email_not_configured": "Email not configured — skipping.",
        "pushover_not_configured": "Pushover not configured — skipping.",
        "slack_not_configured": "Slack not configured — skipping.",
        "email_failed": "Email failed: {error}",
        "pushover_failed": "Pushover failed: {error}",
        "slack_failed": "Slack failed: {error}",
    }
    
    
    def validate_paths(self):
        """Validate files for current profile"""
        required = [
            self.resume_path,
            self.summary_path,
            self.profile_image
        ]
        for path in required:
            if not path.exists():
                raise FileNotFoundError(f"Required file missing: {path}")

# Singleton instance
config = ResumeConfig()
config.validate_paths()
