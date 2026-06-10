from langchain_text_splitters import RecursiveCharacterTextSplitter
from code_reader import load_code_files

def create_chunks(repo_path):

    docs = load_code_files(repo_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for doc in docs:

        split_docs = splitter.create_documents(
            [doc["content"]],                  # Even if you're processing one file, LangChain wants a list.
            metadatas=[{"source": doc["path"]}]     # Metadata is attached to every chunk.
        )

        chunks.extend(split_docs)

    return chunks