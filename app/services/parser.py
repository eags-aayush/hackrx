import pdfplumber
import docx
import os

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
            text += page.extract_text() + "\n"
    return text

def extract_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])