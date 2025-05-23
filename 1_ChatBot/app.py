from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os 
from dotenv import load_dotenv

load_dotenv()
# api keys

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGSMITH_API_KEY")


prompt = ChatPromptTemplate.from_messages([
    ("system", "your name is mira and you are a chatbot that helps users for their queries."),
    ("user", "Question : {question}")
])

llm = ChatOpenAI(model = "gpt-3.5-turbo", temperature = 0.7)
outparser = StrOutputParser()
chain = prompt|llm|outparser


st.title("Chatbot")
st.write("This is a simple chatbot application built with LangChain and Streamlit.")
input  = st.text_input("Enter your question:")

st.write( chain.invoke({"question" : input}))

