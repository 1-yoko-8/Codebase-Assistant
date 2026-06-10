from chunker import create_chunks
from vector_store import create_vector_store

chunks = create_chunks("repos/project")
create_vector_store(chunks)