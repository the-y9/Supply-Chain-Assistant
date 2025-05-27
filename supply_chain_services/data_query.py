from model_services.api_models import call_model
import sqlite3
from policy_services.pdf_answering import generate_answer

db = 'supply_chain.db'
table_name = 'supply_chain'
columns = ['Benefit per order', 'Category Id', 'Category Name', 'Customer City', 'Customer Country', 'Customer Email', 'Customer Fname', 'Customer Id', 'Customer Lname', 'Customer Password', 'Customer Segment', 'Customer State', 'Customer Street', 'Customer Zipcode', 'Days for shipment (scheduled)', 'Days for shipping (real)', 'Delivery Status', 'Department Id', 'Department Name', 'Late_delivery_risk', 'Latitude', 'Longitude', 'Market', 'Order City', 'Order Country', 'Order Customer Id', 'Order Id', 'Order Item Cardprod Id', 'Order Item Discount', 'Order Item Discount Rate', 'Order Item Id', 'Order Item Product Price', 'Order Item Profit Ratio', 'Order Item Quantity', 'Order Item Total', 'Order Profit Per Order', 'Order Region', 'Order State', 'Order Status', 'Order Zipcode', 'Product Card Id', 'Product Category Id', 'Product Description', 'Product Image', 'Product Name', 'Product Price', 'Product Status', 'Sales', 'Sales per customer', 'Shipping Mode', 'Type', 'order date (DateOrders)', 'shipping date (DateOrders)']

def sqlite_query(query):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return "Error executing sql query"
    finally:
        conn.close()


def prompt_to_sql(prompt, policy=None):
    if policy:
        instruction = (f"Only Generate a SQL query nothing else for the following prompt: {prompt}"
                    f"\nThe table name is {table_name}, the column names are {columns}."
                    f"\nDo not modify the table name or column names, and do not add any additional columns or tables."
                    f"\nUse column names in double quotes."
                    f"\nUse the logic of the policy {policy} to generate the SQL query."
                       )
    else:
        instruction = (f"Only Generate a SQL query nothing else for the following prompt: {prompt}"
                   f"\nThe table name is {table_name} and the column names are {columns}."
                   f"\nDo not modify the table name or column names, and do not add any additional columns or tables."
                   f"\nUse column names in double quotes.")
    response = call_model(instruction, i=0)
    return response['content'][0]['text']


def refine_answer(prompt, response):
    instruction = (
        f"Refine the respone {response} to the prompt: {prompt} to give accurate answer based on sqlite response\n"
    )
    answer = call_model(instruction, i=0)
    return answer['content'][0]['text']


def data_query_main(prompt, policy=None):    
    sql_query = prompt_to_sql(prompt, policy)
    print(f"Used SQL Query: {sql_query}")

    sql_response = sqlite_query(sql_query)
    print(f"{len(sql_response)} rows returned from SQL query.")
    # print(f"SQL Response: {sql_response}")
    max_preview_rows = 50
    flag = False
    if isinstance(sql_response, list) and len(sql_response) > max_preview_rows:
        sql_response = sql_response[:max_preview_rows]
        flag = True

    answer = refine_answer(prompt, sql_response)
    if flag:
        answer += "\n\nNote: The SQL response was too large for model call, hence it is truncated to the first 50 rows for preview purposes."
    print(f"SQL Refined Answer: {answer}")

    return sql_query, sql_response, refine_answer(prompt, sql_response)
