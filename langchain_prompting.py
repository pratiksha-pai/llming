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

    chat_template = ChatPromptTemplate.from_messages([
        ("human", f'So your friend is saying this about how they felt yesterday. "{value}". You need to follow up how they are feeling about it today. You are asking this as a follow up so when you ask how they are feeling about it today, you need to ask it in the past tense. Your follow up should be consice, empathetic and kind')
    ])
    messages = chat_template.format_messages(value=value)
    request_tokens = sum(len(message.content.split()) for message in messages)  # Counting tokens in the request

    # request_tokens = sum(len(message.split()) for message in messages)  # Counting tokens in the request

    with get_openai_callback() as cb:  # Utilizing the callback to get token counts
        response = llm(messages)
    response_tokens = cb.total_tokens - request_tokens  # Calculating response tokens by subtracting request tokens from total tokens

    print(f"Request Tokens: {request_tokens}, Response Tokens: {response_tokens}")

    chain = create_extraction_chain(schema, llm)
    print("response", response)
    extracted_data = chain.run(response)

    question = extracted_data[0]["question"] if extracted_data else "No question extracted"

    return jsonify(extracted_data=question, request_tokens=request_tokens, response_tokens=response_tokens)

if __name__ == '__main__':
    app.run(debug=True)
