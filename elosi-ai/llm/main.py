from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json

MODEL = OllamaLLM(model="codellama:7b")

TEMPLATE = """
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

def save_local_dataset(data):
    with open("raw_dataset.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

def save_training_dataset(data_ollama_format):
    with open("training_dataset.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(data_ollama_format) + "\n")

def generate_code(input_prompt):
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    chain = prompt | MODEL

    result = chain.invoke(
        {
            "input_prompt": input_prompt,
        }
    )
    
    return result

    """
    # ask for feedback to train
    feedback = input("Satisfied? (yes/no/fix): ")

    if feedback == "yes":
        save_local_dataset({
            "prompt": input_prompt,
            "result": result,
            "feedback": "accepted"
        })
        save_training_dataset({
            "prompt": input_prompt,
            "completion": result
        })

    elif feedback == "no":
        save_local_dataset({
            "prompt": input_prompt,
            "result": result,
            "feedback": "refused"
        })
        # on save pas dans le training

    elif feedback == "fix":
        correction = input("Type the corrected code: ")
        save_local_dataset({
            "prompt": input_prompt,
            "result": result,
            "feedback": "corrected",
            "correction": correction
        })
        save_training_dataset({
            "prompt": input_prompt,
            "completion": correction
        })
    """