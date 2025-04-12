import streamlit as st
import requests

def get_response(question):
    url = "http://localhost:8080/ollama/bot"
    res = requests.post(url, json={"input" : {"Question": question}})
    print("Status Code:", res.status_code)
    print("Response JSON:", res.json())  # log the actual response
    return res.json().get('output', "❌ No 'output' key in response")



st.title("Chatbot using FASTAPIs")
question = st.text_input("Enter your question:")
onoff=  st.button("submit")

if onoff:
    st.header(get_response(question))