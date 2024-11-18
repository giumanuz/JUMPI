import os
from functools import cache
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.Client(api_key=os.getenv("OPENAI_API_KEY")) 

@cache
def get_correction_system_prompt() -> str:
    with open("gpt/prompts/is_caption.md", "r") as f:
        return f.read()
    
def is_caption(paragraph: str) -> bool:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": get_correction_system_prompt()},
                {"role": "user", "content": paragraph}
            ],
            max_tokens=16384,
            temperature=0.2
        )
        content = response.choices[0].message.content
        if 'yes' in content:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error in API request: {e}")
        return None

