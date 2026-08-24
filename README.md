# Codebase RAG Assistant

A local Retrieval-Augmented Generation (RAG) tool that lets you ask natural-language questions about any GitHub repository. It clones a target repo, indexes its source files into a vector store, and answers questions by retrieving relevant code snippets and passing them to Google's Gemini model, with a simple Streamlit chat-style interface.

## Key Features

- Clone any public GitHub repository by URL
- Parse and filter source files (`.py`, `.js`, `.ts`, `.java`, `.cpp`, `.c`, `.h`, `.md`, `.txt`, `.yaml`, `.yml`, `.json`)
- Language-aware code chunking (Python, JS, TS, Java, C/C++) with a generic fallback splitter
- Semantic search over code using sentence embeddings and a FAISS vector index
- Neighboring-chunk expansion for richer context around each retrieved match
- Question answering grounded strictly in retrieved code context, via the Gemini API
- Streamlit UI showing the generated answer alongside its source code snippets and file paths

## Tech Stack

- **Language:** Python
- **UI:** Streamlit
- **Chunking:** LangChain (`langchain_text_splitters`)
- **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`)
- **Vector search:** FAISS (`IndexFlatL2`)
- **LLM:** Google Generative AI (`gemini-3.1-flash-lite`)
- **Repo cloning:** GitPython
- **Config:** python-dotenv

## High-Level Architecture

**Offline indexing pipeline:**
`ingest.py` clones a repo → `chunker.py` (using `code_reader.py`) splits files into chunks → `vector_store.py` embeds the chunks and writes a FAISS index + pickled chunk metadata to disk.

**Query-time app:**
`app.py` (Streamlit) takes a question → `qa.py` calls `retriever.py` to load the FAISS index, embed the query, and retrieve + expand relevant chunks → `qa.py` builds a context-grounded prompt and calls the Gemini API → the answer and source snippets are displayed in the UI.

These two flows are independent — the index must be built before the app can answer questions.

## Project Structure
Codebase-Assistant/
├── app.py # Streamlit UI entry point
├── ingest.py # Clones a GitHub repo into repos/project
├── build_index.py # Runs chunking + vector store creation
├── chunker.py # Splits source files into chunks
├── code_reader.py # Loads supported source files from a repo
├── vector_store.py # Creates/persists the FAISS index and chunk metadata
├── retriever.py # Loads the index and retrieves relevant chunks
├── qa.py # Builds the prompt and calls the Gemini API
├── requirements.txt
└── .env.example

## Prerequisites

- Git installed and available on your PATH
- A Google Gemini API key

## Installation / Setup

```bash
git clone <this-repository-url>
cd Codebase-Assistant
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variable Setup

Copy the example file and add your Gemini API key:

```bash
cp .env.example .env
```

Then edit `.env` and set:
GEMINI_API_KEY=your_actual_key_here


## Running the Project

Run these in order — each step depends on the previous one:

```bash
# 1. Clone the target repository (prompts for a GitHub URL)
python ingest.py

# 2. Build the vector index from the cloned repository
python build_index.py

# 3. Launch the Q&A interface
streamlit run app.py
```

## How to Use It

1. After running the three commands above, open the Streamlit app in your browser (URL shown in the terminal).
2. Type a question about the indexed repository (e.g. "What does the `retrieve` function do?").
3. Click **Ask**.
4. The app displays the generated answer, followed by the source code snippets and file paths it was based on.

## Screenshots

<!-- Add screenshots below -->

**Main Q&A interface**
`[screenshot placeholder]`

**Example question and answer with sources**
`[screenshot placeholder]`

## Limitations / Current Considerations

- Only one repository can be indexed at a time; re-running `ingest.py` overwrites the previously cloned repo (`repos/project`).
- The index (`vectorstore/`) is not rebuilt automatically — changes to the source repo require manually re-running `ingest.py` and `build_index.py`.
- Running `streamlit run app.py` before the index exists will fail, since the app expects `vectorstore/code.index` and `vectorstore/chunks.pkl` to already be present.
- No persistent database — all state is local files on disk (repo clone, FAISS index, pickled chunks).
