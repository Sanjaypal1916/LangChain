from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
load_dotenv()
from langchain_core.output_parsers import StrOutputParser

## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGSMITH_API_KEY")


app = FastAPI(
    title="Chatbot API",
    description="A simple chatbot API built with FastAPI and LangChain.",
    version="1.0.0"
)

prompt = ChatPromptTemplate.from_messages("user", "QUestion : {question}")

llm = Ollama(model="llama2")
output = StrOutputParser()
chain = prompt|llm|output

add_routes(
    app,
    prompt|llm,
    path="/ollama/bot"
)

if __name__ == "__main__":
    uvicorn.run(app, host= "localhost", port = 8080)
