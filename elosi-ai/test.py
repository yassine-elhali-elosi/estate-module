import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)

mistral_response = client.agents.complete(
    agent_id = "ag:7e1f4155:20250410:untitled-agent:a8450e92",
    messages=[
        {
            "role": "user",
            "content": "I need a server action that adds a tag 'VIP' to all customers with more than 10 sales."
        }
    ]
)

print(mistral_response.choices[0].message.content)