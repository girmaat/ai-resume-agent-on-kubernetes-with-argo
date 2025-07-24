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
from importlib import import_module  # Add this import
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from openai.types.chat import ChatCompletionMessageToolCall

from app.assistant.config.non_ai import config
from app.tools import record_user_details, record_unknown_query

load_dotenv()

class ResumeAssistant:
    def __init__(self):
        # Dynamic imports
        prompts = import_module(config.prompts_module)
        tools = import_module(config.tools_module)
        
        self.name = config.PERSONAL["name"]
        self.openai = OpenAI()
        self.tools = tools.TOOLS
        self.summary = self._load_summary()
        self.resume = self._load_resume()
        self.system_prompt_func = prompts.get_system_prompt

    def _load_summary(self):
        with open(config.summary_path, encoding="utf-8") as f:
            return f.read()

    def _load_resume(self):
        reader = PdfReader(config.resume_path)
        return "\n".join(p.extract_text() for p in reader.pages if p.extract_text())

    def get_resume_path(self):
        """Return absolute path to resume PDF"""
        abs_path = os.path.abspath(config.PERSONAL["resume_pdf"])
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Resume not found at {abs_path}")
        return abs_path

    def system_prompt(self):
        return self.system_prompt_func(self.summary, self.resume)

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

        choice = response.choices[0]
        if choice.finish_reason == "tool_calls":
            tool_calls = choice.message.tool_calls or []

            # Add tool call message
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tc.model_dump() for tc in tool_calls]
            })

            for call in tool_calls:
                fn_name = call.function.name
                args = eval(call.function.arguments)  # JSON string

                if fn_name == "record_user_details":
                    result = record_user_details(**args)
                elif fn_name == "record_unknown_query":
                    result = record_unknown_query(**args)
                else:
                    result = {"error": "unknown tool"}

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                })

            # Re-send messages with tool outputs
            second_response = self.openai.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            return second_response.choices[0].message.content

        else:
            return choice.message.content

if __name__ == "__main__":
    assistant = ResumeAssistant()
    user_input = input("Ask something: ")
    print(assistant.chat(user_input))
