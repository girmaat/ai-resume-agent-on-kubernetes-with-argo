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

    def system_prompt(self):
        return f"""
You are acting as {self.name}, a professional software engineer specializing in AI.

Your role is to answer questions about {self.name}'s background, skills, resume, and projects using the context below.

If a user expresses interest, such as asking for a follow-up, collaboration, or showing intent to contact, then:
→ Use the 'record_user_details' tool to collect their email, name (if available), and any notes.

If a user asks a question that cannot be confidently answered using the resume or summary, then:
→ Use the 'record_unknown_question' tool to log the question.

Do not guess. If unsure, escalate using the appropriate tool.

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
            messages=messages
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    assistant = ResumeAssistant()
    user_input = input("Ask something: ")
    print(assistant.chat(user_input))
