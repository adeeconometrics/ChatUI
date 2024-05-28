from base64 import b64encode
from pathlib import Path
from uuid import UUID

from langchain_core.outputs import LLMResult
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain.callbacks.base import BaseCallbackHandler


class StreamingChatCallbackHandler(BaseCallbackHandler):
    def __init__(self, t_name:str, t_imgb64:str) -> None:
        self.t_name = t_name
        self.t_imgb64 = t_imgb64
    
    def on_llm_start(self, *args, **kwargs) -> None:
        self.container = st.empty()
        self.text = ""

    # def on_llm_end(self, response: LLMResult, **kwargs: Ollama):
    #     print(f"llm ended with response")
    #     st.session_state.chat_history.append(AIMessage(response))

    def on_llm_new_token(self, token:str, *args, **kwargs) -> None:
        self.text += token
        self.container.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <img src="data:image/png;base64,{self.t_imgb64}" alt="{self.t_name}" style="width: 32px; height: 32px; border-radius: 50%; margin-right: 1rem;">
                <div>
                    <strong>{self.t_name}</strong>
                    <p>{self.text}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def chat_message(name:str, message:str, avatar_path:Path):
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <img src="data:image/png;base64,{avatar_path}" alt="{name}" style="width: 32px; height: 32px; border-radius: 50%; margin-right: 1rem;">
        <div>
            <strong>{name}</strong>
            <p>{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def image_to_base64(image_path:Path):
    with open(image_path, "rb") as img_file:
        return b64encode(img_file.read()).decode()

def get_response(user_query, chat_history, t_name, t_imgb64) -> str:
    template = """
    You are a helpful assistant named Mr. Frank. You are here to help me with my code. Answer the following questions considering the chat history.

    Chat history: {chat_history}
    User query: {user_query}
    """

    prompt = ChatPromptTemplate.from_template(template=template)

    llm = Ollama(
        model = 'codegemma:2b', callbacks=[StreamingChatCallbackHandler(t_name, t_imgb64)]
    )
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        'chat_history': chat_history,
        'user_query': user_query
    })

if __name__ == "__main__":
    user_avatar = image_to_base64("img/CreamFruitMono.ico")
    ai_avatar = image_to_base64("img/FrankFruitMono.ico")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            AIMessage("Hello, I'm Mr. Frank, how can I help you today?")
        ]

    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            chat_message('Mr. Frank', message.content, avatar_path=ai_avatar)
        elif isinstance(message, HumanMessage):
            chat_message('User: ', message.content, avatar_path=user_avatar)

    user_input = st.chat_input("I'm Mr. Frank, how can I help you today?")
    if user_input is not None and user_input != '':
        st.session_state.chat_history.append(HumanMessage(user_input))

        chat_message('User: ', user_input, avatar_path=user_avatar)
        
        response = get_response(user_input, st.session_state.chat_history, "Mr. Frank", ai_avatar)
        st.session_state.chat_history.append(AIMessage(response))