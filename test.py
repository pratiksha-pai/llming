import openai
import json
import os
from dotenv import load_dotenv
load_dotenv()

with open('input.json', 'r') as f:
    data = json.load(f)

value = data.get('key', '')
openai.api_key = os.getenv('OPENAI_API_KEY')
prompt = f"Understand the following data: {value}"

response = openai.Completion.create(
    engine="gpt-3.5-turbo",
    prompt=prompt,
    max_tokens=50,
)

question = response['choices'][0]['text'].strip()
generic_question = "Could you provide more details?"
follow_up_question = question if question else generic_question

print(follow_up_question)
