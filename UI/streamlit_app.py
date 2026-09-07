import requests
import streamlit as st


API_URL = "http://ai-knowledge-api-service:8000/ask"


st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="centered"
)


st.title("AI Knowledge Assistant")

st.caption(
    "Ask questions about the ThinkPad P1 Gen 7 documentation."
)


question = st.text_input(
    "Ask a question",
    placeholder="Example: Can I replace the built-in battery myself?"
)


if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        try:
            with st.spinner("Searching knowledge base..."):

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=60
                )

                response.raise_for_status()

                result = response.json()

            st.subheader("Answer")

            st.write(
                result["answer"]
            )

            st.divider()

            st.write(
                f"**Answer type:** {result['answer_type']}"
            )

            st.write(
                f"**Grounded:** {result['grounded']}"
            )

            st.write(
                f"**Tool used:** {result['tool_used']}"
            )

            st.write(
                f"**Cached:** {result['cached']}"
            )

            st.write(
                f"**Latency:** {result['latency_ms']} ms"
            )

            if result["sources"]:

                st.subheader("Sources")

                for source in result["sources"]:

                    st.write(
                        f"- {source['document']} "
                        f"(page {source['page']})"
                    )

        except requests.RequestException as exc:

            st.error(
                f"Could not connect to the API: {exc}"
            )