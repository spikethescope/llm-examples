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
    math_symbols = ['=', '+', '-', '×', '*', '* ', '/', '÷', '±', '∑', '∫', '√', '^', '≠', '≤', '≥', '≈', '∞', '∆', '∂']
    return any(symbol in text for symbol in math_symbols) or '$' in text or any(char.isdigit() for char in text)
    
if uploaded_file and question and gemini_api_key:
    #article = uploaded_file.read().decode()
    
    # Set up the Google Gemini client
    genai.configure(api_key=gemini_api_key)
    
    # Create a prompt for the model
    prompt = f"Here's an article:\n\n{article}\n\n{question}"

    # Call the Google Gemini model
    # Call the Google Gemini model
    response = model.generate_content(prompt)
    
    # Display the response from the model
    st.write("### Answer")
    
    steps = response.text.split('\n')
    
    for step in steps:
        if step.strip():  # Only process non-empty steps
            # Check for important intermediate steps or final answer
            # by looking for keywords or patterns
            if any(keyword in step.lower() for keyword in ['therefore', 'result', 'final', 'answer', '=', 'solution']):
                # Box with light blue background for important steps/answers
                st.markdown(f"""
                <div style="border:1px solid #acc7ed; 
                            padding:15px; 
                            border-radius:5px; 
                            margin:10px 0; 
                            background-color:#e6f0ff;
                            color: #000000;">
                {step}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Regular step - no box, but preserve LaTeX formatting if present
                if '$' in step:
                    # Only apply LaTeX formatting to mathematical content
                    if is_mathematical(step):
                        # Remove any markdown bold syntax
                        step = step.replace("**", "")
                        
                        if '$' in step:
                            # If already in LaTeX format, just display it
                            st.latex(step.replace('$', ''))
                        else:
                            # Convert to LaTeX format for mathematical expressions
                            # Replace common math operators with LaTeX equivalents
                            formatted_step = step
                            formatted_step = formatted_step.replace("×", "\\times ")
                            formatted_step = formatted_step.replace("÷", "\\div ")
                            formatted_step = formatted_step.replace("√", "\\sqrt")
                            
                            # If it's an equation with =, use align* environment
                            if '=' in formatted_step:
                                formatted_step = f"\\begin{{align*}}{formatted_step}\\end{{align*}}"
                            else:
                                formatted_step = f"$${formatted_step}$$"
                            
                            st.latex(formatted_step)
                else:
                    st.write(step)                      
                
    
