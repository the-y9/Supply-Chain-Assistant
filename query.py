


from model_services.api_models import call_model
from policy_services.pdf_answering import answering_main
from supply_chain_services.data_query import data_query_main


def intent_classifier(prompt):
    instruction = (
        f"Classify the intent of the following prompt:\n\n"
        f"\"{prompt}\"\n\n"
        f"Determine whether it requires:\n"
        f"- Policy information (e.g., rules, definitions, procedures)\n"
        f"- Data (e.g., transactional records, statistics, numbers)\n"
        f"- Or both.\n\n"
        f"Rules:\n"
        f"- If the prompt needs a definition, rule, or procedural explanation, classify as 'policy'.\n"
        f"- If it needs transactional data, statistics, or numbers, classify as 'data'.\n"
        f"- If it requires both kinds of information, classify as 'both'.\n\n"
        f"Respond with only one word: 'data', 'policy', or 'both'."
    )
    
    response = call_model(instruction, i=0)
    
    try:
        result = response['content'][0]['text'].strip().lower()
        if result in {'data', 'policy', 'both'}:
            return result
        else:
            return 'error'
    except (KeyError, IndexError, AttributeError):
        return 'error'



def query_main(prompt):
    intent = intent_classifier(prompt).lower()

    if intent == 'data':
        sql_query, sql_response, answer = data_query_main(prompt)
        return {"sql_query": sql_query, "sql_response": sql_response, "answer": answer, "intent": intent}
    
    elif intent == 'policy':
        answer, sources = answering_main(prompt)
        return {"policy_answer": answer, "policy_sources": sources, "intent": intent}
        # print(f"Referred Policy Sources: {sources}")
        # print(f"Policy Answer: {answer}")

    elif intent == 'both':
        policy_answer, policy_sources = answering_main(prompt)
        # print(f"Referred Policy: {policy_answer}")

        if 'Info not found' in policy_answer:
            data_answer = "No relevant policy information found."
            sql_query = "Failed to generate SQL query due to missing policy information."
            return {"policy_answer": policy_answer, "policy_sources": policy_sources, "intent": intent, "data_answer": data_answer, "sql_query": sql_query}
        
        data_answer, sql_query = data_query_main(prompt, policy=policy_answer)
        # print(f"Used SQL Query: {sql_query}")
        # print(f"Aggregated Answer: {data_answer}")
        return {
            "policy_answer": policy_answer,
            "policy_sources": policy_sources,
            "data_answer": data_answer,
            "sql_query": sql_query,
            "intent": intent
        }