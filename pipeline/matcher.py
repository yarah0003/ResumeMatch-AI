import numpy as np
from .rag_setup import _embeddings

def _cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def match_skills(candidate_skills, required_skills, threshold=0.72):
    """Returns (matched_list, missing_list)."""
    if not candidate_skills or not required_skills:
        return [], required_skills
    emb       = _embeddings()
    cand_embs = emb.embed_documents(candidate_skills)
    matched, missing = [], []
    for req in required_skills:
        req_emb = emb.embed_query(req)
        best    = max(_cosine(req_emb, c) for c in cand_embs)
        (matched if best >= threshold else missing).append(req)
    return matched, missing

def ats_score(candidate_skills, required_skills):
    """Exact keyword overlap score (0-100)."""
    c = {s.lower() for s in candidate_skills}
    r = {s.lower() for s in required_skills}
    return round(len(c & r) / len(r) * 100, 1) if r else 0.0