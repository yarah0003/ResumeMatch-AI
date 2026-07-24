import numpy as np
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from .rag_setup import _embeddings

PROMPT = """You are an expert resume coach.
Rewrite the candidate's weak bullet to highlight the missing skill.

Missing skill: {skill}
Candidate's closest bullet: "{weak_bullet}"

Strong resume bullet examples for reference:
{examples}

Rules:
- Do NOT fabricate numbers or experience that isn't implied
- Incorporate the missing skill naturally
- Use strong action verbs and be specific
- Output ONLY the rewritten bullet, nothing else

Rewritten bullet:"""

def find_closest_bullet(skill, bullets):
    if not bullets:
        return ""
    emb      = _embeddings()
    skill_v  = emb.embed_query(skill)
    bul_vecs = emb.embed_documents(bullets)
    scores   = [_cosine(skill_v, b) for b in bul_vecs]
    return bullets[int(np.argmax(scores))]

def _cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def rewrite_bullet(skill, weak_bullet, bullets_store):
    docs     = bullets_store.similarity_search(skill, k=3)
    examples = "\n".join([f"• {d.page_content}" for d in docs])
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
    chain    = ChatPromptTemplate.from_template(PROMPT) | llm
    result   = chain.invoke({"skill": skill, "weak_bullet": weak_bullet, "examples": examples})
    return result.content.strip()