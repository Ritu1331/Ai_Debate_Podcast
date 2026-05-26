from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import os

DATA_PATH = "./data"
DB_PATH = "./chroma_db"

def ingest_documents():

    print("Starting ingestion...")

    documents = []

    for file in os.listdir(DATA_PATH):

        print(f"Found file: {file}")

        if file.endswith(".pdf"):

            loader = PyPDFLoader(
                os.path.join(DATA_PATH, file)
            )

            loaded_docs = loader.load()

            print(f"Loaded {len(loaded_docs)} pages")

            documents.extend(loaded_docs)

    print(f"Total documents: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=DB_PATH
    )

    print("Documents ingested successfully!")

if __name__ == "__main__":
    ingest_documents()