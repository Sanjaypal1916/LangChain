from langchain.prompts import ChatPromptTemplate
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os 
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA

load_dotenv()

groq_env = os.getenv("GROQ_API_KEY") 
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

model = ChatGroq(api_key=groq_env, model = "gemma2-9b-it")
prompt = ChatPromptTemplate.from_template("""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}
""")



prompt_template="""
Use the following piece of context to answer the question asked.
Please try to provide the answer only based on the context

{context}
Question:{question}

Helpful Answers:
 """
prompt_QA=PromptTemplate(template=prompt_template,input_variables=["context","question"])

st.title("app using Googles Gemma model")
input_prompt = st.text_input("enter your Question here")

def document_prepare():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
        st.session_state.loader = PyPDFDirectoryLoader("./census")
        st.session_state.data = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200)
        st.session_state.final_document = st.session_state.text_splitter.split_documents(st.session_state.data[:20])
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_document, st.session_state.embeddings)

if st.button("document"):
    document_prepare()
    st.text("docuemnt prepared")

if input_prompt and st.button("dochain"):
    document_chain = create_stuff_documents_chain(llm = model, prompt=prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrival_chain = create_retrieval_chain(retriever, document_chain)
    response = retrival_chain.invoke({"input": input_prompt})
    st.text(response["answer"])

    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")

if input_prompt and st.button("retrivalQA"):
    retriever = st.session_state.vectors.as_retriever()
    retrive = RetrievalQA( llm=model,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt":prompt_QA}
    )
    ans = retrive.invoke({"query": input_prompt})
    ans["result"]

    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")



