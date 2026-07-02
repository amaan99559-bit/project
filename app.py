# ---------------- JOB ROLE SKILL ADVISOR ----------------
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Job Role Skill Advisor",
    page_icon="💼",
    layout="wide"
)

# ---------------- CUSTOM CLEAN CSS ----------------
st.markdown(
    """
    <style>
    body {
        background: #f0f2f6;
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
    }
    /* Title */
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #555555;
        margin-bottom: 25px;
    }
    /* Input bar */
    .stTextInput > div > input {
        border: 2px solid #1a73e8;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 16px;
        width: 60%;
        margin: auto;
        display: block;
    }
    /* Result card */
    .result-card {
        background-color: #ffffff;
        border-left: 5px solid #1a73e8;
        padding: 18px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }
    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #1a73e8, #4285f4);
        color: white;
        border-radius: 8px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #4285f4, #1a73e8);
        transform: scale(1.05);
        box-shadow: 0px 0px 10px rgba(26,115,232,0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>💼 Job Role Skill Advisor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Discover essential skills, their purpose, and learning depth</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
job_role = st.text_input("🔎 Enter a job role (e.g., Data Scientist, Web Developer, Product Manager)", "")

# ---------------- PROCESS ----------------
if job_role:
    if st.button("Generate Skill Plan"):
        if not MISTRAL_API_KEY:
            st.error("❌ Mistral API Key not found. Please add it to the .env file.")
        else:
            with st.spinner("📊 Generating skill roadmap..."):
                llm = ChatMistralAI(mistral_api_key=MISTRAL_API_KEY)

                prompt = ChatPromptTemplate.from_template(
                    """You are an expert career advisor.
                    For the job role: {role}, provide:
                    - A list of essential skill sets (point-wise).
                    - For each skill:
                        * Purpose: one sentence explaining why this skill matters.
                        * Depth: how deeply the user should learn it (basic, intermediate, advanced).
                        * Approach: practical learning suggestions (courses, projects, practice).
                    
                    Format clearly with bullet points and sub-points.
                    """
                )

                chain = prompt | llm | StrOutputParser()
                skill_plan = chain.invoke({"role": job_role})

                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.subheader("📌 Skill Roadmap")
                st.write(skill_plan)
                st.markdown("</div>", unsafe_allow_html=True)

                # Visual depth indicators
                st.subheader("📊 Suggested Learning Depth")
                depth_levels = {
                    "Basic": 0.3,
                    "Intermediate": 0.6,
                    "Advanced": 1.0
                }
                for level, progress in depth_levels.items():
                    st.progress(progress, text=f"{level} mastery")
