# policy_services/pdf_answering.py
from policy_services.pdf_faiss import search_faiss
from model_services.api_models import call_model
import json

def generate_answer(query, docs):

    prompt = (
    "Provide brief and the most accurate answer strictly based on the policy documents. Give theoutput that can be displayed in a web application directly. "
    "If the query is complex or contains multiple components, break it down into smaller parts to extract all relevant definitions or interpretations. "
    "Ensure each part is addressed comprehensively and clearly. "
    "If the answer cannot be found within the provided context, respond with 'Info not found.'\n\n"
    f"Policy Documents:\n{docs}\n\n"
    f"Query:\n{query}\n\n"
    "Answer:"
)


    # Call Claude or other model via your API
    response = call_model(prompt, i=1)  # 0 = "claude-3-haiku"
    return response['content'][0]['text']

def answering_main(query):
        scores, results = search_faiss(query, top_k=3)
        if not results:
            return "No relevant documents found."
        answer = generate_answer(query, [r['text'] for r in results])
        sources = set([r['filename'] for r in results])

        return answer, list(sources)
