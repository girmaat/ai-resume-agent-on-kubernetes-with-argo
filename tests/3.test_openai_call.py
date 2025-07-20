# ------------------------------------------------------------------------------

# Purpose: Make a real call to the OpenAI API to verify API key and model access.
#
# How to Run:
#   $ python tests/3.test_openai_call.py
#
# Expected Output:
#   Success message with GPT response (e.g., “🤖 GPT says: Hello!”)
#
# Notes:
#   - Requires OPENAI_API_KEY in your .env file
#   - Make sure you have internet access and valid OpenAI billing setup
#   - This script helps validate connectivity and credentials before deeper integration
# ------------------------------------------------------------------------------

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    exit(1)

try:
    response = client.chat.completions.create(
        model="gpt-4",  
        messages=[
            {"role": "user", "content": "Say hello"}
        ]
    )
    message = response.choices[0].message.content
    print("GPT says:", message)
except Exception as e:
    print("ERROR: OpenAI API call failed:", e)
    exit(1)
