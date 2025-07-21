# ------------------------------------------------------------------------------
# File: tests/test_tools.py
# Purpose: Manually test the tool functions (record_user_details and
#          record_unknown_query) and ensure notification logic works.
#
# How to Run:
#   python tests/test_tools.py
#
# Expected Output:
#   Prints result dictionaries from each function.
#   Console will show which notification channels are active or skipped.
# ------------------------------------------------------------------------------
import sys
import os


from dotenv import load_dotenv



# Ensure app/ is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load .env if available
load_dotenv()

from app.tools import record_user_details, record_unknown_query

if __name__ == "__main__":
    print(record_user_details("alice@example.com", name="Alice", notes="Interested in beta access"))
    print(record_unknown_query("Can Girma relocate to Germany?"))
