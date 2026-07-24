import streamlit as st
import tempfile, os
from dotenv import load_dotenv
load_dotenv()

from pipeline.parser import parse_pdf
from pipeline.orchestrator import analyze_gap

st.set_page_config(page_title="ResumeMatch AI", page_icon="🎯", layout="wide")
st.title("🎯 ResumeMatch AI")
st.caption("Identify skill gaps between your resume and a job description")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
with col2:
    jd_text = st.text_area("📋 Paste Job Description", height=300)

if st.button("🔍 Analyze Gap", type="primary"):
    if not resume_file or not jd_text.strip():
        st.error("Please upload a resume PDF and paste a job description.")
    else:
        with st.spinner("Analyzing… this takes about 30-60 seconds"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(resume_file.getbuffer())
                tmp_path = tmp.name
            resume_text = parse_pdf(tmp_path)
            os.unlink(tmp_path)
            result = analyze_gap(resume_text, jd_text)

        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("🎯 Overall Score",   f"{result.overall_score()}%")
        c2.metric("🧠 Semantic Match", f"{result.match_score_semantic}%")
        c3.metric("🤖 ATS Score",      f"{result.match_score_ats}%")

        ca, cb = st.columns(2)
        with ca:
            st.subheader("✅ Matched Skills")
            for s in result.matched_skills: st.success(s)
        with cb:
            st.subheader("❌ Missing Skills")
            for s in result.missing_skills: st.error(s)

        if result.rewritten_bullets:
            st.subheader("✍️ Rewritten Bullets")
            for rb in result.rewritten_bullets:
                with st.expander(f"Missing skill: {rb.missing_skill}"):
                    st.write("**Original bullet:**")
                    st.info(rb.original_bullet)
                    st.write("**Rewritten bullet:**")
                    st.success(rb.rewritten_bullet)