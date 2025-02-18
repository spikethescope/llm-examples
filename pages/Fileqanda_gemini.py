import streamlit as st
import google.generativeai as genai
import os
import PyPDF2
# Sidebar for API key input
with st.sidebar:
    gemini_api_key = st.text_input("Enter Google Gemini API Key", key="file_qa_api_key", type="password")
    st.markdown("[View the source code](https://github.com/spikethescope/llm-examples/blob/main/pages/Fileqanda_gemini.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")
model = genai.GenerativeModel("gemini-2.0-flash")
st.title("📝 File Q&A with Google Gemini")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"))

if uploaded_file is not None:     
        # Read and extract text from the PDF
        reader = PyPDF2.PdfReader(uploaded_file)
        article = []
        for page in reader.pages:
            article.append(page.extract_text())
        st.session_state.article = "\n".join(article)
#else:
        # Handle other file types (e.g., txt, md)
        #st.session_state.article = uploaded_file.read().decode()
        
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not gemini_api_key:
    st.info("Please add your Google Gemini API key to continue.")

if uploaded_file and question and gemini_api_key:
    #article = uploaded_file.read().decode()
    
    # Set up the Google Gemini client
    genai.configure(api_key=gemini_api_key)
    
    # Create a prompt for the model
    prompt = f"Here's an article:\n\n{article}\n\n{question}"

    # Call the Google Gemini model
response = model.generate_content(prompt)

# Display the response from the model
st.write("### Answer")

# Split response into steps if it contains multiple parts
steps = response.text.split('\n')

# Display each step in a separate box with LaTeX formatting
for i, step in enumerate(steps, 1):
    if step.strip():  # Only process non-empty steps
        st.markdown(f"""
        <div style="border:1px solid #e1e4e8; padding:10px; border-radius:5px; margin:10px 0; background-color:#f6f8fa;">
        <strong>Step {i}:</strong><br>
        $$\\begin{aligned}
        {step}
        \\end{aligned}$$
        </div>
        """, unsafe_allow_html=True)
Key modifications made:

Added HTML/CSS styling to create boxes around the content
Incorporated LaTeX formatting using $$\begin{aligned}...\end{aligned}$$
Added option to split and display intermediate steps separately
Used st.markdown() instead of st.write() for more formatting control
Added styling for better visual hierarchy
To use this effectively, make sure:

Your Streamlit app has LaTeX support enabled
The response text contains proper LaTeX syntax
If you want to format specific mathematical expressions, they should be properly formatted in LaTeX syntax
If you want to apply different styles to different types of content (like equations vs. text), you can add conditions:

# Call the Google Gemini model
response = model.generate_content(prompt)

# Display the response from the model
st.write("### Answer")

# Split response into steps if it contains multiple parts
steps = response.text.split('\n')

# Display each step in a separate box with LaTeX formatting
for i, step in enumerate(steps, 1):
    if step.strip():  # Only process non-empty steps
        if step.startswith('$'):  # Mathematical expression
            st.markdown(f"""
            <div style="border:1px solid #dce6ff; padding:10px; border-radius:5px; margin:10px 0; background-color:#f0f5ff;">
            <strong>Equation {i}:</strong><br>
            $$\\begin{aligned}
            {step}
            \\end{aligned}$$
            </div>
            """, unsafe_allow_html=True)
        else:  # Regular text
            st.markdown(f"""
            <div style="border:1px solid #e1e4e8; padding:10px; border-radius:5px; margin:10px 0; background-color:#f6f8fa;">
            <strong>Step {i}:</strong><br>
            {step}
            </div>
            """, unsafe_allow_html=True)
