import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_objectbox.vectorstores import ObjectBox
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv

load_dotenv()


groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")

prompt=ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions:{input}

    """
)


st.title("RAG using GROQ and objectbox")


def prepare():
    if "vectors" not in st.session_state:
        st.session_state.embedding = OllamaEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader(".\census")
        st.session_state.doc = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_doc = st.session_state.text_splitter.split_documents( st.session_state.doc[:20])
        st.session_state.vectors = ObjectBox.from_documents(st.session_state.final_doc,st.session_state.embedding, embedding_dimensions=768 )




input_prompt = st.text_input("enter your question here")
if st.button("Documents Embedding"):
    prepare()
    st.write("ObjectBox Database is ready")

if input_prompt:
    document_chain = create_stuff_documents_chain(llm, prompt )
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": input_prompt})
    st.write(response["answer"])
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")