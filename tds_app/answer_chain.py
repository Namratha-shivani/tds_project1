from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def create_chain(retriever):
    return RetrievalQA.from_chain_type(
        llm=OpenAI(
            model_name="gpt-3.5-turbo",  # or the model supported by aipipe.org
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_BASE")), 
        retriever=retriever)
