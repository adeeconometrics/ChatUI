from typing import Any
from time import sleep
import json
import requests
from urllib.error import HTTPError

import streamlit as st


def chat_ui() -> None:
    st.title("Mr. Frank for CodeAssist")
    st.write("Welcome to the chat! I'm Mr. Frank, ask away!")

    user_input = st.text_input("User Input")

    headers =  {
        'Content-Type': 'application/json',
    }

    data = {
        'model': "gemma:2b",
        'stream': False,
        'prompt': user_input,
    }

    # Send button
    if st.button("Send"):
        # response = process_input("http://localhost:11434/api/generate",user_input)
        api_response  = requests.post('http://localhost:11434/api/generate', headers=headers, data=json.dumps(data))

        placeholder = st.empty()


        try:
            # response_text = api_response.text
            # response = json.loads(response_text)["response"]
            for line in api_response.iter_lines():
                if line:
                    response = json.loads(line)["response"]
                        
                for i in range(len(response)):
                    placeholder.markdown("LLama: "+ response[:i+1])
                    sleep(.025)
            # st.write("LLama: ", response)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')

def process_input(api_url:str, input:Any) -> str:
    # Add your logic to process user input and generate response
    # For example, you can use a chatbot library or write your own logic here

    return "This is a sample response"

if __name__ == '__main__':
    chat_ui()