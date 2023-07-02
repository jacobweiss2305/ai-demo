from dotenv import load_dotenv

load_dotenv()

import os

from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI

import pandas as pd

import Levenshtein

def find_best_match(string, file_list):
    best_match = None
    best_score = float('inf')

    for file_name in file_list:
        score = Levenshtein.distance(string, file_name)
        if score < best_score:
            best_score = score
            best_match = file_name

    return best_match

def qa(file_path, prompt):

    loader = TextLoader(file_path)

    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

    return qa.run(prompt)

def is_valid_file_path(file_path):
    return os.path.isfile(file_path)

def load_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text
