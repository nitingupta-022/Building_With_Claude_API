![alt text](Images/01.png)

# Tool Functions

![alt text](Images/02.png)

- Plain python function that will be executed when Claude decides it needs some additional information to help the user. 
- `Best practices` 
    - Use well-named, descriptive arguments. 
    - Validate the inputs, raising an error if they fail validation. 
    - Return meaningful errors - Calude will try to call to use your function a second time!

```python
def get_weather(location) : 
    if not location or location.strip() == "" : 
        raise ValueError("Location cannot be empty")
    
    url = "https://fakeweatherapi.example.com/current"
    params = {
        "q" : location, 
        "appid" : api_key, 
        "units" : "metric" 
    }

    response = request.get(url, params=params, timeout = 10)
    response.raise_for_status()

    return response.json() 
```

# Tool Schemas

![alt text](Images/03.png)

`Write a JSON Schema spec to describe your function`
- The JSON Schema helps Claude understand what arguments your function requires. 
- JSON Schema is not just a LLM thing - this is a commonly used for data validation. 
    - There are tons of tools online that can help you generate a JSON Schema. 
- `Best practices` 
    - Explain what the tool does, when to use it, and what it returns. 
    - Aim for 3 to 4 sentences
    - Provide super detailed descriptions. 

```json
{
    "name" : "get_weather", 
    "description" : "Retreives current weather", 
    "input_schema" : {
        "type" : "object", 
        "properties" : {
            "location" : {
                "type" : "string", 
                "description" : "The location for which ..."
            }
        },
        "required" : [
            "location"
        ]
    }
}
```

![alt text](Images/04.png)


# Handling message blocks

![alt text](Images/05.png)

## Single-Block messages 

![alt text](Images/06.png)

## Multi-Block messages 

![alt text](Images/07.png)

## Managing Conversation History with Multi-Block Messages 

![alt text](Images/08.png)

# Sending Tool Results

![alt text](Images/09.png)

![alt text](Images/10.png)

![alt text](Images/11.png)

## Tool Result Block 

- Placed the 'content' list of a user message 
- Communicates the results of running a tool function back to Claude
- `tool_use_i` - Must match the id of the ToolUse block that this ToolResult corresponds to 
- `content` - Output from running your tool, serialized as a string
- `is_error` - True if an error occured

```json
{
    "tool_use_id" : "toolu_01BEbi7q7qz",
    "type" : "tool_result",
    "content" : "12:47:13",
    "is_error" : False
}
```

## There might be multiple `ToolUse` blocks!

![alt text](Images/12.png)

# Multi-Turn convesations With Tools 

![alt text](Images/13.png)

## Tools Use Improvements 

![alt text](Images/14.png)


# Implementing Mutlitple Turns

## Stop Reason

Tells use why Claude stopped generating text 
- "tool_use" : Claude has decided that it needs to call a tool 
- "end_turn" : Calude has finished generating it's assistant message. 
- "max_tokens" : Claude has hit the token output limit and can't generate any more output. 
- "stop_sequence" : Claude has encounter one of your provided stop sequences. 

## Conversation with tools 

- Provide an initial list of messages. 
- Feed messages into Claude
- `If Claude ins't asking for a tool use`, then we must have a final answe to send back to our user. 
- `If Claude wants to use a tool`, then we will run the tool, put the results into a user message, and run Claude again. 

```python
def run_conversation(messages) : 
    while True : 
        response = chat(messages) 

        add_user_message(messages, response)

        # Pseudo code 
        if response isnt asking for a tool : 
            break 
        
        tool_result_blocks = run_tools(response)
        add_user_message(tool_result_blocks)

    return messages
```


![alt text](Images/15.png)

![alt text](Images/16.png)

# Fine Grained Tool Calling 

![alt text](Images/17.png)

## Basic Tool Streaming

![alt text](Images/18.png)

![alt text](Images/19.png)

## How JSON Validation Works

![alt text](Images/20.png)

```json
{
    "abstract" : "This paper presents a novel...",
    "meta" : {
        "word_count" : 847,
        "review" : "This paper introduces QuanNet..."
    }
}
```

Top Level Key : Value

- abstract : "This paper presents a novel..."
- meta : {"word_count" : 847, "review" : "This paper ..."}

![alt text](Images/21.png)

![alt text](Images/22.png)

![alt text](Images/23.png)

## fine gradined tool calling 

- Sometimes you want ot get each chunk of generated JSON as fast as possible. 
- Fine grainded tool calling sends `groups` of chunks without waiting for a full top level key to be created. 
- `Critical` : JSON validation is disabled! Your code should hanlde invalid tool inputs!

## When to Use Fine-Grained Tool Calling

Consider enabling fine-grained tool calling when : 
- You need to show users real-time progress on tool argument generation
- You want to start processing partial tool results as quickly as possible
- The buffering delays negatively impact your user experience
- You're comfortable implementing robust JSON error handling

