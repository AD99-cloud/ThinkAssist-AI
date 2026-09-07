# ThinkAssist AI

ThinkAssist is an AI-powered technical support assistant for the Lenovo ThinkPad P1 Gen 7.

It uses retrieval-augmented generation, semantic search, reranking, tool calling, and a FastAPI backend to answer questions from connected Lenovo documentation through a modern Next.js chat interface.

## Architecture

```text
User
  |
  v
Next.js Frontend
  |
  v
FastAPI API
  |
  +-------------------+
  |                   |
  v                   v
Tool Router        RAG Pipeline
                       |
                       v
               Sentence Embeddings
                       |
                       v
                    ChromaDB
                       |
                       v
              Candidate Retrieval
                       |
                       v
              Cross-Encoder Reranker
                       |
                       v
                    Groq LLM
                       |
                       v
              Answer + Sources
```

## Key Features

* Document-grounded question answering
* Semantic search with ChromaDB
* Cross-encoder reranking
* Tool calling for calculations and device information
* Source references
* Guardrails for unsupported questions
* FastAPI backend
* Next.js / TypeScript frontend
* Docker and Kubernetes configuration
* Cloud deployment with Render and Vercel

## Tech Stack

**AI:** Groq, Sentence Transformers, ChromaDB, RAG, Cross-Encoder Reranking
**Backend:** Python, FastAPI, Pydantic
**Frontend:** Next.js, React, TypeScript, Tailwind CSS
**Infrastructure:** Docker, Kubernetes, Render, Vercel



## Live App

Frontend: `think-assist-ai.vercel.app`

Backend: `https://thinkassist-ai-backend.onrender.com`

