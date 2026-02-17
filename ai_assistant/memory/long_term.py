import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Persistent Chroma client (disk storage)
client = chromadb.PersistentClient(path="data/memory")

# 🔹 OpenAI embedding function (needs API key)
embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="assistant_memory",
    embedding_function=embedding_function
)

def store_memory(text):
    memory_text = f"User info: {text}"
    print("STORING MEMORY:", memory_text)

    collection.add(
        documents=[memory_text],
        ids=[str(hash(memory_text))]
    )

def search_memory(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if results and results["documents"]:
        return results["documents"][0]

    return []
