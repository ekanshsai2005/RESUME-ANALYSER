# Automated Resume Analyzer

Upload a resume, compare it with a job description, and get a **match score** plus a list of **missing skills**.

## Features
- Reads resumes and job descriptions in **PDF, DOCX, TXT**
- Extracts skills from a built-in taxonomy of ~100 skills (with aliases, e.g. `k8s` -> Kubernetes, `C++`, `.NET`)
- Match score = **70% skill coverage** + **30% TF-IDF text similarity**
- Shows matched, missing, and extra skills
- Two interfaces: **CLI** and **Streamlit web app**

## Setup
```bash
cd resume_analyzer
pip install -r requirements.txt
```

## Usage

### CLI
```bash
python main.py --resume samples/resume.txt --jd samples/job_description.txt
python main.py -r my_resume.pdf -j jd.docx --json     # JSON output
```

### Web app
```bash
streamlit run app.py
```

### As a library
```python
from analyzer import analyze, extract_text

result = analyze(extract_text("resume.pdf"), extract_text("jd.txt"))
print(result.match_score, result.missing_skills)
```

## Tests
```bash
pytest -q
```

## Project structure
```
resume_analyzer/
├── analyzer/
│   ├── parser.py    # PDF/DOCX/TXT text extraction
│   ├── skills.py    # skill taxonomy + extraction
│   ├── matcher.py   # scoring logic
│   └── report.py    # text/JSON output
├── main.py          # CLI
├── app.py           # Streamlit UI
├── samples/         # example resume + JD
└── tests/
```

## Customising
- Add skills in `analyzer/skills.py` (`SKILLS` dict: canonical name -> aliases).
- Change the score balance via `SKILL_WEIGHT` / `TEXT_WEIGHT` in `analyzer/matcher.py`.

## Limitations
- Scanned/image-only PDFs need OCR (not included).
- Skill matching is dictionary-based, so skills outside the taxonomy are only reflected in the text-similarity part.
