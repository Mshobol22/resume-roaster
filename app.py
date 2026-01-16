import streamlit as st
import google.generativeai as genai
import pypdf
import time

# --- CONFIGURATION ---
MODEL_NAME = "gemini-2.5-flash" # Change to 'gemini-2.5-flash' if you have access
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
    
    # Smart Key Handling
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        api_key = st.text_input("Enter Gemini API Key", type="password")
        st.caption("Get a free key at aistudio.google.com")

    st.divider()
    
    # MONETIZATION SECTION
    st.header("💎 Premium Access")
    st.write("Unlock the 'Job Matcher' & Detailed Fixes.")
    
    # REPLACE THIS WITH YOUR REAL GUMROAD LINK
    gumroad_link = "https://mustaphashobol.gumroad.com/l/dbidas" 
    
    st.markdown(f"[👉 Get a Premium Code ($5)]({gumroad_link})", unsafe_allow_html=True)
    access_code = st.text_input("Enter Access Code Here")

# --- MAIN INPUTS ---
uploaded_file = st.file_uploader("1. Upload your CV (PDF)", type="pdf")
job_description = st.text_area("2. Paste the Job Description (Optional - Increases Accuracy)")

# --- MAIN LOGIC ---
if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    
    if st.button("🔥 Roast Me!"):
        # FANCY LOADING ANIMATION
        with st.status("🤖 AI Recruiter is reading...", expanded=True) as status:
            st.write("Scanning for buzzwords...")
            time.sleep(1)
            st.write("Comparing against industry standards...")
            time.sleep(1)
            if job_description:
                st.write("Analyzing Job Description match...")
            else:
                st.write("Judging formatting choices...")
            
            try:
                # READ PDF
                pdf_reader = pypdf.PdfReader(uploaded_file)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                
                # --- BUILD THE PROMPT ---
                
                # Step 1: Base Context (Resume vs Job OR Resume vs General)
                if job_description:
                    base_prompt = f"""
                    You are a strict ATS (Applicant Tracking System) and Senior Recruiter.
                    Compare the following Resume to the provided Job Description.
                    
                    Job Description:
                    {job_description}
                    
                    Resume:
                    {text_content}
                    """
                else:
                    base_prompt = f"""
                    You are a brutal Senior Recruiter. Review this resume for general hireability.
                    Resume:
                    {text_content}
                    """

                # Step 2: Output Context (Premium vs Free)
                if access_code == "HIRED2026": # Premium Mode
                    final_prompt = base_prompt + """
                    Output Instructions:
                    1. MATCH SCORE: Give a strictly numerical score (0-100) on how well they match the job/industry.
                    2. MISSING KEYWORDS: List the top 5 critical skills/keywords from the job description that are MISSING in the resume.
                    3. THE ROAST: A 3-sentence ruthless summary of the gap.
                    4. THE FIX: Rewrite the candidate's "Professional Summary" to specifically target this job.
                    5. SALARY ESTIMATE: Estimate the salary range for this role and if this resume justifies the top end.
                    """
                    mode = "Premium"
                else: # Free Mode
                    final_prompt = base_prompt + """
                    Output Instructions:
                    1. MATCH SCORE: Give a strictly numerical score (0-100) on how well they match.
                    2. THE ROAST: A 3-sentence ruthless summary of why they won't get an interview.
                    3. TEASER: Write exactly: "I found 5 critical missing keywords that will auto-reject you from this job. Unlock Premium to see exactly what they are."
                    """
                    mode = "Free"

                # CALL THE AI
                model = genai.GenerativeModel(MODEL_NAME) 
                response = model.generate_content(final_prompt)
                
                # FINISH LOADING
                status.update(label="Roast Complete!", state="complete", expanded=False)
                
                # DISPLAY RESULTS
                st.markdown("### 💀 The Verdict")
                st.write(response.text)
                
                if mode == "Free":
                    st.info("💡 You are viewing the Free version. Enter a code in the sidebar to see the Missing Keywords & Fixes.")
                else:
                    st.success("✨ Premium Analysis Unlocked! Use the keywords above to update your resume.")

            except Exception as e:
                st.error(f"Error: {e}")

elif uploaded_file and not api_key:
    st.warning("Please enter your API Key to proceed.")

# --- FOOTER ---
st.divider()
with st.expander("❓ Frequently Asked Questions"):
    st.write("**Q: Do you save my resume?**")
    st.write("A: No. Your file is processed in memory by Google's AI and immediately forgotten.")
    st.write("**Q: Is this accurate?**")
    st.write("A: It simulates how an ATS (Robot Recruiter) reads your resume. If the AI can't find your skills, neither can the hiring manager.")