from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os 
from dotenv import load_dotenv


# api keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# tracking 
os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")





