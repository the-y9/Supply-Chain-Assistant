from transformers import pipeline
from pdf_faiss import search_faiss

model_name = "google/flan-t5-base" # A faster and more accurate model

generator = pipeline('text2text-generation', model=model_name)

def generate_answer(query, docs):
    context = " ".join([d['text'] for d in docs])
    # print(context)
    # print("+" * 60)
    prompt = (
    "Answer the query based on the context. If the context doesn't contain the answer, respond with 'Info not found.'\n\n"
    f"Context: {context}\n\n"
    f"Query: {query}\n\n"
    "Answer:"
)

    response = generator(prompt,  do_sample=False)
    return response[0]['generated_text']
