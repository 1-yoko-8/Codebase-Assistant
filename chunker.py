from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from code_reader import load_code_files
import os

LANG_MAP = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".ts": Language.TS,
    ".java": Language.JAVA,
    ".cpp": Language.CPP,
    ".c": Language.CPP,
    ".h": Language.CPP,
}

def get_splitter(file_ext: str):
    lang = LANG_MAP.get(file_ext)

    if lang:
        return RecursiveCharacterTextSplitter.from_language(
            language=lang,
            chunk_size=1000,
            chunk_overlap=100,
        )

    return RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
    )


def create_chunks(repo_path):
    docs = load_code_files(repo_path)

    chunks = []
    global_id = 0

    for doc in docs:
        file_path = doc["path"]
        _, file_ext = os.path.splitext(file_path)

        splitter = get_splitter(file_ext)

        split_docs = splitter.create_documents(
            [doc["content"]],
            metadatas=[{"source": file_path}]
        )

        for i, chunk in enumerate(split_docs):
            chunk.metadata.update({
                "chunk_id": global_id,
                "file_chunk_id": i,   # order inside file
                "source": file_path
            })

            chunks.append(chunk)
            global_id += 1

    return chunks