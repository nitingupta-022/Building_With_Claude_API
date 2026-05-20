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

 
 # Example of response streaming with the API. This is useful for long responses, as it allows you to process the response as it is generated, rather than waiting for the entire response to be generated before processing it.
"""
messages = [] 

add_user_message(messages, "Write a 1 sentence description of a fake database.") 

stream = client.messages.create(
    model = "claude-sonnet-4-6", 
    max_tokens = 1000, 
    messages = messages, 
    stream = True
)

for event in stream : 
    print(event) 
""" 

# Here I get the text chunk by chunk. This is useful for long responses, as it allows you to process the response as it is generated, rather than waiting for the entire response to be generated before processing it.
messages = [] 

add_user_message(messages, "Write a 1 sentence description of a fake database.")

with client.messages.stream(
    model = "claude-sonnet-4-6", 
    max_tokens = 1000, 
    messages = messages
) as stream : 
    for text in stream.text_stream : 
        print(text, end = "")


# This will return the final message, which is the complete response from the model. This is useful if you want to process the entire response at once, rather than processing it as it is generated.
# stream.get_final_message()