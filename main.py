"""Command-line interface.

Usage:
    python main.py --resume samples/resume.txt --jd samples/job_description.txt
    python main.py -r resume.pdf -j jd.txt --json
"""
from __future__ import annotations

import argparse
import sys

from analyzer import analyze, extract_text
from analyzer.report import to_json, to_text


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Automated Resume Analyzer")
    p.add_argument("-r", "--resume", required=True, help="Resume file (.pdf, .docx, .txt)")
    p.add_argument("-j", "--jd", required=True, help="Job description file (.pdf, .docx, .txt)")
    p.add_argument("--json", action="store_true", help="Output JSON instead of a text report")
    args = p.parse_args(argv)

    try:
        resume = extract_text(args.resume)
        jd = extract_text(args.jd)
        result = analyze(resume, jd)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(to_json(result) if args.json else to_text(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
