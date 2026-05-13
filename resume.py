import streamlit as st
import pdfplumber
import re

from nltk.corpus import stopwords
import nltk

# Download only stopwords (safe)
nltk.download('stopwords')

# ---------------- UI ----------------
st.set_page_config(page_title="ATS Resume Scanner")
st.title("ATS Resume Scanner")
st.write("Upload Resume & Compare with Job Description")

# ---------------- Upload Resume ----------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ---------------- Job Description ----------------
job_description = st.text_area("Paste Job Description")

# ---------------- Extract PDF Text ----------------
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

# ---------------- Clean Text (NO NLTK TOKENIZER) ----------------
def preprocess(text):
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)   # SAFE TOKENIZER

    stop_words = set(stopwords.words("english"))

    clean_tokens = []
    for word in tokens:
        if word not in stop_words:
            clean_tokens.append(word)

    return clean_tokens

# ---------------- SKILL DATABASE ----------------
SKILL_DB = [
    "python", "sql", "excel", "pandas", "numpy",
    "machine", "learning", "data", "analysis",
    "power", "bi", "tableau", "statistics",
    "aws", "docker", "git", "nlp", "streamlit",
    "javascript", "react", "html", "css"
]

# ---------------- Extract Skills ----------------
def extract_skills(tokens):
    skills = []
    for word in tokens:
        if word in SKILL_DB:
            skills.append(word)
    return list(set(skills))

# ---------------- ATS SCORE ----------------
def ats_score(resume_skills, jd_skills):

    matched = []

    for skill in jd_skills:
        if skill in resume_skills:
            matched.append(skill)

    if len(jd_skills) == 0:
        return 0, [], []

    score = (len(matched) / len(jd_skills)) * 100

    missing = []
    for skill in jd_skills:
        if skill not in resume_skills:
            missing.append(skill)

    return round(score, 2), matched, missing

# ---------------- MAIN ----------------
if uploaded_file and job_description:

    # Extract text
    resume_text = extract_text(uploaded_file)

    # st.subheader("📌 Resume Text")
    # st.write(resume_text)

    # Process text
    resume_tokens = preprocess(resume_text)
    jd_tokens = preprocess(job_description)

    # Extract skills
    resume_skills = extract_skills(resume_tokens)
    jd_skills = extract_skills(jd_tokens)

    # ATS Score
    score, matched, missing = ats_score(resume_skills, jd_skills)

    # ---------------- OUTPUT ----------------
    st.subheader("Resume Skills")
    st.write(resume_skills)

    st.subheader("ATS Score")
    st.success(f"{score}% Match")

    st.subheader("✅ Matched Skills")
    st.write(matched)

    st.subheader("❌ Missing Skills")
    st.write(missing)

else:
    st.info("Upload resume and paste job description to get ATS score")