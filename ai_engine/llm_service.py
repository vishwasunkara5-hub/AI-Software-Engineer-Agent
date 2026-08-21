import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = None

if api_key and api_key != "YOUR_ACTUAL_API_KEY_HERE":
    client = OpenAI(api_key=api_key)


def review_code(code: str) -> str:

    if client is None:
        return (
            "AI service is not configured yet. "
            "The local code analyzer is working correctly."
        )

    prompt = f"""
You are an expert software engineer.

Analyze the following Python code.

Give a concise professional code review.

Include:
1. Bugs
2. Code quality problems
3. Security concerns
4. Performance improvements
5. Suggestions for better code

Python code:

{code}
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    return response.output_text