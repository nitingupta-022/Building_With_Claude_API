from dotenv import load_dotenv
from anthropic import Anthropic 

load_dotenv() 
client = Anthropic() 

# Helper functions 
def add_user_message(message, text) : 
    user_message = {"role" : "user", "content" : text}
    message.append(user_message)

def add_assistant_message(message, text) : 
    assistant_message = {"role" : "assistant", "content" : text} 
    message.append(assistant_message) 

def chat(messages, system=None, stop_sequences=None) : 
    params = {
        "model" : "claude-sonnet-4-6", 
        "max_tokens" : 1000, 
        "messages" : messages,
    }

    if system : 
        params["system"] = system 
    
    if stop_sequences : 
        params["stop_sequences"] = stop_sequences 

    message = client.messages.create(**params)
    return message.content[0].text



messages = [] 
add_user_message(messages, "Generate a very short event bridge rule as json. Return only the json, no markdown.")
answer = chat(messages) 
print(answer)