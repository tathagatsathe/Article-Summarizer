import streamlit as st
import requests
import json
from newspaper import Article
import time
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Article Summarizer",)

st.title("News Article Summarizer")

API_KEY = os.getenv('HUGGINGFACE_API_KEY')
headers = {"Authorization": f"Bearer {API_KEY}"}

default_url = ""
url = st.text_input('URL: ', default_url)

def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if st.button('Summarize'):
    article = Article(url)
    article.download()
    article.parse()
    title = article.title
    text = article.text
    
    
    with st.spinner("Loading"):
        output = query({"inputs":text,})
        st.header(title,divider="gray")
        summary = output[0]['summary_text'].replace('<n>', " ")
        st.write(summary)
