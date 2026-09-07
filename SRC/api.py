import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from SRC.assistant import ask


app = FastAPI(
    title="AI Knowledge Assistant",
    description="Document-grounded ThinkPad support assistant with tool calling.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        description="Question to ask the AI knowledge assistant.",
    )


class SourceResponse(BaseModel):
    document: str
    page: int


class AskResponse(BaseModel):
    question: str
    answer: str
    grounded: bool
    answer_type: str
    sources: list[SourceResponse]
    tool_used: str | list[str] | None = None
    cached: bool
    latency_ms: float


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    start_time = time.perf_counter()

    try:
        result = ask(request.question)

        latency_ms = (time.perf_counter() - start_time) * 1000
        result["latency_ms"] = round(latency_ms, 2)

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The assistant failed to process the request.",
        ) from exc