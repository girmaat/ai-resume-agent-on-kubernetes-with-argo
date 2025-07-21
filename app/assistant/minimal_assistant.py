# ------------------------------------------------------------------------------
# Script: minimal_assistant.py
# Purpose: Basic assistant class that loads dummy summary and resume and responds to a single user message.
#
# How to Run:
#   python app/assistant/minimal_assistant.py
#
# Expected Output:
#   Assistant responds to your input using static prompt context
# ------------------------------------------------------------------------------

import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()

class ResumeAssistant:
    def __init__(self):
        self.name = "Girma Debella"
        self.openai = OpenAI()
        self.summary = self._load_summary()
        self.resume = self._load_resume()

    def _load_summary(self):
        path = "me/summary.txt"
        with open(path, encoding="utf-8") as f:
            return f.read()

    def _load_resume(self):
        pdf_path = "me/gi.pdf"
        reader = PdfReader(pdf_path)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])


    tools = [
        {
            "type": "function",
            "function": {
                "name": "record_user_details",
                "description": "Collect contact info when user expresses interest.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "User's email address"
                        },
                        "name": {
                            "type": "string",
                            "description": "Optional full name"
                        },
                        "notes": {
                            "type": "string",
                            "description": "Extra info, e.g., intent, job interest"
                        }
                    },
                    "required": ["email"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "record_unknown_query",
                "description": "Log questions that the assistant cannot answer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The user's original question"
                        }
                    },
                    "required": ["question"]
                }
            }
        }
    ]

    def system_prompt(self):
        return f"""
You are acting as {self.name}, a professional software engineer.

Your job is to answer questions about {self.name}'s experience, skills, background, and projects using the context below.

If a user expresses interest (e.g., wants to follow up, collaborate, hire, or get in touch), then:
- Use the tool `record_user_details` and collect their email, name, and notes (if given).

If a user asks something that cannot be confidently answered using the provided resume or summary:
- Use the tool `record_unknown_query` to log what was asked.

Do not guess or fabricate answers — if unsure, escalate using the appropriate tool.

---

## Summary:
{self.summary}

---

## Resume:
{self.resume}
"""

    def chat(self, user_input):
        messages = [
            {"role": "system", "content": self.system_prompt()},
            {"role": "user", "content": user_input}
        ]
        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=messages,                    
            tools=self.tools
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    assistant = ResumeAssistant()
    user_input = input("Ask something: ")
    print(assistant.chat(user_input))
