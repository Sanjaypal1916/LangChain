import streamlit as st
import requests

def get_response(question):
    url = "http://localhost:8080/ollama/bot/invoke"
    res = requests.post(url, json={"input" : {"question": question}})
    print("Status Code:", res.status_code)
    print("Response JSON:", res.json())  # log the actual response
    return res.json().get('text', "❌ No 'output' key in response")

def response(question):
    url = "http://localhost:8080/ollama/bot/invoke"
    res = requests.post(url, json={"input": {"question": question}})
    print("Status Code:", res.status_code)
    response_json = res.json()
    print("Response JSON:", response_json)  # log the actual response

    try:
        # Extract the text from the nested generation
        text_output = response_json["output"]
    except (KeyError, IndexError) as e:
        text_output = "❌ Failed to parse generated text from response"
        print("Error extracting text:", e)

    return text_output

st.title("The GirlFriend Chatbot")
question = st.text_input("Enter your feelings here:")
onoff=  st.button("submit")

if onoff:
    st.header(response(question))