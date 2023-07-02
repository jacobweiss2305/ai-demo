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

prompt_text = """ What is the ticker, cusip, sedol of the company? 

Do not mix results. For example you can't pick a SEDOL from one source with a TICKER from another source

"""

st.text_area("Prompt:", prompt_text, height=200)

response = utils.qa(file_path, prompt_text)

st.text_area("Response:", response, height=200)
