# policy_services/pdf_faiss.py
import os
import faiss
from policy_services.pdf_embeddings import load_embeddings, get_metadata, get_data_hash, save_metadata_and_hash
from policy_services.pdf_embeddings import CACHE_DIR, EMBEDDING_PATH, METADATA_PATH
from policy_services.pdf_chunk import all_chunks
import pickle
from model_services.api_models import call_model
import numpy as np


# === Embeddings Cache Setup ===
FAISS_PATH = os.path.join(CACHE_DIR, "faiss.index")

INDEX = None
METADATA = None

def embeddings_exists_and_valid():
    if not os.path.exists(METADATA_PATH):
        return False

    current_hash = get_data_hash(all_chunks)
    with open(METADATA_PATH, "rb") as f:
        cached = pickle.load(f)

    return cached.get("hash") == current_hash


def build_faiss_index():
    embeddings = load_embeddings()

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index

def save_faiss_index(index):
    faiss.write_index(index, FAISS_PATH)

def load_faiss_index():
    if not os.path.exists(FAISS_PATH):
        print("🔄 Building FAISS index ...")
        INDEX = build_faiss_index()
        save_faiss_index(INDEX)
    return faiss.read_index(FAISS_PATH)

def initialize_index():
    global INDEX, METADATA

    if embeddings_exists_and_valid():
        INDEX = load_faiss_index()
        with open(METADATA_PATH, "rb") as f:
            METADATA = pickle.load(f)["metadata"]
        return

    print("🔄 Building metadata and index...")
    METADATA = get_metadata()
    INDEX = load_faiss_index()
    save_metadata_and_hash(METADATA, get_data_hash(all_chunks))

def search_faiss(query_text, top_k=5):
    if INDEX is None or METADATA is None:
        initialize_index()

    embeddings = call_model(query_text, i=2)  # using amazon-embedding-v2
    query_vec = np.array(embeddings["embedding"])
    if query_vec.ndim == 1:
        query_vec = query_vec.reshape(1, -1)  # Ensure it's 2D for FAISS
    # normalized = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)
    D, I = INDEX.search(query_vec, top_k)
    return D, [METADATA[i] for i in I[0]]


def faiss_main():
    while True:
        print("-x-" * 20)
        query = input("Enter your query: ")
        if query.lower() in ["exit", "quit"]:
            break
        try:
            scores, results = search_faiss(query, top_k=3)
            for i, r in enumerate(results):
                print("-" * 60)
                print(f"Score: {scores[0][i]:.2f}")
                print(f"{r['filename']} [{r['chunk_id']}]:\n {r['text']}")
        except Exception as e:
            print(f"Error during search: {e}")