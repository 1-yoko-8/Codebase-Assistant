import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_vector_store():
    index = faiss.read_index("vectorstore/code.index")
    with open("vectorstore/chunks.pkl","rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def retrieve(query, k=3):
    index, chunks = load_vector_store()

    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding,k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results