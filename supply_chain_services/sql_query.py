import sqlite3
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, util

# Load model and tokenizer
model_name = "mrm8488/t5-small-finetuned-wikiSQL"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Flan-T5 small for SQL validation
validation_model_name = "google/flan-t5-small"
val_tokenizer = AutoTokenizer.from_pretrained(validation_model_name)
val_model = AutoModelForSeq2SeqLM.from_pretrained(validation_model_name)


# SQLite config
sqlite_db_path = 'supply_chain.db'
table_name = 'supply_chain'

# Load embedding model for fuzzy matching
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_table_columns():
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return columns

def fuzzy_column_match(query_part, columns):
    query_embedding = embed_model.encode(query_part, convert_to_tensor=True)
    col_embeddings = embed_model.encode(columns, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, col_embeddings)[0]
    best_idx = scores.argmax().item()
    return columns[best_idx]

def preprocess_prompt(prompt, columns):
    phrases = re.findall(r'\b[a-zA-Z ]{4,}\b', prompt)
    replacements = {}

    for phrase in phrases:
        phrase_clean = phrase.lower().strip()
        best_col = fuzzy_column_match(phrase_clean, columns)
        # Replace only if phrase looks like a column, but don't overwrite intent words
        if best_col.lower() != phrase_clean and best_col.lower() not in prompt.lower():
            replacements[phrase] = best_col

    # Replace only the matching phrases, keep the rest intact
    for phrase, col in replacements.items():
        # Use case-insensitive replacement for the phrase within the prompt
        prompt = re.sub(re.escape(phrase), col, prompt, flags=re.IGNORECASE)

    return prompt


def prompt_to_sql(prompt: str, table_name = table_name):
    input_text = f"translate English to SQL: {prompt}"
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=128)
    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    sql = re.sub(r"\btable\b", table_name, sql)

    return sql

def validate_sql(question, sql_query, columns=None):
    prompt = (
        f"Question: {question}\n"
        f"SQL Query: {sql_query}\n"
        f"{columns}\n"
        "Please check if the SQL query is syntactically correct and if all the column names exist in the table schema. "
        "If there are errors, provide the corrected SQL query. Otherwise, confirm that the query is correct."
    )
    inputs = val_tokenizer(prompt, return_tensors="pt")
    outputs = val_model.generate(**inputs, max_length=256)
    answer = val_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def run_sql_query(sql: str):
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()
        return column_names, rows
    except sqlite3.Error as e:
        conn.close()
        return None, f"SQL error: {e}"

def main():
    columns = get_table_columns()
    while True:
        
        prompt = input("Enter your question about the supply chain data:\n> ")
        if not prompt.strip():
            print("Exiting...")
            break
        preprocessed_prompt = preprocess_prompt(prompt, columns)
        print(f"\nPreprocessed Prompt: {preprocessed_prompt}")

        sql_query = prompt_to_sql(preprocessed_prompt)
        print("\nGenerated SQL Query:")
        print(sql_query)

        validation_response = validate_sql(prompt, sql_query, columns)
        print("Validation Response:")
        print(validation_response)
        
        decision = str(input("Which query to execute? (gen/val/no): ").strip().lower())
        if decision == 'gen':
            column_names, result = run_sql_query(sql_query)
            if column_names is None:
                print(result)
            else:
                print("\nQuery Results:")
                print("\t".join(column_names))
                for row in result:
                    print("\t".join(str(c) for c in row))

        elif decision == 'val':
            column_names, result = run_sql_query(validation_response)
            if column_names is None:
                print(result)
            else:
                print("\nQuery Results:")
                print("\t".join(column_names))
                for row in result:
                    print("\t".join(str(c) for c in row))

if __name__ == "__main__":
    main()
