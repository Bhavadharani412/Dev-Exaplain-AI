import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# -----------------------------
# Config
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="DevExplain AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Theme
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}
.main {
    background: #000000;
    color: #f3f3f3;
}
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
h1, h2, h3 {
    color: #ffffff;
}
.hero-box {
    padding: 2rem;
    border: 1px solid #242424;
    border-radius: 20px;
    background: linear-gradient(180deg, #111111 0%, #0a0a0a 100%);
}
.metric-card {
    padding: 1rem;
    border-radius: 18px;
    border: 1px solid #222222;
    background: #111111;
    text-align: center;
}
.feature-card {
    padding: 1.2rem;
    border-radius: 18px;
    border: 1px solid #222222;
    background: #111111;
    min-height: 150px;
}
.stButton > button {
    width: 100%;
    border-radius: 14px;
    background: #e9204f;
    color: white;
    border: none;
    padding: 0.8rem 1rem;
    font-weight: 700;
}
.stButton > button:hover {
    background: #ff2e63;
}
div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
    background: #111111;
    color: #f3f3f3;
    border-radius: 14px;
}
hr {
    border-color: #1d1d1d;
}
</style>
""", unsafe_allow_html=True)

if not api_key:
    st.error("Missing GROQ_API_KEY in .env file")
    st.stop()

client = Groq(api_key=api_key)
MODEL_NAME = "llama-3.3-70b-versatile"

# -----------------------------
# Helpers
# -----------------------------
def ask_groq(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior engineer, architect, coding mentor and technical writer. Return polished markdown responses."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=4096
        )
        return completion.choices[0].message.content
    except Exception as error:
        return f"Error: {str(error)}"


def analysis_prompt(language: str, code: str) -> str:
    return f"""
Analyze this {language} code.
Return markdown with:
# Summary
# Why This Approach
# Dry Run
# Algorithm Pattern
# Time Complexity
# Space Complexity
# Edge Cases
# Optimizations
# Improved Code

Code:
```{language.lower()}
{code}
```
"""


def article_prompt(language: str, code: str) -> str:
    return f"""
Turn this {language} code into a clean Hashnode markdown article.
Include:
# Title
# Intro
# Problem
# Code
# Explanation
# Dry Run
# Complexity
# Optimizations
# Final Thoughts

Code:
```{language.lower()}
{code}
```
"""


def repo_prompt(url: str) -> str:
    return f"""
Analyze this GitHub repository URL:
{url}

Return:
# Project Summary
# Likely Stack
# Folder Responsibilities
# Architecture
# Improvements
# Onboarding Guide
"""

# -----------------------------
# Navbar
# -----------------------------
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("## 🚀 DevExplain AI")
with col2:
    st.caption("Free Plan · Personal Use")

# -----------------------------
# Hero Section
# -----------------------------
st.markdown("""
<div class='hero-box'>
<h1>Understand Any Codebase in Seconds</h1>
<p>AI-powered code explanations, GitHub repository insights, and technical blog generation for developers and students.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("<div class='metric-card'><h3>100+</h3><p>Analyses Ready</p></div>", unsafe_allow_html=True)
with m2:
    st.markdown("<div class='metric-card'><h3>3x</h3><p>Faster Understanding</p></div>", unsafe_allow_html=True)
with m3:
    st.markdown("<div class='metric-card'><h3>Free</h3><p>Powered by Groq</p></div>", unsafe_allow_html=True)

st.write("")

f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("<div class='feature-card'><h3>Code Analyzer</h3><p>Paste code and get logic, dry run, complexity, and optimization insights.</p></div>", unsafe_allow_html=True)
with f2:
    st.markdown("<div class='feature-card'><h3>Repo Review</h3><p>Understand public GitHub repositories faster with architecture summaries.</p></div>", unsafe_allow_html=True)
with f3:
    st.markdown("<div class='feature-card'><h3>Hashnode Writer</h3><p>Turn code into clean technical articles instantly.</p></div>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# Main Product Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Analyze Code", "Generate Article", "Review Repo"])

with tab1:
    lang = st.selectbox("Language", ["Java", "Python", "JavaScript", "TypeScript", "C++", "C", "Go", "PHP"])
    code = st.text_area("Paste Code", height=420)
    if st.button("Analyze Now"):
        if code.strip():
            with st.spinner("Analyzing..."):
                st.markdown(ask_groq(analysis_prompt(lang, code)))
        else:
            st.warning("Paste code first.")

with tab2:
    lang2 = st.selectbox("Language ", ["Java", "Python", "JavaScript", "TypeScript", "C++", "C", "Go", "PHP"])
    code2 = st.text_area("Paste Code ", height=420)
    if st.button("Generate Blog"):
        if code2.strip():
            with st.spinner("Writing article..."):
                result = ask_groq(article_prompt(lang2, code2))
                st.markdown(result)
                st.download_button("Download Markdown", result, file_name="hashnode.md")
        else:
            st.warning("Paste code first.")

with tab3:
    repo = st.text_input("GitHub Repo URL", placeholder="https://github.com/user/repo")
    if st.button("Review Repository"):
        if repo.strip():
            with st.spinner("Reviewing repo..."):
                st.markdown(ask_groq(repo_prompt(repo)))
        else:
            st.warning("Paste URL first.")

st.divider()
st.caption("Built by Bhava . DevExplain AI")