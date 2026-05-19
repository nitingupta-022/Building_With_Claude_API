"""
Chat Bot Exercise
"""

from dotenv import load_dotenv 
from anthropic import Anthropic 

# Load env variables 
load_dotenv() 

# Create an API client 
client = Anthropic() 


# helper functions 

def add_user_message(messages, text) : 
    user_message = {"role" : "user", "content" : text} 
    messages.append(user_message) 

def add_assistant_message(messages, text) : 
    assistant_message = {"role" : "assistant", "content" : text}
    messages.append(assistant_message)

def chat(messages) : 
    message = client.messages.create(
        model = "claude-sonnet-4-6", 
        max_tokens = 300,
        messages = messages
    )
    return message.content[0].text


messages = [] 
print("""Type 'exit' to quit the chat bot.""")
while True : 
    user_input = input(">> ")
    if user_input.lower() == "exit" : 
        break 
    
    add_user_message(messages, user_input) 
    response = chat(messages)
    add_assistant_message(messages, response) 
    print(">>", response, "\n")         