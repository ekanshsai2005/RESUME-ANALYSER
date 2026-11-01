"""Streamlit web UI: upload a resume, paste/upload a JD, get a match score.

Run with:  streamlit run app.py
"""
import streamlit as st

from analyzer import analyze, extract_text

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="centered")
st.title("📄 Automated Resume Analyzer")
st.caption("Upload your resume, add a job description, and see how well they match.")

resume_file = st.file_uploader("Resume", type=["pdf", "docx", "txt"])

jd_mode = st.radio("Job description input", ["Paste text", "Upload file"], horizontal=True)
jd_text = ""
if jd_mode == "Paste text":
    jd_text = st.text_area("Job description", height=220)
else:
    jd_file = st.file_uploader("Job description file", type=["pdf", "docx", "txt"], key="jd")
    if jd_file:
        try:
            jd_text = extract_text(jd_file.getvalue(), filename=jd_file.name)
        except ValueError as exc:
            st.error(str(exc))

if st.button("Analyze", type="primary"):
    if not resume_file or not jd_text.strip():
        st.warning("Please provide both a resume and a job description.")
        st.stop()
    try:
        resume_text = extract_text(resume_file.getvalue(), filename=resume_file.name)
        result = analyze(resume_text, jd_text)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    st.subheader(f"Match score: {result.match_score:.0f}%")
    st.progress(min(int(result.match_score), 100))
    st.info(result.verdict)

    c1, c2 = st.columns(2)
    c1.metric("Skill coverage", f"{result.skill_score:.0f}%")
    c2.metric("Text similarity", f"{result.text_similarity:.0f}%")

    st.markdown(f"**✅ Matched skills ({len(result.matched_skills)})**")
    st.write(", ".join(result.matched_skills) or "None")
    st.markdown(f"**❌ Missing skills ({len(result.missing_skills)})**")
    st.write(", ".join(result.missing_skills) or "None - you cover everything listed!")
    with st.expander("Extra skills on your resume"):
        st.write(", ".join(result.extra_skills) or "None")
