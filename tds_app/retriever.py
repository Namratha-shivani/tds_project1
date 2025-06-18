from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

def get_retriever(chunks):
    embedding = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.environ["OPENAI_API_KEY"],
        openai_api_base="https://aipipe.org/v1"
    )
    vectorstore = FAISS.from_documents(chunks, embedding)
    return vectorstore.as_retriever()
