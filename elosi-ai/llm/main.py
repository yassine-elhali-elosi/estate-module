from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_odoo_model")
model = AutoModelForCausalLM.from_pretrained("./fine_tuned_odoo_model")

question = "How many delivery orders are there in the system?"
input_text = f"### Input:\n{question}\n### Instruction:"

inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(inputs.input_ids, max_length=200)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)