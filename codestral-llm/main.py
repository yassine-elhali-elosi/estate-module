from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json

def save_dataset(data):
    with open("llm_dataset.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

model = OllamaLLM(model="codellama:7b")

template = """
You are an expert Odoo backend developer.
Only return the Python code — no explanations, no comments.
The code must be valid, safe, and ready to run inside an Odoo server action.
You understand models like res.partner, sale.order, crm, and typical business flows.
Always assume the env variable is available.
Use clear logic and avoid hardcoded IDs.
Import libraries where necessary.

Here is the prompt:
{input_prompt}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

input_prompt = input("Prompt: ")
result = chain.invoke(
    {
        "input_prompt": input_prompt,
    }
)
print(result)

# ask for feedback to train
feedback = input("Satisfied? (yes/no/fix): ")

if feedback == "yes":
    save_dataset({"feedback": "accepted"})