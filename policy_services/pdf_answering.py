from transformers import pipeline
from pdf_faiss import search_faiss

model_name = "google/flan-t5-base"

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

if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        if not query.strip():
            print("Exiting...")
            break
        scores, results = search_faiss(query, top_k=3)
        if not results:
            print("No relevant documents found.")
            continue
        answer = generate_answer(query, results)
        print(f"Answer: {answer}")
        print(f"Sources: {set([r['filename'] for r in results])}")
        print("-" * 60)