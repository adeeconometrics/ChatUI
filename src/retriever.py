import streamlit as st

from langchain_community.llms import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain.text_splitter import CharacterTextSplitter


def ask_document(urls: str, question: str, llm: Ollama, embeddings: OllamaEmbeddings) -> str:
    urls_list = urls.split("\n")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1024, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)

    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name = 'rag_chroma',
        embedding=embeddings,
    )
    retriever = vectorstore.as_retriever()

    template = """
        Answer the question based on the following context:
        {context}
        Question: {question}
    """

    prompt = ChatMessagePromptTemplate.from_template(template=template)
    chain = (
        {"context": retriever, "question": question}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(question)

if __name__ == '__main__':

    llm = Ollama(model='tinyllama')
    embeddings = OllamaEmbeddings(model='tinyllama')

    st.title("Document Query with Ollama")
    st.write("Enter URLs (one per line) and a question to query the documents.")

    # Input fields
    urls = st.text_area("Enter URLs separated by new lines", height=150)
    question = st.text_input("Question")

    # Button to process input
    if st.button('Query Documents'):
        with st.spinner('Processing...'):
            answer = ask_document(urls, question, llm, embeddings)
            st.text_area("Answer", value=answer, height=300, disabled=True)
