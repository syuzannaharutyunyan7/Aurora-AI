import chromadb
from sentence_transformers import SentenceTransformer
import uuid

embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="memory/chroma")
col = client.get_or_create_collection("memory")

# ----------------------------
# ADD MEMORY
# ----------------------------
def add(text):
    if not text or len(text.strip()) < 5:
        return

    emb = embedder.encode([text])[0]

    col.add(
        ids=[str(uuid.uuid4())],
        embeddings=[emb.tolist()],
        documents=[text]
    )

# ----------------------------
# SEARCH MEMORY (FIXED)
# ----------------------------
def search(query, k=5):
    q = embedder.encode([query])[0]

    res = col.query(
        query_embeddings=[q.tolist()],
        n_results=k
    )

    if not res or "documents" not in res or not res["documents"]:
        return []

    return res["documents"][0]