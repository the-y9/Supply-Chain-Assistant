


from model_services.api_models import call_model
from policy_services.pdf_answering import answering_main
from supply_chain_services.data_query import data_query_main
import json

columns = ['Benefit per order', 'Category Id', 'Category Name', 'Customer City', 'Customer Country', 'Customer Email', 'Customer Fname', 'Customer Id', 'Customer Lname', 'Customer Password', 'Customer Segment', 'Customer State', 'Customer Street', 'Customer Zipcode', 'Days for shipment (scheduled)', 'Days for shipping (real)', 'Delivery Status', 'Department Id', 'Department Name', 'Late_delivery_risk', 'Latitude', 'Longitude', 'Market', 'Order City', 'Order Country', 'Order Customer Id', 'Order Id', 'Order Item Cardprod Id', 'Order Item Discount', 'Order Item Discount Rate', 'Order Item Id', 'Order Item Product Price', 'Order Item Profit Ratio', 'Order Item Quantity', 'Order Item Total', 'Order Profit Per Order', 'Order Region', 'Order State', 'Order Status', 'Order Zipcode', 'Product Card Id', 'Product Category Id', 'Product Description', 'Product Image', 'Product Name', 'Product Price', 'Product Status', 'Sales', 'Sales per customer', 'Shipping Mode', 'Type', 'order date (DateOrders)', 'shipping date (DateOrders)']

def intent_classifier(prompt):
    instruction = (
        f"You are the entry point for classifying the intent of a prompt related to supply chain management.\n"
        f"You are an expert in supply chain management and data analysis. Your task is to classify the intent of a given prompt.\n\n"
        f" If the prompt is a greet or general query or something like that, which is not associated with supply-chain, then classify it as 'general'. Otherwise\n"
        f"Analyze the columns [{columns}] and Classify the intent of the following prompt:\n\n"
        f"\"{prompt}\"\n\n"
        f"Determine whether it requires:\n"
        f"- Policy information (e.g., rules, definitions, procedures)\n"
        f"- Data (e.g., transactional records, statistics, numbers)\n"
        f"- Or both.\n\n"
        f"Rules:\n"
        f"- If the prompt needs a definition, rule, or procedural explanation, classify as 'policy'.\n"
        f"- If it needs transactional data, statistics, or numbers, classify as 'data'.\n"
        f"- If it requires standards, metric, rule, or both kinds of information, for the logic of query classify as 'both'.\n\n"
        f"Respond with only one word: 'data', 'policy', or 'both'."
        f" If it is a greet or general query or something like that, which is not associated with supply-chain directly, then classify it as 'general'.\n"
    )
    
    response = call_model(instruction, i=0)
    
    try:
        result = response['content'][0]['text'].strip().lower()
        if result in {'data', 'policy', 'both', 'general'}:
            return result
        else:
            return 'error'
    except (KeyError, IndexError, AttributeError):
        return 'error'


def query_main(prompt, intent=None):
    if not intent:
        intent = intent_classifier(prompt).lower()

    if intent == 'data':
        sql_query, sql_response, answer = data_query_main(prompt)
        return {"sql_query": sql_query, "sql_response": sql_response, "answer": answer, "intent": intent}
    
    elif intent == 'policy':
        answer, sources = answering_main(prompt)
        return {"answer": answer, "policy_sources": sources, "intent": intent}
        # print(f"Referred Policy Sources: {sources}")
        # print(f"Policy Answer: {answer}")

    elif intent == 'both':
        policy_answer, policy_sources = answering_main(prompt)
        print(f"Referred Policy: {policy_answer}")
        # yield json.dumps({"policy_answer": policy_answer, "policy_sources": policy_sources, "intent": intent}) + "\n"

        if 'Info not found' in policy_answer:
            data_answer = "No relevant policy information found."
            sql_query = "Failed to generate SQL query due to missing policy information."
            answer = policy_answer + data_answer
            return {"answer": answer, "policy_sources": policy_sources, "intent": intent, "sql_query": sql_query}
        
        sql_query, sql_response, data_answer = data_query_main(prompt, policy=policy_answer)
        # print(f"Used SQL Query: {sql_query}")
        # print(f"Aggregated Answer: {data_answer}")
        return {
            "policy_answer": policy_answer,
            "policy_sources": policy_sources,
            "answer": data_answer,
            "sql_query": sql_query,
            "sql_response": sql_response,
            "intent": intent
        }
        # yield json.dumps({
        #     "data_answer": data_answer,
        #     "sql_query": sql_query
        # })

    elif intent == 'general':
        response = call_model(prompt, i=0)
        return {"answer": response['content'][0]['text'], "intent": intent}
    
def query_policy(prompt, intent="policy"):
    return query_main(prompt, intent=intent)

def query_data(prompt, intent="data"):
    return query_main(prompt, intent=intent)

def query_both(prompt, intent="both"):
    return query_main(prompt, intent=intent)