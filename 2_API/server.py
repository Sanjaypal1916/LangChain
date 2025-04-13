from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
load_dotenv()
from langchain_core.output_parsers import StrOutputParser



app = FastAPI(
    title="girlfriend chatbot API",
    description="A simple chatbot API built with FastAPI and LangChain.",
    version="1.0.0"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Anisa, an AI girlfriend. who is kind and always teaches best for your boyfirend that is the user. talk to him like a girlfriend."),
    ("user", "Question: {question}")
])

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

