import streamlit as st
from qa import answer_question

st.title("Codebase RAG Assistant")

question = st.text_input("Ask a question about the repository")

if st.button("Ask"):

    answer, docs = answer_question(question)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")

    for doc in docs:

        st.code(
            doc.page_content[:500]
        )

        st.caption(
            doc.metadata["source"]
        )