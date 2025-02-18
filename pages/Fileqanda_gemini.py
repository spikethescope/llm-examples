import streamlit as st
import google.generativeai as genai
import os
import PyPDF2
# Sidebar for API key input
with st.sidebar:
    gemini_api_key = st.text_input("Enter Google Gemini API Key", key="file_qa_api_key", type="password")
    st.markdown("[View the source code](https://github.com/spikethescope/llm-examples/blob/main/pages/Fileqanda_gemini.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")
model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")
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
def is_mathematical(text):
    # Check if text contains mathematical symbols or equations
    math_symbols = ['=', '+', '-', '×', '*', '/', '÷', '±', '∑', '∫', '√', '^', '≠', '≤', '≥', '≈', '∞', '∆', '∂']
    return any(symbol in text for symbol in math_symbols) or '$' in text or any(char.isdigit() for char in text)
    
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
    
    steps = response.text.split('\n')

    def format_important_step(step):
        # Remove any markdown bold markers
        step = step.replace('**', '')
        step = step.strip('*')
        # Heuristically check whether the line contains math symbols
        has_math = any(sym in step for sym in ['=', '√', '+', '-', '*', '/', '^'])
        # If it appears to contain math and isn’t already wrapped in LaTeX delimiters, then wrap it.
        if has_math and "" not in step: step = "" + step + "$$"
        return step
    
    for step in steps:
        if step.strip(): # Only process non-empty lines
            # If the step is an important/final step (detected by key phrases)
            if any(keyword in step.lower() for keyword in ['therefore', 'result', 'final', 'answer', '=', 'solution']):
                formatted_step = format_important_step(step)
                 # Display the important step in a box (grey background) using st.markdown with unsafe_allow_html
                st.markdown(f"""
                <div style="border:1px solid #d0d0d0; 
                            padding:15px; 
                            border-radius:5px; 
                            margin:10px 0; 
                            background-color:#f5f5f5;
                            color: #000000;">
                {formatted_step}
                </div>
                """, unsafe_allow_html=True)
            else:
                # For regular steps: if the step contains a '$', assume it is a LaTeX expression and use st.latex
                if '$' in step:
                    st.latex(step.replace('$', ''))
                else:
                    st.write(step)
        
