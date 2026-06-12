import os
from dotenv import load_dotenv
import google.generativeai as genai
from retriever import retrieve

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-3.1-flash-lite")

def answer_question(question):

    docs = retrieve(question,k=3)

    context = "\n\n".join(
        f"FILE: {doc.metadata['source']}\n{doc.page_content}"
        for doc in docs
    )

    prompt = f"""
    You are a senior software engineering assistant.

    INSTRUCTIONS:
    - Answer ONLY using the provided code context.
    - If the answer is not in the context, say:
      "I could not find that information in the repository."
    - Explain step-by-step in a clear and simple way.
    - Refer to file names or functions when relevant.
    - The answer should include the related code snippet as well.

    CONTEXT:
    {context}

    QUESTION:
    {question}
    """

    response = model.generate_content(prompt)
    return response.text, docs