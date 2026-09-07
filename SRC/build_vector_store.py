from pathlib import Path
import json
import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "DATA" / "Processed"
CHROMA_DIR = PROJECT_ROOT / "DATA" / "CHROMA_DB"

INPUT_FILE = PROCESSED_DIR / "chunks.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

print("Loading chunks...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Create persistent local Chroma database
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

# Re-create collection while we're developing
try:
    client.delete_collection("thinkpad_knowledge")
except Exception:
    pass

collection = client.create_collection(
    name="thinkpad_knowledge"
)

texts = [chunk["text"] for chunk in chunks]

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

ids = []
documents = []
metadatas = []

for chunk in chunks:
    ids.append(chunk["chunk_id"])
    documents.append(chunk["text"])

    metadatas.append({
        "document": chunk["document"],
        "page": chunk["page"],
        "chunk_number": chunk["chunk_number"]
    })

print("Saving embeddings to ChromaDB...")

collection.add(
    ids=ids,
    embeddings=embeddings.tolist(),
    documents=documents,
    metadatas=metadatas
)

print()
print("Vector store created successfully")
print(f"Chunks stored: {collection.count()}")
print(f"Database location: {CHROMA_DIR}")