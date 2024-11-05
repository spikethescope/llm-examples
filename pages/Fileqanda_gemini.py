import streamlit as st
import google.generativeai as genai
import os

# Sidebar for API key input
with st.sidebar:
    gemini_api_key = st.text_input("Google Gemini API Key", key="file_qa_api_key", type="password")
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

st.title("📝 File Q&A with Google Gemini")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not gemini_api_key:
    st.info("Please add your Google Gemini API key to continue.")

if uploaded_file and question and gemini_api_key:
    article = uploaded_file.read().decode()
    
    # Set up the Google Gemini client
    genai.configure(api_key=gemini_api_key)
    
    # Create a prompt for the model
    prompt = f"Here's an article:\n\n{article}\n\n{question}"

    # Call the Google Gemini model
    response = genai.generate(
        prompt=prompt,
        model="gemini-pro",  # Specify the model you want to use
        max_tokens=100,
        stop_sequences=["\n"]
    )
    
    # Display the response from the model
    st.write("### Answer")
    st.write(response.text)
