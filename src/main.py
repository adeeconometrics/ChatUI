from typing import Any
from time import sleep
from os import path
import json
import requests
from urllib.error import HTTPError

import streamlit as st


def chat_ui() -> None:
    st.title("Mr. Frank for CodeAssist")

    # script_dir = path.dirname(__file__)
    # fin_path = path.join(script_dir, "../img/FinFruit.jpg")
    # frank_path = path.join(script_dir, "../img/FrankFruit.jpg")
    # fin_abs_path = path.join(script_dir, fin_path)
    # frank_abs_path = path.join(script_dir, frank_path)

    # input_col, output_col = st.columns(2)
    # input_col.markdown(frank_abs_path)
    # user_input = input_col.text_input("Input")

    # output_col.image(fin_abs_path)
    # placeholder = output_col.empty()

    user_input = st.chat_input("I'm Mr. Frank, how can I help you today?")
    if user_input:
        st.write("User: ", user_input)

        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'model': "llama3",
            'stream': False,
            'prompt': user_input,
        }

        api_response = requests.post(
            'http://localhost:11434/api/generate', headers=headers, data=json.dumps(data))

        placeholder = st.empty()

        try:
            # response_text = api_response.text
            # response = json.loads(response_text)["response"]
            for line in api_response.iter_lines():
                if line:
                    response = json.loads(line)["response"]

                for i in range(len(response)):
                    placeholder.markdown("Mr. Frank: \n" + response[:i+1])
                    sleep(.025)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')


if __name__ == '__main__':
    chat_ui()
