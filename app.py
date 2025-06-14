# app.py for creating an answering app
import os
import io
import base64
import pytesseract
from PIL import Image
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from bs4 import BeautifulSoup
import openai
import numpy as np
import faiss

# Load environment
load_dotenv()
openai.api_base = "https://aipipe.org/v1" 
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend calls (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folders containing local HTML files (wget output)
HTML_FOLDERS = ["./discourse.onlinedegree.iitm.ac.in", "./tds.s-anand.net"]

docs = []
doc_sources = []

EMBED_MODEL = "text-embedding-ada-002"
DIMENSION = 1536

def load_html_chunks():
    for folder in HTML_FOLDERS:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".html"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        soup = BeautifulSoup(f, "html.parser")

                        # Extract known semantic content blocks
                        # This will catch Discourse and blog-like formats
                        content_blocks = soup.find_all(['article', 'section', 'div'], recursive=True)

                        for block in content_blocks:
                            # Optional: Filter based on class for known structures like Discourse
                            if block.has_attr("class"):
                                class_str = " ".join(block.get("class"))
                                if "cooked" not in class_str and "post" not in class_str:
                                    continue  # skip unrelated divs

                            text = block.get_text(separator=" ", strip=True)
                            if text and len(text) > 50:  # Avoid junk
                                docs.append(text)
                                doc_sources.append(filepath)

def embed_chunks(texts: List[str]):
    texts = [t[:8191] for t in texts]
    response = openai.Embedding.create(input=texts, model=EMBED_MODEL)
    return [d['embedding'] for d in response['data']]

# Load and embed all chunks
print("Indexing HTML content...")
load_html_chunks()
doc_embeddings = embed_chunks(docs)
index = faiss.IndexFlatL2(DIMENSION)
index.add(np.array(doc_embeddings).astype('float32'))

@app.post("/answer/")
async def answer_question(
    text: str = Form(...),
    link: Optional[str] = Form(None),
    image: Optional[UploadFile] = None
):
    # OCR from image if provided
    image_text = ""
    if image:
        try:
            content = await image.read()
            image_obj = Image.open(io.BytesIO(content))
            image_text = pytesseract.image_to_string(image_obj)
        except Exception as e:
            return JSONResponse({"error": f"Image processing failed: {str(e)}"}, status_code=400)

    full_query = f"{text}\n{image_text}".strip()

    # Embed user query
    query_embedding = openai.Embedding.create(
        input=full_query[:8191],
        model=EMBED_MODEL
    )["data"][0]["embedding"]

    # Filter based on link (if provided)
    mask = [True] * len(docs)
    if link:
        keyword = link.split("/")[-1].replace(".html", "")
        mask = [keyword in os.path.basename(src) for src in doc_sources]

    filtered_docs = [d for d, m in zip(docs, mask) if m]
    filtered_sources = [s for s, m in zip(doc_sources, mask) if m]
    filtered_embeddings = [e for e, m in zip(doc_embeddings, mask) if m]

    if not filtered_docs:
        return JSONResponse({"error": "No matching content found for the given link."}, status_code=404)

    # Create temporary FAISS index
    temp_index = faiss.IndexFlatL2(DIMENSION)
    temp_index.add(np.array(filtered_embeddings).astype('float32'))
    D, I = temp_index.search(np.array([query_embedding]).astype('float32'), 5)

    top_chunks = [{"text": filtered_docs[i], "url": filtered_sources[i]} for i in I[0]]

    # Prepare RAG-style prompt
    context_block = "\n\n".join([c["text"] for c in top_chunks])
    prompt = f"""You are a helpful assistant. Use the context below to answer the user's question.

Context:
{context_block}

Question:
{text}

Answer:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    answer_text = response['choices'][0]['message']['content'].strip()

    return {
        "answer": answer_text,
        "link": top_chunks
    }
