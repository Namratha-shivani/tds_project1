from langchain.document_loaders import DirectoryLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_documents():
    base_path = os.path.dirname(__file__)  # tds_app/

    md_path = os.path.join(base_path, "data", "tds_content")
    json_path = os.path.join(base_path, "data", "discourse_threads")

    md_loader = DirectoryLoader(md_path, glob="**/*.md")
    json_loader = DirectoryLoader(json_path, glob="**/*.json", loader_cls=JSONLoader)

    docs = md_loader.load() + json_loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(docs)
