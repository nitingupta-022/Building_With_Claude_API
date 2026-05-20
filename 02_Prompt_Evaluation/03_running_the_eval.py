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
        "model" : "claude-sonnet-4-6", 
        "max_tokens" : 1000, 
        "messages" : messages,
        "temperature" : temperature, 
        "stop_sequences" : stop_sequences
    }

    if system : 
        params["system"] = system 
    
    
    message = client.messages.create(**params)
    return message.content[0].text

def run_prompt(test_case) : 
    """ Merges the prompt and test case input, then returns the result """
    prompt = """
    Please solve the following task : 

    {test_case["task"]} 
    """

    messages = [] 
    add_user_message(messages, prompt) 
    output = chat(messages) 
    return output

def run_test_case(test_case) : 
    """ Calls run_prompt, then grades the result """
    output = run_prompt(test_case) 

    # TODO - Grading
    score = 10
    
    return {
        "output" : output, 
        "test_case" : test_case, 
        "score" : score 
    }

def run_eval(dataset) : 
    """ Loads the dataset and calls run_test_case with each case """
    results = [] 

    for test_case in dataset : 
        result = run_test_case(test_case)
        results.append(result) 
    
    return results



with open("dataset.json", "r") as f : 
    dataset = json.load(f) 

results = run_eval(dataset)

with open("results.json", "w") as f : 
    json.dump(results, f, indent = 2)

# print(json.dumps(results, indent = 2)) 