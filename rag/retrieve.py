import chromadb
from sentence_transformers import SentenceTransformer


# =====================================================
# CHROMADB SETUP
# =====================================================

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="debate_docs"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =====================================================
# RETRIEVE CONTEXT
# =====================================================

def retrieve_context(query, top_k=3):

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = results.get("documents", [])

    if not documents:

        return ""

    if len(documents[0]) == 0:

        return ""

    context = "\n".join(documents[0])

    return context