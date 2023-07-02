import os
import streamlit as st
import utils
import os
from langchain.llms import OpenAI

llm = OpenAI()

st.title("Entity Resolution Bot")

selected_file  = st.selectbox("Select a file", os.listdir("entity-resolution\docs"))

file_path = os.path.join("entity-resolution\docs", selected_file)
text = utils.load_text_file(file_path)
st.text_area("File Content:", text, height=200)

prompt = st.text_input("Prompt", "What is the ticker, cusip, sedol of the company? Explain why.")

response = utils.qa(file_path, prompt)

st.text_area("Response:", response, height=200)
