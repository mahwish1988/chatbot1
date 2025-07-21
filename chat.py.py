####################### Answer Generator from Any PDF File #######################

import streamlit as st
import pymupdf
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
from PyPDF2 import PdfReader

# Load environment variables and API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Generative AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to clean and preprocess text
def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip().lower())


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    doc =pymupdf.open(stream=pdf_file.read(), filetype="pdf")  
    for page in doc:
        text += page.get_text("text")
    return clean_text(text)


# Function to generate answers
def generate_answers(content, query):
    prompt = f'''
    Based on the following content:
    {content}
    Answer the following question:
    {query}
    
    Provide a concise and clear answer.
    '''
    
    try:
        response =model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text if response.candidates else "No answer generated."
    except Exception as e:
        return f"Error: {str(e)}"
    

    # Streamlit UI setup
st.set_page_config(page_title="Answer Generator from PDF")
st.header("Generate Answers from PDF")

uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

if 'pdf_content' not in st.session_state:
    st.session_state['pdf_content'] = ""

if uploaded_pdf:
    st.session_state['pdf_content'] = extract_text_from_pdf(uploaded_pdf)
    st.success("PDF content loaded successfully!")

user_query = st.text_input("Enter your question:")

if st.button("Generate Answer") and st.session_state['pdf_content']:
    content = st.session_state['pdf_content']
    answer = generate_answers(content, user_query)

    st.subheader("Generated Answer:")
    st.text(answer)
