from dotenv import load_dotenv
from anthropic import Anthropic 

# Load env variables
load_dotenv()

# Create an API client 
client = Anthropic()
model = "claude-sonnet-4-5"

message = client.messages.create(
    model=model, 
    max_tokens=1000, 
    messages=[
        {
            "role" : "user", 
            "content" : "What is qunatum computing. Explain in one sentence ? "
        }
    ]
)

# print(message)
# print()
print(message.content[0].text)