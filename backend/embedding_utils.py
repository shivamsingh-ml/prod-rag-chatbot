from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

client = QdrantClient(host="qdrant", port=6333)

def ensure_collection(collection_name: str):
    if collection_name not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def upload_documents_to_qdrant(documents, collection_name: str):
    Qdrant.from_documents(
        documents=documents,
        embedding=embedding_model,
        location="http://qdrant:6333",
        collection_name=collection_name,
    )

def delete_collection(collection_name: str):
    try:
        client.delete_collection(collection_name=collection_name)
        return True
    except Exception as e:
        print(f"Error deleting collection '{collection_name}': {e}")
        return False
