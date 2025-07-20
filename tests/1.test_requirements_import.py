# tests/test_requirements_import.py

# ------------------------------------------------------------------------------
# Script: 1.test_requirements_import.py
# Purpose: Test that required Python packages (openai, dotenv) are installed and importable.
#
# How to Run:
#   $ python tests/1.test_requirements_import.py
#
# Expected Output:
#   SUCCESS: openai and dotenv imported successfully.
# ------------------------------------------------------------------------------

def test_imports():
    try:
        import openai
        from dotenv import load_dotenv
        print("SUCCESS: openai and dotenv imported successfully.")
    except ImportError as e:
        print("ERROR: Failed to import a required package:", e)
        exit(1)

if __name__ == "__main__":
    test_imports() 
