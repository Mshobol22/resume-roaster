import streamlit as st
import google.generativeai as genai
import pypdf
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Roast My Resume", page_icon="🔥", layout="centered")

# --- CSS FOR BETTER LOOKS ---
st.markdown("""
    <style>
    .big-score { font-size: 80px; font-weight: bold; text-align: center; color: #FF4B4B; }
    .roast-box { border: 2px solid #FF4B4B; padding: 20px; border-radius: 10px; background-color: #ffe6e6; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🔥 The Brutal Resume Roaster")
st.subheader("Is your resume trash? Let an AI Recruiter tell you the truth.")

# --- SIDEBAR: SETTINGS & MONETIZATION ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Smart Key Handling: Tries to find secret key first, asks user if missing
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        api_key = st.text_input("Enter Gemini API Key", type="password")
        st.caption("Get a free key at aistudio.google.com")

    st.divider()
    
    # MONETIZATION SECTION
    st.header("💎 Premium Access")
    st.write("Want the detailed fix? Buy a pass.")
    st.markdown("[👉 Get a Premium Code ($5)](https://gumroad.com)", unsafe_allow_html=True) # Replace with your link later
    access_code = st.text_input("Enter Access Code Here")

# --- MAIN LOGIC ---
uploaded_file = st.file_uploader("Upload your CV (PDF)", type="pdf")

if uploaded_file and api_key:
    # Configure AI
    genai.configure(api_key=api_key)
    
if st.button("🔥 Roast Me!"):
        # 1. Start the fancy loading animation
        with st.status("🤖 AI Recruiter is reading...", expanded=True) as status:
            st.write("Scanning for buzzwords...")
            time.sleep(1) # Fake delay to build suspense
            st.write("Analyzing formatting errors...")
            time.sleep(1)
            st.write("Judging your career choices...")
            
            try:
                # 2. Do the actual work
                pdf_reader = pypdf.PdfReader(uploaded_file)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                
                # 3. Mark loading as done
                status.update(label="Roast Complete!", state="complete", expanded=False)
                
                # 4. Check Access Code (Free vs Premium)
                if access_code == "HIRED2026": 
                    prompt = f"""
                    You are a brutal Senior Recruiter. Review this resume.
                    Output Structure:
                    1. SCORE: Give a strictly numerical score from 0-100 based on hireability. Just the number.
                    2. ROAST: A 3-sentence ruthless summary of why they aren't getting hired.
                    3. RED FLAGS: Bullet points of specific bad habits in the text.
                    4. THE FIX: Rewrite the "Professional Summary" to be 10x better.
                    5. SALARY ESTIMATE: Guess their current salary and what they COULD earn with a better resume.
                    Resume: {text_content}
                    """
                    mode = "Premium"
                else:
                    prompt = f"""
                    You are a brutal Senior Recruiter. Review this resume.
                    Output Structure:
                    1. SCORE: Give a strictly numerical score from 0-100 based on hireability. Just the number.
                    2. ROAST: A 3-sentence ruthless summary of why they aren't getting hired.
                    3. TEASER: Write exactly this sentence: "I found 4 critical errors that are costing you money. Unlock Premium to see how to fix them."
                    Resume: {text_content}
                    """
                    mode = "Free"

                # 5. Call AI
                model = genai.GenerativeModel('gemini-2.5-flash') 
                response = model.generate_content(prompt)
                
                # 6. Display Results
                st.markdown("### 💀 The Verdict")
                st.write(response.text)
                
                if mode == "Free":
                    st.info("💡 You are viewing the Free version. Enter a code in the sidebar to unlock the specific fixes.")
                else:
                    st.success("✨ Premium Analysis Unlocked!")

            except Exception as e:
                st.error(f"Error: {e}")