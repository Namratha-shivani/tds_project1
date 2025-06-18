import hashlib
import httpx
import json
import numpy as np
import os
import time
from pathlib import Path
from semantic_text_splitter import MarkdownSplitter
from tqdm import tqdm
from google import genai

def get_embedding(text: str) -> list:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text
    )
    return response.embeddings

def get_chunks(file_path: str, chunk_size: int = 20000):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        splitter = MarkdownSplitter(chunk_size)
        chunks = splitter.chunks(content)
        return chunks

if __name__ == "__main__":
    files = [*Path("data/tds_content").glob("*.md"), *Path("data/tds_content").rglob("*.md")]
    all_chunks = []
    all_embeddings = []
    total_chunks = 0
    file_chunks = {}

    for file_path in files:
        chunks = get_chunks(file_path)
        file_chunks[file_path] = chunks
        total_chunks += len(chunks)

    request_count = 0

    with tqdm(total=total_chunks, desc="Processing embeddings") as pbar:
        for file_path, chunks in file_chunks.items():
            for chunk in chunks:
                try:
                    embedding = get_embedding(chunk)
                    all_chunks.append(chunk)
                    all_embeddings.append(embedding)
                    request_count += 1

                    # Wait after every 5 requests
                    if request_count % 5 == 0:
                        time.sleep(30)

                    pbar.set_postfix({"file": file_path.name, "chunks": len(all_chunks)})
                    pbar.update(1)

                except Exception as e:
                    print(f"Skipping chunk from {file_path.name} due to error: {e}")
                    pbar.update(1)
                    continue

    np.savez("embeddings.npz", chunks=np.array(all_chunks, dtype=object), embeddings=np.array(all_embeddings, dtype=object))