For most applications, the default behavior with validation is perfectly adequate. But when you need that extra responsiveness, fine-grained tool calling gives you the control to get chunks as fast as Claude can generate them.

# The Text Edit Tool 

Claude comes with one built-in tool that you don't need to create from scratch : the text editor tool. This tool gives Claude the ability to work with files and directories just like you would in a standard text editor.

## What the text editor tool can do ? 

The text editor tool provides Claude with a comprehesive set of file manipulation capabilities : 

![alt text](Images/24.png)

This dramatically expands Claude's abilities and essentially gives it the power to act as a software engineer right out of the gate.

## Understanding the Implementation Requirements

Here's where things get a bit confusing: while the tool schema is built into Claude, you still need to provide the actual implementation. Think of it this way - Claude knows how to ask for file operations, but you need to write the code that actually performs those operations.

![alt text](Images/25.png)

![alt text](Images/26.png)

When you use other tools, you write both the JSON schema and the function implementation. With the text editor tool, Claude provides the schema knowledge, but you must write functions to handle Claude's requests to create files, read directories, replace text, and so on.

## Schema Versions 

While the main schema is built into Claude, you do need to include a small schema stub when making requests. The exact schema depends on which Claude model you're using:

```python
def get_text_edit_schema(model):
    if model.startswith("claude-3-7-sonnet"):
        return {
            "type": "text_editor_20250124",
            "name": "str_replace_editor",
        }
    elif model.startswith("claude-3-5-sonnet"):
        return {
            "type": "text_editor_20241022", 
            "name": "str_replace_editor",
        }
```

## Practical Example

Let's see the text editor tool in action. When you ask Claude to work with files, it will use the tool to read, modify, and create files as needed.

For example, if you ask Claude to "Open the ./main.py file and summarize its contents", Claude will:

1. Use the text editor tool to view the file
2. Read the contents
3. Provide you with a summary

You can take this further by asking Claude to modify files. For instance: "Open the ./main.py file and write out a function to calculate pi to the 5th digit. Then create a ./test.py file to test your implementation."

Claude will:

1. View the existing main.py file
2. Replace its contents with a new implementation including the pi calculation function
3. Create a new test.py file with appropriate unit tests

## Why Use the Text Editor Tool?

You might wonder why this tool exists when modern code editors already have AI assistants built in. The text editor tool becomes valuable in scenarios where:

- You're building applications that need to programmatically edit files
- You're working in environments without access to full-featured code editors
- You want to integrate file editing capabilities directly into your Claude-powered applications

Essentially, the text editor tool lets you replicate much of the functionality of a fancy AI-powered code editor within your own applications, giving you fine-grained control over how Claude interacts with your file system.

# The Web Search Tool 

Claude includes a built-in web search tool that lets it search the internet for current or specialized information to answer user questions. Unlike other tools where you need to provide the implementation, Claude handles the entire search process automatically - you just need to provide a simple schema to enable it.

![alt text](Images/27.png)

## Setting Up the Web Search Tool

To use the web search tool, you create a schema object with these required fields:

```json
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search", 
    "max_uses": 5
}
```

The max_uses field limits how many searches Claude can perform. Claude might do follow-up searches based on initial results, so this prevents excessive API calls. A single search returns multiple results, but Claude may decide additional searches are needed.

## How the Response Works

When Claude uses the web search tool, the response contains several types of blocks:

- Text blocks - Claude's explanation of what it's doing
- ServerToolUseBlock - Shows the exact search query Claude used
- WebSearchToolResultBlock - Contains the search results
- WebSearchResultBlock - Individual search results with titles and URLs
- Citation blocks - Text that supports Claude's statements

![alt text](Images/28.png)

The response structure lets you see exactly what Claude searched for and which sources it found. Citations include the specific text Claude used to support its answers, along with the source URLs.

## Restricting Search Domains

You can limit searches to specific domains using the allowed_domains field. This is particularly useful when you want reliable, authoritative sources:

```json
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": ["nih.gov"]
}
```

For example, when asking about medical or exercise advice, restricting to domains like PubMed (nih.gov) ensures you get evidence-based information rather than random blog content.

![alt text](Images/29.png)

## Rendering Search Results
The different block types in the response are designed for specific UI rendering:

Render text blocks as regular content
Display web search results as a list of sources at the top
Show citations inline with the text, including the source domain, page title, URL, and quoted text.

![alt text](Images/30.png)

This structure helps users understand how Claude arrived at its answers and provides transparency about the sources being used. The citation format makes it clear which specific information came from which sources, building trust in the AI's responses.

## Practical Usage

The web search tool works best for:

- Current events and recent developments
- Specialized information not in Claude's training data
- Fact-checking and finding authoritative sources
- Research tasks requiring up-to-date information
- Simply include the schema in your tools array when making API calls, and Claude - will automatically decide when a web search would help answer the user's question.
