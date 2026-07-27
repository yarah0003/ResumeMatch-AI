from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from .output_schema import ExtractionResult

PROMPT = """You are an expert resume analyst.
Extract from the {doc_type} below and return ONLY a JSON object with exactly this structure:
{{
  "skills": ["skill1", "skill2", "skill3"],
  "experience_bullets": ["bullet1", "bullet2"]
}}

Rules:
- "skills": a FLAT list of ALL skills as plain strings (technical, soft skills, tools, certifications, frameworks — all combined into one list)
- "experience_bullets": if doc_type is Resume, list each experience bullet verbatim; if Job Description, return empty list []

{doc_type}:
{text}"""


def extract_skills(text, doc_type="Resume"):
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)

    structured_llm = llm.with_structured_output(ExtractionResult, method="json_mode")

    prompt = ChatPromptTemplate.from_template(PROMPT)

    chain = prompt | structured_llm

    return chain.invoke({"text": text, "doc_type": doc_type})