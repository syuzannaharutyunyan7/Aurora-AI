from pypdf import PdfReader
import docx
from rag.db import add

# ----------------------------
# READERS
# ----------------------------
def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def read_docx(path):
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text)

# ----------------------------
# CLEAN
# ----------------------------
def clean(text):
    return text.replace("\x00", " ").strip()

# ----------------------------
# CHUNKING
# ----------------------------
def chunk_text(text, size=500):
    text = clean(text)
    return [text[i:i+size] for i in range(0, len(text), size)]

# ----------------------------
# INGEST FILE
# ----------------------------
def ingest_file(path):

    if path.endswith(".pdf"):
        text = read_pdf(path)

    elif path.endswith(".docx"):
        text = read_docx(path)

    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    chunks = chunk_text(text)

    for chunk in chunks:
        if len(chunk.strip()) > 20:
            add(chunk.strip())

    return chunks