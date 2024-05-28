from typing import Dict, List

import ollama
import streamlit as st

def stream_response(ollama_model:str) -> str:
    stream = ollama.chat(
        model=ollama_model,
        messages=st.session_state['messages'],
        stream=True,
    )

    for chunk in stream:
        yield chunk['message']['content']

if __name__ == '__main__':
    ollama_model = 'tinyllama'

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if prompt := st.text_area("Prompt"):
        st.session_state['messages'].append({'role': 'user', 'content': prompt})
        
        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            response = st.write_stream(stream_response(ollama_model))
            st.session_state['messages'].append({'role': 'assistant', 'content': response})