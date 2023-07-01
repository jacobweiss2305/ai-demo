import os
import streamlit as st
import utils
import os
from langchain.llms import OpenAI

llm = OpenAI()

st.title("Entity Resolution Bot")


#


# Get the list of TXT files in the "docs" subdirectory
files = os.listdir("chat-bot-helper\docs")
txt_files = [file for file in files if file.endswith(".txt")]

# Radio button to select the TXT file
selected_file = st.radio("Support documentation:", txt_files)

# Display the content of the selected TXT file
if selected_file:
    file_path = os.path.join("chat-bot-helper\docs", selected_file)
    text = utils.load_text_file(file_path)
    st.text_area("File Content:", text, height=200)

files = os.listdir('chat-bot-helper\docs')

txt_files = [file for file in files if file.endswith(".txt")]

question = st.text_input("Ask a question:")

if question:

    find = f"""
    What is the best document to answer this question: {question}

    Please respond with the file name of the best document.

    Example:
    sample.txt

    """

    best_document = utils.qa("chat-bot-helper\docs\meta.txt", find)

    store_answer_best_document = "best_document.txt"

    with open(store_answer_best_document, 'w') as file:
            file.write(best_document)

    extract_prompt = f"""

    Extract the .txt file name. Do not remove the number or special characters.

    The filename should look like this: 01_sample.txt

    """

    best_file = utils.qa(store_answer_best_document, extract_prompt).replace(" ", "")

    # Example usage
    file_path = f"chat-bot-helper\docs\{best_file}"
    is_valid = utils.is_valid_file_path(file_path)
    
    if is_valid:

        answer_question = utils.qa(f"chat-bot-helper\docs\{best_file}", question)

        
    else:
        answer_question = "Sorry we don't have documentations for that question. I have sent a message to alphatheory support cc'ing you."
        user = "jaweiss2305@gmail.com"
        email_prompt = f"""
        Please respond in a tone as a sassy teenager.
        Please create an email for support@alphatheory.com with the following information:
        This user {user} asked the question: {question}
        Unfortunately, we don't have a document for that question.
        We need to ask the support to create a document for that question and follow up with the user.
        """
        email = llm.predict(email_prompt)

    if answer_question:
        st.text_area("Chat Bot:", answer_question, height=200)

    if email:
        st.text_area("Email to support:", email, height=200)


