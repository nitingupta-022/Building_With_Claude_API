"""
Math Tutot Specialist System Prompt 
- Responses should : 
    - Initially, only give the student hints. 
    - Patiently walk the student through a solution. 
    - Show solutions for similar problems. 
- Responses should not : 
    - Immediately give a direct answer. 
    - Tell the student to use a calculator. 
"""

from dotenv import load_dotenv
from anthropic import Anthropic 

# Load env variables 
load_dotenv() 

client = Anthropic() 


# Helper functions 
def add_user_message(message, text) : 
    user_message = {"role" : "user", "content" : text}
    message.append(user_message)

def add_assistant_message(message, text) : 
    assistant_message = {"role" : "assistant", "content" : text} 
    message.append(assistant_message) 

"""without using the system prompt"""
# def chat(messages) : 
#     message = client.messages.create(
#         model = "claude-sonnet-4-6", 
#         max_tokens = 1000, 
#         messages = messages
#     )
#     return message.content[0].text


"""with using the system prompt"""
def chat(messages, system=None) : 
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
system = """
You are a patient math tutor. 
Do not directly answer a student's questions. 
Guide them to a solution step by step.
"""
add_user_message(messages, "How do I solve 5x + 3 = 2 for x ?")
answer = chat(messages, system = system)
print(answer)