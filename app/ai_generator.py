import os
import re
from google import genai

def load_env():
    """
    Manually load environment variables from .env file to avoid
    external dependencies outside of standard library for this task.
    """
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def generate_tests(parsed_api: dict | None = None, image=None, custom_prompt: str = "") -> str:
    """
    Calls the OpenAI API to generate test scenarios and pytest code based
    on the prompt template and parsed API details.
    Extracts and returns the Python code block from the response.
    """
    # Load .env file
    load_env()

    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env or environment variables.")
    
    client = genai.Client(api_key=api_key)

    contents = []

    if parsed_api:
        # Read prompt template
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'test_prompt.txt')
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()

        # Format the prompt
        prompt = prompt_template.format(
            method=parsed_api.get('method', ''),
            url=parsed_api.get('url', ''),
            body=parsed_api.get('body', '')
        )
        contents.append(prompt)

    if custom_prompt:
        contents.append(f"Additional Instructions:\n{custom_prompt}")

    if not contents and not image:
        contents.append("Generate some basic test examples since no input was provided.")

    if image:
        contents.append(image)

    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )

    content = response.text

    # Parse out the python code block
    match = re.search(r'```python(.*?)```', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback to general code block, or the content itself if no block
    match_general = re.search(r'```(.*?)```', content, re.DOTALL)
    if match_general:
        return match_general.group(1).strip()
        
    return content.strip()
