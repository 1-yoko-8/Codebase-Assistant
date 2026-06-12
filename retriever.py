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
    Returns current chunk + neighboring chunks
    from the same file.
    """

    source = chunks[idx].metadata["source"]

    start = idx
    end = idx

    # previous chunks
    for _ in range(window):
        if (
            start > 0
            and chunks[start - 1].metadata["source"] == source
        ):
            start -= 1

    # next chunks
    for _ in range(window):
        if (
            end < len(chunks) - 1
            and chunks[end + 1].metadata["source"] == source
        ):
            end += 1

    return chunks[start:end + 1]


def retrieve(query, k=3, expand_window=1):
    index, chunks = load_vector_store()

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    distances, indices = index.search(query_embedding, k)

    results = []
    seen_chunk_ids = set()

    for idx in indices[0]:

        if idx == -1:
            continue

        expanded_chunks = expand_neighbors(
            chunks,
            idx,
            window=expand_window
        )

        for chunk in expanded_chunks:

            chunk_id = chunk.metadata["chunk_id"]

            if chunk_id in seen_chunk_ids:
                continue

            seen_chunk_ids.add(chunk_id)
            results.append(chunk)

    return results