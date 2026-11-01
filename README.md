# Automated Resume Analyzer

Upload a resume, compare it with a job description, and get a **match score** plus a list of **missing skills**.

## Features
- Reads resumes and job descriptions in **PDF, DOCX, TXT**
- Extracts skills from a built-in taxonomy of ~100 skills (with aliases, e.g. `k8s` -> Kubernetes, `C++`, `.NET`)
- Match score = **70% skill coverage** + **30% TF-IDF text similarity**
- Shows matched, missing, and extra skills
- Two interfaces: **CLI** and **Streamlit web app**

## Requirements
- Python **3.9 or newer**

## Setup (macOS)

### 1. Check Python
Open **Terminal** (Cmd+Space, type "Terminal") and run:
```bash
python3 --version
```
If Python is missing or older than 3.9, install it with Homebrew (`brew install python`) or from [python.org](https://www.python.org/downloads/).

### 2. Unzip and open the project
```bash
cd ~/Downloads
unzip resume_analyzer.zip
cd resume_analyzer
```
Adjust the first line if the zip is somewhere other than Downloads.

### 3. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
Your prompt will now start with `(venv)`.

### 4. Install the dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the tests
```bash
pytest -q
```
You should see `9 passed`.

### Returning later
Each time you open a new Terminal window, reactivate the environment before running anything:
```bash
cd ~/Downloads/resume_analyzer
source venv/bin/activate
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
A browser tab opens at `http://localhost:8501`. If Streamlit asks for your email on first run, press Enter to skip.

### As a library
```python
from analyzer import analyze, extract_text

result = analyze(extract_text("resume.pdf"), extract_text("jd.txt"))
print(result.match_score, result.missing_skills)
```

## Troubleshooting (macOS)
- **`command not found: python`**: outside the virtual environment use `python3` and `pip3`. Inside the activated environment, plain `python` and `pip` work.
- **"externally-managed-environment" error**: you ran `pip install` without activating the virtual environment. Run `source venv/bin/activate` first.
- **`xcrun: error` or a developer tools prompt**: run `xcode-select --install`, wait for it to finish, then retry.
- **Port already in use**: run `streamlit run app.py --server.port 8502`.
- **"No text could be extracted"**: the PDF is a scan or image. Use a text-based PDF, or export the resume as DOCX.

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
- Every skill in the job description is treated as required, so "Flask or Django" lists Django as missing even if you know Flask.
