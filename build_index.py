import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
EMBED_MODEL = "gemini-embedding-001"   # check AI Studio for the current embedding model name


def split_into_chunks(text, chunk_size=800, overlap=100):
    """Cut text into pieces of ~800 characters, each overlapping the previous by 100."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


# 1. Read every .md file in the docs folder and split it into chunks
chunks = []
for file in Path("docs").glob("*.md"):
    text = file.read_text(encoding="utf-8")
    for piece in split_into_chunks(text):
        chunks.append({"source": file.name, "text": piece})

print(f"Created {len(chunks)} chunks")

# 2. Turn each chunk into an embedding
for i, chunk in enumerate(chunks, start=1):
    result = client.models.embed_content(model=EMBED_MODEL, contents=chunk["text"])
    chunk["embedding"] = result.embeddings[0].values
    print(f"Embedded chunk {i}/{len(chunks)}")

# 3. Save everything to a file
Path("index.json").write_text(json.dumps(chunks), encoding="utf-8")
print("Saved index.json ✅")