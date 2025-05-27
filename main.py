from policy_services.pdf_faiss import faiss_main, search_faiss
# from policy_services.pdf_answering import answering_main
# from supply_chain_services.data_query import data_query_main
from query import query_main


if __name__ == "__main__":
    prompt = """
    Based on our Risk Management framework, which supply chain disruptions occurred in the past year that exceeded our defined risk tolerance thresholds, and what was their financial impact?
"""
    # prompt = """
    # supply chain disruptions
    # """
    # s, results = search_faiss(prompt)
    # print([r['text'] for r in results])

    print(query_main(prompt))