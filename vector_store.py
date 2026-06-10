from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os


model = SentenceTransformer("all-MiniLM-L6-v2")  # model to generate embedding vectors

def create_vector_store(chunks):
    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    os.makedirs("vectorstore",exist_ok=True)
    faiss.write_index(index,"vectorstore/code.index")  # code.index - binary file containing FAISS's serialized index data

    with open("vectorstore/chunks.pkl","wb") as f:
        pickle.dump(chunks,f)      # ref notes

    print(f"Stored {len(chunks)} chunks")