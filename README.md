# AI Test Generator

A tool that takes an API definition as JSON input, uses an LLM to generate test scenarios and `pytest` code, saves the test file, and runs `pytest` automatically.

## Requirements
- Python 3.10+
- Gemini API Key

## Installation
1. Clone the repository.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your environment variables:
   Copy `.env.example` to `.env` and add your Gemini API Key.
   ```bash
   cp .env.example .env
   ```

## How to Run
Run the main script:
```bash
python app/main.py
```

## Example Input and Output
The tool parses an API JSON object such as:
```json
{
  "method": "POST",
  "url": "/create-user",
  "body": { "name": "string", "email": "string" }
}
```

It outputs the generated test file into the `tests/` folder and prints the `pytest` results directly to your console!
