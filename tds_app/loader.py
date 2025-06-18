from langchain_community.document_loaders import DirectoryLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def json_loader_factory(filepath):
    return JSONLoader(
        file_path=filepath,
        jq_schema=".post_stream.posts[].cooked",  # or any other field you want
        text_content=False  # This puts raw HTML as content; set to True to strip HTML tags
    )

def load_documents():
    md_loader = DirectoryLoader("tds_app/data/tds_content/", glob="**/*.md")
    json_loader = DirectoryLoader(
        "tds_app/data/discourse_threads/",
        glob="**/*.json",
        loader_cls=json_loader_factory
    )

    docs = md_loader.load() + json_loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(docs)

