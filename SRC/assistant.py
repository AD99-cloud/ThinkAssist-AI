from SRC.retriever import retrieve
from SRC.llm import generate_answer
from SRC.tool_router import run_tool_question
from SRC.cache import get_cached, set_cached


def handle_conversation(question: str):
    q = question.strip().lower()

    greetings = {
        "hi",
        "hello",
        "hey",
        "hi there",
        "hello there",
        "hey there",
        "good morning",
        "good afternoon",
        "good evening",
    }

    thanks = {
        "thanks",
        "thank you",
        "thanks!",
        "thank you!",
        "thx",
    }

    capability_questions = {
        "what can you do",
        "what can you help me with",
        "how can you help me",
        "who are you",
    }

    if q in greetings:
        return (
            "Hi! I'm ThinkAssist. How can I help with your "
            "ThinkPad P1 Gen 7 today?"
        )

    if q in thanks:
        return (
            "You're welcome! Let me know if you have another "
            "question about your ThinkPad."
        )

    if q.rstrip("?") in capability_questions:
        return (
            "I can help with ThinkPad P1 Gen 7 setup, hardware, "
            "battery and power, troubleshooting, Windows recovery, "
            "warranty information, ports, and other supported documentation."
        )

    return None

def ask(question: str, top_k: int = 3):
    conversation_response = handle_conversation(question)

    if conversation_response:
        return {
            "question": question,
            "answer": conversation_response,
            "grounded": False,
            "answer_type": "conversation",
            "sources": [],
            "tool_used": None,
            "cached": False,
        }
    # Step 0: check cache first
    cache_key = question.strip().lower()

    cached_result = get_cached(cache_key)

    if cached_result is not None:
        cached_result["cached"] = True
        return cached_result

    # Step 1: check whether a tool should handle the question
    tool_result = run_tool_question(question)

    if tool_result["tool_used"] is not None:

        result = {
            "question": question,
            "answer": tool_result["answer"],
            "grounded": True,
            "answer_type": "tool",
            "sources": [],
            "tool_used": tool_result["tool_used"],
            "cached": False
        }

        set_cached(cache_key, result)

        return result

    # Step 2: otherwise search the document knowledge base
    retrieved_chunks = retrieve(
        query=question,
        top_k=top_k
    )

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):

        context_parts.append(
            f"""
SOURCE {i}
Document: {chunk['document']}
Page: {chunk['page']}

{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    # Step 3: generate grounded answer from retrieved documentation
    response = generate_answer(
        question=question,
        context=context
    )

    # Step 4: classify the type of answer
    if response.grounded:
        answer_type = "document"
    else:
        answer_type = "unsupported"

    result = {
        "question": question,
        "answer": response.answer,
        "grounded": response.grounded,
        "answer_type": answer_type,
        "sources": [
            source.model_dump()
            for source in response.sources
        ],
        "tool_used": None,
        "cached": False
    }

    set_cached(cache_key, result)

    return result