import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json
import os

# MODEL = OllamaLLM(model="codellama:7b")

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel
from langchain.llms import HuggingFacePipeline
import torch

def load_finetuned_model():
    adapter_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "codegen_lora_adapter"))
    
    base_model = AutoModelForCausalLM.from_pretrained(
        "Salesforce/codegen-350M-mono",
        device_map="cpu"
    )
    model = PeftModel.from_pretrained(
        base_model,
        adapter_path,
        device_map="cpu"
    )
    tokenizer = AutoTokenizer.from_pretrained(adapter_path)

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=300)
    return HuggingFacePipeline(pipeline=pipe)

MODEL = load_finetuned_model()

TEMPLATE = """
You are an expert Odoo backend developer.
Only return the Python code — no explanations, no comments.
The code must be valid, safe, and ready to run inside an Odoo server action.
You understand models like res.partner, sale.order, crm, and typical business flows.
Always assume the env variable is available.
Use clear logic and avoid hardcoded IDs.
Import libraries where necessary.
**Do not include** quotes before and after the code, it should be pure code and ready to execute.

Here is the prompt:
{input_prompt}
"""

def save_local_dataset(data):
    print("Saving local dataset...", data)
    file_path = os.path.join(os.path.dirname(__file__), "raw_dataset.jsonl")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")
        f.flush()

def save_training_dataset(data_ollama_format):
    print("Saving training dataset...", data_ollama_format)
    file_path = os.path.join(os.path.dirname(__file__), "training_dataset.jsonl")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data_ollama_format) + "\n")
        f.flush()

def generate_code(input_prompt):
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    chain = prompt | MODEL

    result = chain.invoke(
        {
            "input_prompt": input_prompt,
        }
    )
    print(result)
    return result

def feedback(value, input_prompt, result):
    # ask for feedback to train
    print(value, input_prompt, result)

    if value == "yes":
        print("--------------")
        save_local_dataset({
            "prompt": input_prompt,
            "result": result,
            "feedback": "accepted"
        })
        save_training_dataset({
            "prompt": input_prompt,
            "completion": result
        })

    elif value == "no":
        save_local_dataset({
            "prompt": input_prompt,
            "result": result,
            "feedback": "refused"
        })
        # on save pas dans le training

    elif value == "fix":
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

    print("Feedback saved.")