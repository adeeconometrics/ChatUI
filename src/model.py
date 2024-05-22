import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain.callbacks.manager import CallBackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama

def get_response(user_query, chat_history):
    template = """
    You are a helpful assistant named Mr. Frank. You are here to help me with my code. Answer the following questions considering the chat history.

    Chat history: {chat_history}
    User query: {user_query}
    """

    prompt = ChatPromptTemplate.from_template(template=template)

    llm = Ollama(
        model = 'gemma:2b',
    )
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        'chat_history': chat_history,
        'user_query': user_query
    })

if __name__ == "__main__":
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            AIMessage("Hello, I'm Mr. Frank, how can I help you today?")
        ]

    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message('AI', avatar=st.image('img/FrankFruit.ico')):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('Human', avatar=st.image('img/CreamFruit.ico')):
                st.write(message.content)

    user_input = st.chat_input("I'm Mr. Frank, how can I help you today?")
    if user_input is not None and user_input != '':
        st.session_state.chat_history.append(HumanMessage(user_input))
        
        with st.chat_message("Human", avatar=st.image('img/CreamFruit.ico')):
            st.markdown(f"User: {user_input}")
        with st.chat_message('AI', avatar=st.image('img/FrankFruit.ico')):
            response = get_response(user_input, st.session_state.chat_history)
            st.markdown(f"Mr. Frank: \n{response}")

        st.session_state.chat_history.append(AIMessage(response))