import os
import faiss
from pdf_embeddings import generate_embeddings, get_metadata, get_data_hash, save_metadata_and_hash, CACHE_PATH
from pdf_chunk import all_chunks
import pickle
from sentence_transformers import SentenceTransformer


# === Embeddings Cache Setup ===
FAISS_DIR = "./faiss"
os.makedirs(FAISS_DIR, exist_ok=True)
FAISS_PATH = os.path.join(FAISS_DIR, "faiss.index")

INDEX = None
METADATA = None

def faiss_index_exists_and_valid():
    if not os.path.exists(CACHE_PATH) or not os.path.exists(FAISS_PATH):
        return False

    current_hash = get_data_hash(all_chunks)
    with open(CACHE_PATH, "rb") as f:
        cached = pickle.load(f)

    return cached.get("hash") == current_hash


def build_faiss_index():
    embeddings = generate_embeddings()
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index

def save_faiss_index(index):
    faiss.write_index(index, FAISS_PATH)

def load_faiss_index():
    return faiss.read_index(FAISS_PATH)

def initialize_index():
    global INDEX, METADATA

    if faiss_index_exists_and_valid():
        INDEX = load_faiss_index()
        with open(CACHE_PATH, "rb") as f:
            METADATA = pickle.load(f)["metadata"]
        print("✅ Using cached FAISS index and metadata.")
        return

    print("🔄 Rebuilding FAISS index and metadata...")
    INDEX = build_faiss_index()
    METADATA = get_metadata()
    save_faiss_index(INDEX)
    save_metadata_and_hash(METADATA, get_data_hash(all_chunks))

model = SentenceTransformer('all-MiniLM-L6-v2')
def search_faiss(query_text, model = model, top_k=5):
    if INDEX is None or METADATA is None:
        initialize_index()

    query_vec = model.encode([query_text]).astype("float32")
    D, I = INDEX.search(query_vec, top_k)
    return D, [METADATA[i] for i in I[0]]


if __name__ == "__main__":
    while True:
        print("-x-" * 20)
        query = input("Enter your query: ")
        if query.lower() in ["exit", "quit"]:
            break
        scores, results = search_faiss(query, top_k=3)
        for i, r in enumerate(results):
            print("-" * 60)
            print(f"Score: {scores[0][i]:.2f}")
            print(f"{r['filename']} [{r['chunk_id']}]:\n {r['text']}")