from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def get_retriever(chunks):
    vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
    return vectorstore.as_retriever()
