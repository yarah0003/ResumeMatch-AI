import pdfplumber
import re

def parse_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text(x_tolerance=3, y_tolerance=3)
            if extracted:
                text += extracted + "\n"
    return clean_text(text)

def clean_text(text):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()