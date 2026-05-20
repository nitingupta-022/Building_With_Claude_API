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

def chat(messages, system = None, temperature = 1.0) : 
    params = {
        "model" : "claude-sonnet-4-6", 
        "max_tokens" : 1000, 
        "messages" : messages, 
        # temperature controls the randomness of the output. Higher values (e.g., 0.8) make the output more random, while lower values (e.g., 0.2) make it more focused and deterministic.
        "temperature" : temperature   
    } 

    if system : 
        params["system"] = system

    message = client.messages.create(**params) 
    return message.content[0].text 



messages = [] 

add_user_message(
    messages, 
    "Generate a one senetence movie idea."
)

answer = chat(messages, temperature = 1.0)
print(answer)