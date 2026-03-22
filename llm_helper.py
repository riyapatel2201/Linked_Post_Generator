import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st

# Check if running in a local machine or Streamlit cloud
if 'STREAMLIT_RUNTIME' in os.environ:
    # Running on Streamlit Server, fetch secrets from Streamlit's secrets
    groq_api_key = st.secrets["GROQ_API_KEY"]
else:
    # Running locally, load secrets from .env file
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize ChatGroq with the API key
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

if __name__ == "__main__":
    response = llm.invoke("Two most important ingredients in samosa are ")
    print(response.content)