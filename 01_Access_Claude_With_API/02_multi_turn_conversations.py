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

def add_assistant_message(message, text) : 
    assistant_message = {"role" : "assistant", "content" : text} 
    message.append(assistant_message) 

def chat(messages) : 
    message = client.messages.create(
        model="claude-sonnet-4-6", 
        max_tokens=1000,
        messages = messages
    )
    return message.content[0].text


# Step 1 : Make a starting list of messages
messages = []  

# Step 2 : Add in the inital user question
add_user_message(messages, "What is quantum computing. Explain in one sentence ?")

# Step 3 : Get the assistant response and add it to the messages list
response = chat(messages) 

# Step 4 : Add the assistant response to the messages list 
add_assistant_message(messages, response) 

# Step 5 : Add a follow up question to the messages list 
add_user_message(messages, "Write anothersentence.")

# Step 6 : Take the assistant response to the follow up question
response = chat(messages) 
add_assistant_message(messages, response) 

print(response)