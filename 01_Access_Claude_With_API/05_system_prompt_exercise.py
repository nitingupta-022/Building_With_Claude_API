from dotenv import load_dotenv
from anthropic import Anthropic 

load_dotenv() 
client = Anthropic() 

# Helper functions 
def add_user_message(messages, text) : 
    user_message = {"role" : "user", "content" : text} 
    messages.append(user_message) 

def add_assistant_message(messages, text) : 
    assistant_message = {"role" : "assistant", "content" : text}
    messages.append(assistant_message)

def chat(messages, system = None) : 
    params = {
        "model" : "claude-sonnet-4-6", 
        "max_tokens" : 1000, 
        "messages" : messages, 
    } 

    if system : 
        params["system"] = system

    message = client.messages.create(**params) 
    return message.content[0].text 



messages = [] 

add_user_message(messages, "Write a Python function that checks a string for duplicate characters.")
answer = chat(messages, system = "You ae a Python engineer who writes very concise code.")
print(answer)