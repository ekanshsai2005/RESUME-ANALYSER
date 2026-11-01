"""Compare a resume against a job description and score the match."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skills import extract_skills

SKILL_WEIGHT = 0.7   # share of the final score from skill coverage
TEXT_WEIGHT = 0.3    # share from overall text similarity


@dataclass
class AnalysisResult:
    match_score: float                 # 0-100 overall
    skill_score: float                 # 0-100 JD skill coverage
    text_similarity: float             # 0-100 TF-IDF cosine similarity
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    extra_skills: list[str] = field(default_factory=list)   # on resume, not asked for
    verdict: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def text_similarity(resume: str, jd: str) -> float:
    """TF-IDF cosine similarity in [0, 1]."""
    try:
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        matrix = vec.fit_transform([resume, jd])
        return float(cosine_similarity(matrix[0], matrix[1])[0][0])
    except ValueError:  # empty vocabulary
        return 0.0


def _verdict(score: float) -> str:
    if score >= 80:
        return "Excellent match - apply with confidence."
    if score >= 60:
        return "Good match - highlight the missing skills if you have them."
    if score >= 40:
        return "Partial match - consider upskilling or tailoring your resume."
    return "Weak match - significant gaps against this job description."


def analyze(resume_text: str, jd_text: str) -> AnalysisResult:
    if not resume_text.strip() or not jd_text.strip():
        raise ValueError("Both resume and job description must be non-empty.")

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra = sorted(resume_skills - jd_skills)

    sim = text_similarity(resume_text, jd_text)

    if jd_skills:
        skill_cov = len(matched) / len(jd_skills)
        overall = SKILL_WEIGHT * skill_cov + TEXT_WEIGHT * sim
    else:  # JD mentions no known skills: fall back to text similarity only
        skill_cov = 0.0
        overall = sim

    overall_pct = round(overall * 100, 1)
    return AnalysisResult(
        match_score=overall_pct,
        skill_score=round(skill_cov * 100, 1),
        text_similarity=round(sim * 100, 1),
        matched_skills=matched,
        missing_skills=missing,
        extra_skills=extra,
        verdict=_verdict(overall_pct),
    )
