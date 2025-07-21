# ------------------------------------------------------------------------------
# Script: 2.test_env_loading.py
# Purpose: Validate that the OpenAI API key is correctly loaded from a `.env` file.
#
# How to Run:
#   $ python tests/2.test_env_loading.py
#
# Expected Output:
#   UCCESS: OPENAI_API_KEY loaded from .env
#
# ------------------------------------------------------------------------------

def test_env():
    import os
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("SUCCESS: OPENAI_API_KEY loaded from .env")
    else:
        print("ERROR: OPENAI_API_KEY not found in environment")
        exit(1)

if __name__ == "__main__":
    test_env()
