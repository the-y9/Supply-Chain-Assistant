import os
import hashlib
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from pdf_chunk import all_chunks

# === Embeddings Cache Setup ===
CACHE_DIR = "./embeddings_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_PATH = os.path.join(CACHE_DIR, "embeddings.pkl")

def get_data_hash(data):
    texts = [entry["text"] for entry in data]
    return hashlib.md5("".join(texts).encode()).hexdigest()

def generate_embeddings():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [chunk['text'] for chunk in all_chunks]
    embeddings = model.encode(texts)
    normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return normalized

def get_metadata():
    return [{
        'filename': chunk['filename'],
        'chunk_id': chunk['chunk_id'],
        'text': chunk['text']
    } for chunk in all_chunks]

def save_metadata_and_hash(metadata, data_hash):
    with open(CACHE_PATH, "wb") as f:
        pickle.dump({'metadata': metadata, 'hash': data_hash}, f)

def load_metadata():
    with open(CACHE_PATH, "rb") as f:
        return pickle.load()['metadata']

def embeddings_exist_and_valid():
    """Check if embeddings cache exists and matches current data hash."""
    if not os.path.exists(CACHE_PATH):
        return False
    current_hash = get_data_hash(all_chunks)
    with open(CACHE_PATH, "rb") as f:
        cached = pickle.load(f)
    return cached.get("hash") == current_hash

def load_or_generate_embeddings():
    """Main entry point: load metadata if embeddings are valid; otherwise generate."""
    if embeddings_exist_and_valid():
        print("✅ Using cached embeddings.")
        return load_metadata()
    
    print("🔄 Generating new embeddings...")
    embeddings = generate_embeddings()
    metadata = get_metadata()
    data_hash = get_data_hash(all_chunks)
    save_metadata_and_hash(metadata, data_hash)
    return metadata
