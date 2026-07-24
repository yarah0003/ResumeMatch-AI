from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from .output_schema import ExtractionResult

PROMPT = """You are an expert resume analyst.
Extract from the {doc_type} below:
1. ALL skills (technical, soft skills, tools, certifications, frameworks)
2. If it is a Resume: also extract each experience bullet point verbatim

{doc_type}:
{text}"""


def extract_skills(text, doc_type="Resume"):
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)

    # Enforce structured output directly on the model
    structured_llm = llm.with_structured_output(ExtractionResult)

    prompt = ChatPromptTemplate.from_template(PROMPT)

    # Chain the prompt straight to the structured LLM
    chain = prompt | structured_llm

    return chain.invoke({"text": text, "doc_type": doc_type})