# policy_services/pdf_answering.py
from policy_services.pdf_faiss import search_faiss
from model_services.api_models import call_model
import json

def generate_answer(query, docs):

    prompt = (
        "Using policy documents give the most accurate answer only. If the context doesn't contain the answer, respond with 'Info not found.'\n\n"
        f"Policy Documents: {docs}\n\n"
        f"Query: {query}\n\n"
        "Answer:"
    )

    # Call Claude or other model via your API
    response = call_model(prompt, i=0)  # 0 = "claude-3-haiku"
    return response['content'][0]['text']

def answering_main(query):
        scores, results = search_faiss(query, top_k=3)
        if not results:
            return "No relevant documents found."
        answer = generate_answer(query, [r['text'] for r in results])
        sources = set([r['filename'] for r in results])

        return answer, sources
