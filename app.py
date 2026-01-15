import streamlit as st
import google.generativeai as genai
import pypdf

# 1. THE CONFIGURATION
st.set_page_config(page_title="The Brutal Resume Roaster", page_icon="🔥")

# 2. THE UI (User Interface)
st.title("🔥 The Brutal Resume Roaster")
st.subheader("Upload your CV. Get humbled. Get hired.")
st.write("Most resumes are ignored because they are boring. Let's find out why.")

# Sidebar for API Key (Keeps it secure)
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Paste your Google Gemini API Key", type="password")
    st.info("Get your free key at: aistudio.google.com")

# 3. THE FILE UPLOADER
uploaded_file = st.file_uploader("Drop your Resume (PDF only)", type="pdf")

# 4. THE LOGIC
if uploaded_file is not None and api_key:
    # Set up the AI
    genai.configure(api_key=api_key)
    
    # Read the PDF
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()
            
        # 5. THE SYSTEM PROMPT (The Secret Sauce)
        # This tells the AI exactly how to behave.
        prompt = f"""
        You are a ruthless, cynical, Senior Tech Recruiter at a top Fortune 500 company. 
        You have seen 10,000 resumes and you hate 99% of them.
        
        Review the following resume text. 
        
        Your output must be structured like this:
        1. **The First Impression:** Give a brutal 1-sentence summary of the vibe this resume gives off.
        2. **The Roast:** List 3-5 specific things that suck about this resume. Be mean but constructive. Focus on vague metrics, buzzwords, and poor formatting logic.
        3. **The Fix:** Give 3 specific actionable changes that would instantly increase the candidate's salary potential.
        
        Resume Text:
        {text_content}
        """

        # Button to trigger the roast
        if st.button("Roast Me!"):
            with st.spinner("Analyzing your failures..."):
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                st.markdown("### 💀 The Verdict")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Error reading file: {e}")

elif uploaded_file and not api_key:
    st.warning("Please enter your API Key in the sidebar to proceed.")