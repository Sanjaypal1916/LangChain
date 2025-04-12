from fastapi import FastAPI
from langchain_community_llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os 
import dotenv import load_dotenv

load_dotenv()

## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGSMITH_API_KEY")
app = FastAPI(
    title="Chatbot API",
    description="A simple chatbot API built with FastAPI and LangChain.",
    version="1.0.0"
)