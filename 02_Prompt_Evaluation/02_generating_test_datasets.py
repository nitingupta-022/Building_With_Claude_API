from dotenv import load_dotenv
from anthropic import Anthropic 
import json

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

def generate_dataset() : 
    prompt = """
    Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompt that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON each representing task that required Python, JSON, or Regex to complete.

    Example ouput : 

    ```json
    [
        {
            "task" : "Description of task",
            "format" : "python/json/regex"
        }, 
        ...additional
    ]
    ```

    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, 
    * Focus on tasks that do not require writing much code.

    Please generate 3 objects. 
    """

    messages = [] 
    add_user_message(messages, prompt) 
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text)



dataset = generate_dataset()

with open("dataset.json", "w") as f : 
    json.dump(dataset, f, indent=4)