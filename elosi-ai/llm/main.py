from transformers import AutoTokenizer, AutoModelForCausalLM
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "fine-tuned-odoo-model")

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)

question = "How many delivery orders are there in the system?"
input_text = f"### Input:\n{question}\n### Instruction:"

inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(inputs.input_ids, max_length=200)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)