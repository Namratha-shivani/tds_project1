from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from .loader import load_documents
from retriever import get_retriever
from answer_chain import create_chain
from ocr import extract_text

# Setup
chunks = load_documents()
retriever = get_retriever(chunks)
qa_chain = create_chain(retriever)

# FastAPI setup
app = FastAPI()

class Attachment(BaseModel):
    filename: str
    data: str

class Query(BaseModel):
    question: str
    attachments: List[Attachment] = []

@app.post("/api/")
async def answer(query: Query):
    full_question = query.question
    for att in query.attachments:
        full_question += "\n" + extract_text(att.data)

    result = qa_chain({"query": full_question})

    # Get source links
    docs = retriever.get_relevant_documents(full_question)
    links = [{"url": doc.metadata.get("source", ""), "text": doc.page_content[:150]} for doc in docs[:3]]

    return {"answer": result["result"], "links": links}
