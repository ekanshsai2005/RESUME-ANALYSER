"""Extract plain text from resume files (PDF, DOCX, TXT)."""
from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO, Union

SUPPORTED = {".pdf", ".docx", ".txt", ".md"}


def _read_pdf(stream: BinaryIO) -> str:
    from pypdf import PdfReader

    reader = PdfReader(stream)
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def _read_docx(stream: BinaryIO) -> str:
    from docx import Document

    doc = Document(stream)
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.extend(cell.text for cell in row.cells)
    return "\n".join(parts)


def extract_text(source: Union[str, Path, bytes, BinaryIO], filename: str | None = None) -> str:
    """Return text from a file path, raw bytes, or file-like object.

    `filename` is required (for its extension) when `source` is bytes or a stream
    without a `.name` attribute, e.g. a Streamlit upload.
    """
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        suffix = path.suffix.lower()
        data = path.read_bytes()
    else:
        name = filename or getattr(source, "name", "")
        suffix = Path(name).suffix.lower()
        data = source if isinstance(source, bytes) else source.read()

    if suffix not in SUPPORTED:
        raise ValueError(f"Unsupported file type '{suffix}'. Use one of: {', '.join(sorted(SUPPORTED))}")

    if suffix == ".pdf":
        text = _read_pdf(io.BytesIO(data))
    elif suffix == ".docx":
        text = _read_docx(io.BytesIO(data))
    else:
        text = data.decode("utf-8", errors="ignore")

    text = text.strip()
    if not text:
        raise ValueError("No text could be extracted (scanned/image-only PDFs need OCR).")
    return text
