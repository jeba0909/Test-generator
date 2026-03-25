import json
import os
from parser import parse_api_input
from ai_generator import generate_tests, load_env
from test_writer import save_test_code
from runner import run_pytest

def main():
    """
    Main entry point for the AI Test Generator.
    Loads JSON API definition, parses it, generates tests via OpenAI,
    writes them to a file, and runs them with pytest.
    """
    # Phase 1: dummy input
    dummy_input = {
        "method": "POST",
        "url": "/create-user",
        "body": { "name": "string", "email": "string" }
    }

    print("--- Loading JSON Input ---")
    print(json.dumps(dummy_input, indent=2))
    
    print("\n--- Parsing Output ---")
    parsed_api = parse_api_input(dummy_input)
    print(f"Method: {parsed_api['method']}")
    print(f"URL: {parsed_api['url']}")
    print(f"Body: {parsed_api['body']}")

    print("\n--- Generating Tests with AI ---")
    # Load env vars from .env file explicitly
    load_env()
    
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️ GEMINI_API_KEY not found!")
        print("Please create a .env file and set GEMINI_API_KEY to run the full AI flow.")
        return

    try:
        print("Calling Gemini API...")
        generated_code = generate_tests(parsed_api)
        print("Tests generated successfully!")
        
        print("\n--- Saving Test Code ---")
        test_file = save_test_code(generated_code, parsed_api['url'])
        print(f"Saved to: {test_file}")
        
        # Run pytest on the generated file
        run_pytest(test_file)
        
    except Exception as e:
        print(f"\n❌ Error during generation or execution: {e}")

if __name__ == "__main__":
    main()
