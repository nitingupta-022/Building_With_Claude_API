""" 
- Use message prefilling and stop sequences only to get three different commands in single response. 
- Threre shouldn't be any comments or explanation
- Hint : message prefilling isn't limited to just characters like ```
"""

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

def chat(messages, system=None, temperature = 1.0, stop_sequences=[]) : 
    params = {
        "model" : "claude-opus-4-1", 
        "max_tokens" : 1000, 
        "messages" : messages,
        "temperature" : temperature, 
        "stop_sequences" : stop_sequences
    }

    if system : 
        params["system"] = system 
    
    
    message = client.messages.create(**params)
    return message.content[0].text


messages = [] 
prompt = """ 
Generate three different sample AWS CLI commands. Each should be very shorts.
"""

add_user_message(messages, prompt) 
add_assistant_message(messages, "```")

text = chat(messages, stop_sequences=["```"])
print(text.strip())