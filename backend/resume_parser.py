import fitz

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ''
    for page in doc:
        text += page.get_text()
    return text

from docx import Document
import io

def extract_docx_text(uploaded_file):
    doc = Document(io.BytesIO(uploaded_file.read()))
    return "\n".join([para.text for para in doc.paragraphs])
