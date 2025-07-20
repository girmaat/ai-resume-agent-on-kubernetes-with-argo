# tests/test_requirements_import.py

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
