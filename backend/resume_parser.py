from io import BytesIO
from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file):
    pdf = PdfReader(BytesIO(file.read()))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text

def extract_docx_text(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])
