import os
import json

from dotenv import load_dotenv
from groq import Groq

from SRC.schemas import AssistantResponse

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found.")

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-20b"


def generate_answer(question: str, context: str) -> AssistantResponse:

    system_prompt = """
You are an AI technical support assistant for Lenovo ThinkPad documentation.

You must follow these rules:

1. Answer ONLY using the supplied document context.
2. Do not use outside knowledge.
3. If the context does not contain enough information, say:
   "I don't have enough information in the provided documentation."
4. Never invent specifications, procedures, warnings, or policies.
5. Only cite documents and pages explicitly present in the supplied context.
6. grounded must be true only when the answer is supported by the supplied context.
7. If there is insufficient information, grounded must be false and sources should be empty.

Return ONLY valid JSON in exactly this structure:

{
  "answer": "your answer",
  "grounded": true,
  "sources": [
    {
      "document": "filename.pdf",
      "page": 1
    }
  ]
}
"""

    user_prompt = f"""
DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.1
    )

    raw_output = response.choices[0].message.content

    parsed_output = json.loads(raw_output)

    return AssistantResponse(**parsed_output)