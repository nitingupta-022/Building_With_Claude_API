"""
Exercise Task : 
- Give the Model
- Grader more context on what a good solution looks like 


Steps to follow :
1. Update the dataset generation prompt to ask for some "solution criteria" to be include for each test case.
2. Update the 'grade_by_model' prompt to include that solution criteria
"""



import re
import string
import json
import ast 
from dotenv import load_dotenv
from anthropic import Anthropic 
from statistics import mean 

load_dotenv()
client = Anthropic() 

# Helper functions
def add_user_message(messages, text) : 
    user_message = {"role" : "user", "content" : text}
    messages.append(user_message)

def add_assistant_message(messages, text) : 
    assistant_message = {"role" : "assistant", "content" : text}
    messages.append(assistant_message) 

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
    Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompt that generate Python, JSON or Regex specifically for AWS-related tasks. Generate an array of each representing task that requires Python, JSON or Regex to complete.

    Example ouput : 
    ```json
    [
        {
            "task" : "Description of task",
            "format" : "json" or "python" or "regex",
            "solution_criteria" : "key criteria for evaluating the solution"
        },
        ...additional tasks
    ]
    ```

    * Focus on tasks that can be solved by writing a single python function, a single JSON object, or a single regex pattern.
    * Focus on tasks that do not require writing much code.

    Please generate 3 objects.
    """

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text)

dataset = generate_dataset()
with open("dataset_02.json", "w") as f : 
    json.dump(dataset, f, indent=4)

def run_prompt(test_case) : 
    """ Merges the prompt and test case input, then returns the result """
    prompt = f"""
    Please solve the following task : 

    {test_case["task"]}

    * Respond only with Python, JSON, or plain Regex
    * Do not add any comments or commentary or explnation
    """

    system_prompt = "You are an experienced AWS engineer with a hyper focus addressing constraints and edge cases. You are solving the task for a non-technical audience, so clarity and simplicity is key. Focus on writing concise code that directly addresses the task without any extra commentary or explanation."

    messages = [] 
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")
    output = chat(messages, system=system_prompt, stop_sequences=["```"])
    return output

def grade_by_model(test_case, output) : 
    """ Grades the output by asking the model to evaluate it """
    eval_prompt = f"""
    You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution. 

    Original Task :
    <task>
    {test_case["task"]}
    </task>

    AI-Generated Solution :
    <solution>
    {output}
    </solution>

    Criteria you should use to evaluate the solution : 
    <criteria>
    {test_case["solution_criteria"]}
    </criteria>

    Output Format 
    Provide your evaluation as a structured JSON object with  the following fields in this specific order : 
    - "strengths" : An array of 1-3 key strengths
    - "weaknesses" : An array of 1-3 key areas for improvement
    - "reasoning" : A concise explanation of your overall assessment
    - "score" : A number b/w 1-10.

    Respond with JSON. Keep your response concise and direct. 
    Example response shape : 
    {{
        "strengths" : string[], 
        "weaknesses" : string[], 
        "reasoning" : string, 
        "score" : number
    }}
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)

def validate_json(text) : 
    """ Validates if the provided text is a valid JSON object. """
    try : 
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError : 
        return 0
    
def validate_python(text) : 
    """ Validates if the provided text is a valid python code. """
    try : 
        ast.parse(text.strip()) 
        return 10
    except SyntaxError : 
        return 0       

def validate_regex(text) : 
    """ Validates if the provided text is a valid regex pattern. """
    try : 
        re.compile(text.strip())
        return 10
    except re.error : 
        return 0

def grade_syntax(response, test_case) : 
    """ Grades the syntax of the response based on the expected format in the test case. """
    format = test_case["format"]
    if format == "json" : 
        return validate_json(response)
    elif format == "python" : 
        return validate_python(response)
    else :
        return validate_regex(response)
    
def run_test_case(test_case) : 
    """ Calls run_prompt, then grades the result """
    output = run_prompt(test_case)

    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    syntax_score = grade_syntax(output, test_case)

    score = (model_score + syntax_score) / 2

    return {
        "output" : output,
        "test_case" : test_case,
        "score" : score,
        "reasoning" : reasoning
    }

def run_eval(dataset) : 
    """ Loads the dataset and calls run_test_case with each case """
    results = [] 

    for test_case in dataset : 
        result = run_test_case(test_case)
        results.append(result) 
    
    average_score = mean([result["score"] for result in results])
    print(f"Average Score : {average_score}")

    return results




with open("dataset_02.json", "r") as f : 
    dataset = json.load(f)

results = run_eval(dataset)

with open("results_02.json", "w") as f : 
    json.dump(results, f, indent = 4)