from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import pandas as pd
import json
from pathlib import Path

EMBED_MODEL   = "text-embedding-3-small"
TAXONOMY_DIR  = "vector_store/taxonomy"
BULLETS_DIR   = "vector_store/bullets"

def _embeddings():
    # Completely free, downloads a tiny model locally once
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_taxonomy_store(csv_path="data/skills.csv"):
    emb = _embeddings()
    if Path(TAXONOMY_DIR).exists():
        return Chroma(persist_directory=TAXONOMY_DIR, embedding_function=emb)
    df     = pd.read_csv(csv_path)
    skills = df['Element Name'].dropna().unique().tolist()
    docs   = [Document(page_content=s) for s in skills]
    return Chroma.from_documents(docs, emb, persist_directory=TAXONOMY_DIR)

def build_bullets_store(json_path="data/bullet_examples.json"):
    emb = _embeddings()
    if Path(BULLETS_DIR).exists():
        return Chroma(persist_directory=BULLETS_DIR, embedding_function=emb)
    examples = json.loads(Path(json_path).read_text(encoding="utf-8"))
    docs = [
        Document(page_content=b["bullet"],
                 metadata={"skill": b["skill"], "domain": b["domain"]})
        for b in examples
    ]
    return Chroma.from_documents(docs, emb, persist_directory=BULLETS_DIR)