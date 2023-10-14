from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain.callbacks import get_openai_callback

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

set_llm_cache(InMemoryCache())
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.6, cache=False)

schema = {
    "properties": {
        "question": {"type": "string"},
    },
    "required": ["question"]
}

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()

    if data is None:
        return jsonify(error="No JSON received"), 400

    value = data.get('key', '')

    # chat_template = ChatPromptTemplate.from_messages([
    #     ("human", f'So your friend is saying this about how they felt yesterday. "{value}". You need to follow up how they are feeling about it today. You are asking this as a follow up so when you ask how they are feeling about it today, you need to ask it in the past tense. Your follow up should be consice, empathetic and kind')
    # ])

    chat_template = ChatPromptTemplate.from_messages([
        ("human", f'Yesterday, your friend shared this: "{value}". Today, kindly and empathetically ask them a brief follow-up question to understand how they feel about it now.')
    ])

    # chat_template = ChatPromptTemplate.from_messages([
    #     ("human", f'Yesterday, your friend shared this: "{value}". Acknowledge their situation or emotion first, then ask a brief follow-up question about how they feel today.')
    # ])

    # chat_template = ChatPromptTemplate.from_messages([
    #     ("human", f'Yesterday, your friend shared this: "{value}". Acknowledge their situation or emotion first, then ask a brief follow-up question about how they feel today.')
    # ])



    messages = chat_template.format_messages(value=value)
    response = llm(messages)
    question = response.content if response else "No question extracted"
    return jsonify(extracted_data=question)

if __name__ == '__main__':
    app.run(debug=True)
