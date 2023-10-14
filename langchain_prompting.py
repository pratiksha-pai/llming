import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.globals import set_llm_cache
import json
from langchain.cache import InMemoryCache
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from flask import Flask, request

app = Flask(__name__)

set_llm_cache(InMemoryCache())
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm = OpenAI(openai_api_key=openai_api_key, temperature=0.6, cache=False)

schema = {
    "properties": {
        "question": {"type": "string"},
    },
    "required": ["question"]
}


with open('input.json', 'r') as file:
    data = json.load(file)

value = data['key']

chat_template = ChatPromptTemplate.from_messages([
    ("human", "I want you to summarize {value}. Can you give me a prompt that gives a asks a concise follow up question on this?")
])
messages = chat_template.format_messages(value=value)
llm = ChatOpenAI()
response = llm(messages)
# print(response)

chain = create_extraction_chain(schema, llm)
extracted_data = chain.run(response)

print("extracted data:")
print(extracted_data[0]["question"])
