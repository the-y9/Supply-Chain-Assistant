# model_services/api_models.py
from dotenv import load_dotenv
import requests
import os
import json
from time import time
start_time = time()
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")
BASE_URL = 'https://quchnti6xu7yzw7hfzt5yjqtvi0kafsq.lambda-url.eu-central-1.on.aws/'


def call_model(prompt, i=0):
    models = ['claude-3-haiku', "claude-3.5-sonnet", "amazon-embedding-v2"]

    payload = {
                    "api_key": API_KEY,
                    "prompt": prompt,
                    "model_id": models[i],
                    "model_params": {
                    "max_tokens": 1024,
                    "temperature": 0.7
                    }
                }
 

    response = requests.post(BASE_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    return response.json().get('response', 'Error')



if __name__ == "__main__":
    prompts = [
        "What is the capital of France?",
        "Explain the theory of relativity in simple terms."
    ]
    try:
        response = call_model("one", i=2) 
        with open("response.json", "w") as f:
            f.write(str(response))
        # response = batch_generate_embeddings(prompts)
        # print(len(response))
    except Exception as e:
        print(f"Error calling model: {e}")