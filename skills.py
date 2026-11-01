"""Skill taxonomy and extraction.

Each canonical skill maps to a list of aliases. Matching is case-insensitive and
respects word boundaries, with special handling for tokens like C++, C#, .NET.
"""
from __future__ import annotations

import re
from functools import lru_cache

SKILLS: dict[str, list[str]] = {
    # Languages
    "Python": ["python", "python3"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js", "ecmascript", "es6"],
    "TypeScript": ["typescript", "ts"],
    "C": ["c language", "c programming"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "csharp"],
    "Go": ["golang", "go lang"],
    "Rust": ["rust"],
    "Kotlin": ["kotlin"],
    "Swift": ["swift"],
    "PHP": ["php"],
    "Ruby": ["ruby"],
    "R": ["r programming", "r language"],
    "SQL": ["sql", "t-sql", "pl/sql"],
    "Bash": ["bash", "shell scripting", "shell script"],
    # Web
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "sass", "scss"],
    "React": ["react", "react.js", "reactjs"],
    "Angular": ["angular", "angularjs"],
    "Vue.js": ["vue", "vue.js", "vuejs"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "Express": ["express.js", "expressjs", "express"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Spring Boot": ["spring boot", "springboot", "spring framework", "spring"],
    ".NET": [".net", "dotnet", "asp.net"],
    "REST APIs": ["rest api", "rest apis", "restful", "rest"],
    "GraphQL": ["graphql"],
    # Data / ML
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision", "opencv"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis", "data analytics", "exploratory data analysis", "eda"],
    "Data Visualization": ["data visualization", "matplotlib", "seaborn", "plotly", "tableau", "power bi"],
    "Statistics": ["statistics", "statistical analysis"],
    "LLMs": ["llm", "llms", "large language model", "large language models", "generative ai", "genai"],
    "Spark": ["spark", "pyspark"],
    "Hadoop": ["hadoop"],
    "ETL": ["etl", "data pipeline", "data pipelines"],
    # Databases
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "SQLite": ["sqlite"],
    "NoSQL": ["nosql"],
    "Oracle": ["oracle db", "oracle database"],
    # Cloud / DevOps
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "CI/CD": ["ci/cd", "cicd", "continuous integration", "continuous delivery", "jenkins", "github actions", "gitlab ci"],
    "Terraform": ["terraform"],
    "Linux": ["linux", "unix"],
    "Git": ["git", "github", "gitlab", "version control"],
    # CS fundamentals
    "Data Structures": ["data structures", "dsa"],
    "Algorithms": ["algorithms", "algorithm design"],
    "OOP": ["oop", "object oriented", "object-oriented"],
    "System Design": ["system design", "distributed systems", "microservices"],
    "Operating Systems": ["operating systems"],
    "Computer Networks": ["computer networks", "networking", "tcp/ip"],
    "DBMS": ["dbms", "database management"],
    # Practices / soft skills
    "Agile": ["agile", "scrum", "kanban"],
    "Testing": ["unit testing", "pytest", "junit", "test automation", "selenium", "tdd"],
    "Communication": ["communication skills", "communication", "presentation skills"],
    "Teamwork": ["teamwork", "collaboration", "team player", "collaborative"],
    "Problem Solving": ["problem solving", "problem-solving", "analytical skills", "analytical thinking"],
    "Leadership": ["leadership", "team lead", "mentoring"],
    # Mobile
    "Android": ["android"],
    "iOS": ["ios"],
    "Flutter": ["flutter"],
    "React Native": ["react native"],
    # Security
    "Cybersecurity": ["cybersecurity", "cyber security", "information security", "infosec"],
}


def _alias_pattern(alias: str) -> re.Pattern:
    escaped = re.escape(alias.lower())
    # Custom boundaries: no alphanumeric / + / # directly adjacent (handles c++, c#, .net)
    return re.compile(rf"(?<![a-z0-9+#]){escaped}(?![a-z0-9+#])", re.IGNORECASE)


@lru_cache(maxsize=1)
def _compiled() -> dict[str, list[re.Pattern]]:
    return {skill: [_alias_pattern(a) for a in aliases] for skill, aliases in SKILLS.items()}


def extract_skills(text: str) -> set[str]:
    """Return the set of canonical skills mentioned in `text`."""
    # Normalise whitespace so multi-word aliases match across line breaks
    normalised = re.sub(r"\s+", " ", text.lower())
    found: set[str] = set()
    for skill, patterns in _compiled().items():
        if any(p.search(normalised) for p in patterns):
            found.add(skill)
    return found
