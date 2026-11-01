"""Render an AnalysisResult as text or JSON."""
from __future__ import annotations

import json

from .matcher import AnalysisResult


def _bar(pct: float, width: int = 30) -> str:
    filled = int(round(pct / 100 * width))
    return "[" + "#" * filled + "-" * (width - filled) + f"] {pct:.1f}%"


def to_text(r: AnalysisResult) -> str:
    lines = [
        "=" * 56,
        " RESUME vs JOB DESCRIPTION - MATCH REPORT",
        "=" * 56,
        f" Overall match : {_bar(r.match_score)}",
        f" Skill coverage: {_bar(r.skill_score)}",
        f" Text similarity: {_bar(r.text_similarity)}",
        "",
        f" {r.verdict}",
        "",
        f" Matched skills ({len(r.matched_skills)}):",
        "   " + (", ".join(r.matched_skills) or "none"),
        "",
        f" Missing skills ({len(r.missing_skills)}):",
        "   " + (", ".join(r.missing_skills) or "none - you cover everything listed!"),
        "",
        f" Extra skills on your resume ({len(r.extra_skills)}):",
        "   " + (", ".join(r.extra_skills) or "none"),
        "=" * 56,
    ]
    return "\n".join(lines)


def to_json(r: AnalysisResult) -> str:
    return json.dumps(r.to_dict(), indent=2)
