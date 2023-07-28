import urequests
import machine
import time

import json

api_key = "insert your API Key"
chatgpt_url = "https://api.openai.com/v1/chat/completions"
chatgpt_ver= "gpt-3.5-turbo"

def send_prompt_to_chatGPT(prompt):
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": f"{chatgpt_ver}",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = urequests.post(chatgpt_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = json.loads(response.text)

        body = response_data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API error ({response.status_code}): {response.text}")
        
    return body

def chat_with_chatGPT():

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    while True:
        prompt= input("user: ")
        if prompt == '>exit':
            break

        chat_data = {
            "model": f"{chatgpt_ver}",
            "messages": [{"role": "user", "content": prompt}]
        }
            
        response = urequests.post(chatgpt_url, headers=headers, data=json.dumps(chat_data))
        if response.status_code == 200:
            response_data = json.loads(response.text)
            body = response_data["choices"][0]["message"]["content"]
            print(">chatGPT: ", body)
        else:
            raise Exception(f"API error ({response.status_code}): {response.text}")
        
