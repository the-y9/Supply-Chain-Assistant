import hashlib
from pdf_chunk import all_chunks
import os
from sentence_transformers import SentenceTransformer
import pickle
import faiss
import numpy as np

CACHE_DIR = "./embeddings_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_PATH = os.path.join(CACHE_DIR, "embeddings.pkl")

# Generate hash based on question texts to detect changes
def get_data_hash(data):
    texts = [entry["text"] for entry in data]
    return hashlib.md5("".join(texts).encode()).hexdigest()

def load_or_create_embeddings():
    data_hash = get_data_hash(all_chunks)

    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            cache = pickle.load(f)
        if cache.get("hash") == data_hash:
            print("Using cached embeddings.")
            return cache

    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [chunk['text'] for chunk in all_chunks]
    embeddings = model.encode(texts) # <class 'numpy.ndarray'>
    normalized_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Metadata
    metadata = []
    for chunk in all_chunks:
        metadata.append({
            'filename': chunk['filename'],
            'chunk_id': chunk['chunk_id'],
            'text': chunk['text']
        })

    # FAISS index
    dim = normalized_embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(normalized_embeddings)

    cache = {
        'hash': data_hash,
        'index': index,
        'metadata': metadata
    }

    # Save index separately since FAISS index isn't pickleable
    faiss.write_index(index, os.path.join(CACHE_DIR, "faiss.index"))

    # Save metadata and hash
    with open(CACHE_PATH, "wb") as f:
        pickle.dump({
            'hash': data_hash,
            'metadata': metadata
        }, f)

    print("Embeddings saved and indexed.")
    return cache

def search(query_text, top_k=5):
    # Load model and index
    FAISS_PATH = os.path.join(CACHE_DIR, "faiss.index")
    if not os.path.exists(FAISS_PATH):
        load_or_create_embeddings()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vec = model.encode([query_text]).astype('float32')

    # Load index
    index = faiss.read_index(os.path.join(CACHE_DIR, "faiss.index"))

    # Load metadata
    with open(CACHE_PATH, "rb") as f:
        cache = pickle.load(f)
    metadata = cache['metadata']

    # Perform search
    D, I = index.search(query_vec, top_k)

    # Get matched metadata
    results = [metadata[i] for i in I[0]]
    return results

results = search("What are audit req", top_k=3)
for r in results:
    print("-" * 60)
    print(f"{r['filename']} [{r['chunk_id']}]:\n {r['text']}")
