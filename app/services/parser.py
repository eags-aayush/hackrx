import pdfplumber
import docx
import os
import requests
import tempfile

def parse_document(doc_url: str) -> str:
    # Download the document
    response = requests.get(doc_url)
    response.raise_for_status()

    # Create a temporary file
    _, temp_path = tempfile.mkstemp()
    with open(temp_path, "wb") as f:
        f.write(response.content)

    try:
        text = extract_text(temp_path)
    finally:
        os.remove(temp_path)

    return text

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_from_docx(file_path)
    elif file_path.endswith(".txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def extract_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])
