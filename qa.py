import os
from dotenv import load_dotenv
import google.generativeai as genai
from retriever import retrieve

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def answer_question(question):

    docs = retrieve(question,k=5)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a software engineering assistant.

Answer ONLY using the provided code context.

If the answer cannot be found,
say:
"I could not find that information in the repository."

Context:
{context}

Question:
{question}
"""

    response = model.generate_content(prompt)
    return response.text, docs