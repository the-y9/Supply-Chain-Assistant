# policy_services/pdf_embeddings.py
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import pickle
import numpy as np
from policy_services.pdf_chunk import all_chunks
from model_services.api_models import call_model
from tqdm import tqdm



# === Embeddings Cache Setup ===
CACHE_DIR = "./cache"
os.makedirs(CACHE_DIR, exist_ok=True)
EMBEDDING_PATH = os.path.join(CACHE_DIR, "embeddings.pkl")
METADATA_PATH = os.path.join(CACHE_DIR, "metadata.pkl")

def get_data_hash(data):
    texts = [entry["text"] for entry in data]
    return hashlib.md5("".join(texts).encode()).hexdigest()


def save_metadata_and_hash(metadata, data_hash):
    with open(METADATA_PATH, "wb") as f:
        pickle.dump({'metadata': metadata, 'hash': data_hash}, f)

def get_metadata():
    return [{
        'filename': chunk['filename'],
        'chunk_id': chunk['chunk_id'],
        'text': chunk['text']
    } for chunk in all_chunks]

def load_metadata():
    with open(METADATA_PATH, "rb") as f:
        return pickle.load()['metadata']

def generate_embeddings():
    print("🔄 Generating embeddings...")
    texts = [entry["text"] for entry in all_chunks]
    embeddings = []
    
    num_cores = os.cpu_count()
    print(f"Number of CPU cores: {num_cores}")
    worker_input = int(input("Enter the number of workers: "))
    max_workers = (worker_input or 2* num_cores)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(call_model, text, i=2): text for text in texts}

        for future in tqdm(as_completed(futures), total=len(futures)):
            response = future.result()
            embeddings.append(response["embedding"])

    embeddings = np.array(embeddings)
    # normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    save_embedding(embeddings, get_data_hash(all_chunks))
    return embeddings

def save_embedding(embeddings, data_hash):
    with open(EMBEDDING_PATH, "wb") as f:
        pickle.dump({"embeddings": embeddings, "hash": data_hash}, f)

def load_embeddings():
    if not os.path.exists(EMBEDDING_PATH):
        generate_embeddings() 
    print("📦 Loading cached embeddings...") 
    with open(EMBEDDING_PATH, "rb") as f:
        cached = pickle.load(f)
    return cached["embeddings"]

def embeddings_exist_and_valid():
    """Check if embeddings cache exists and matches current data hash."""
    if not os.path.exists(EMBEDDING_PATH):
        return False
    current_hash = get_data_hash(all_chunks)
    with open(EMBEDDING_PATH, "rb") as f:
        cached = pickle.load(f)
    return cached.get("hash") == current_hash

# def load_or_generate_embeddings():

#     embeddings = load_embeddings()
#     metadata = load_metadata()
#     data_hash = get_data_hash(all_chunks)
#     save_metadata_and_hash(metadata, data_hash)
#     return metadata
