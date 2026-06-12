import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_vector_store():
    index = faiss.read_index("vectorstore/code.index")
    with open("vectorstore/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def expand_neighbors(chunks, idx, window=1):
    """
    Expands context safely within same file grouping.
    """
    base = chunks[idx]
    results = [base]

    source = base.metadata.get("source")

    # expand forward
    i = idx + 1
    while i < len(chunks) and chunks[i].metadata.get("source") == source and len(results) < 2 * window + 1:
        results.append(chunks[i])
        i += 1

    # expand backward
    i = idx - 1
    while i >= 0 and chunks[i].metadata.get("source") == source and len(results) < 2 * window + 1:
        results.insert(0, chunks[i])
        i -= 1

    return results


def retrieve(query, k=3, expand_window=1):
    index, chunks = load_vector_store()

    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)

    results = []
    seen = set()

    for idx in indices[0]:
        if idx in seen:
            continue

        seen.add(idx)

        # expand context properly
        expanded = expand_neighbors(chunks, idx, window=expand_window)

        for c in expanded:
            cid = c.metadata.get("chunk_id")
            if cid not in seen:
                results.append(c)
                seen.add(cid)

    return results