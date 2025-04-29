from transformers import AutoTokenizer, AutoModelForCausalLM
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "fine-tuned-codegen")

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)

def generate_code(prompt):
    #prompt = "How many delivery orders are there in the system?"
    input_text = f"### Input:\n{prompt}\n### Instruction:"

    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=200)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(response)
    return response