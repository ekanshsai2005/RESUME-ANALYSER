import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analyzer import analyze, extract_text
from analyzer.skills import extract_skills

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_extract_skills_special_tokens():
    found = extract_skills("Experienced in C++, C#, .NET and Node.js. Also Java (not JavaScript).")
    assert {"C++", "C#", ".NET", "Node.js", "Java"} <= found


def test_word_boundaries():
    # 'java' must not match inside 'javascript'; 'go' alone is not a skill
    found = extract_skills("I know JavaScript and love to go hiking")
    assert "JavaScript" in found
    assert "Java" not in found
    assert "Go" not in found


def test_identical_text_scores_high():
    text = "Python developer with SQL, Docker and AWS experience."
    r = analyze(text, text)
    assert r.match_score >= 90
    assert r.missing_skills == []


def test_missing_skills_detected():
    r = analyze("I know Python.", "Need Python, Docker and Kubernetes.")
    assert set(r.missing_skills) == {"Docker", "Kubernetes"}
    assert r.matched_skills == ["Python"]


def test_unrelated_scores_low():
    r = analyze("Chef with ten years cooking Italian cuisine.", "Python, Docker, AWS engineer wanted.")
    assert r.match_score < 20


def test_sample_files():
    r = analyze(extract_text(SAMPLES / "resume.txt"), extract_text(SAMPLES / "job_description.txt"))
    assert 0 < r.match_score < 100
    assert "Docker" in r.missing_skills
    assert "Python" in r.matched_skills


def test_empty_input_raises():
    with pytest.raises(ValueError):
        analyze("", "something")


def test_unsupported_and_missing_file(tmp_path):
    bad = tmp_path / "x.exe"
    bad.write_text("hi")
    with pytest.raises(ValueError):
        extract_text(bad)
    with pytest.raises(FileNotFoundError):
        extract_text(tmp_path / "nope.txt")


def test_docx_roundtrip(tmp_path):
    from docx import Document

    d = Document()
    d.add_paragraph("Python and SQL developer")
    p = tmp_path / "r.docx"
    d.save(p)
    assert "Python" in extract_text(p)
