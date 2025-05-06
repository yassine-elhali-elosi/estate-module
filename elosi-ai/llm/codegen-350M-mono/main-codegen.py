from transformers import AutoTokenizer, AutoModelForCausalLM

# ancien model, distilgpt2
#model_path = "./fine_tuned_odoo_model"

model_path = "./fine-tuned-codegen-350M-mono"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

input_text = """### system:
You are an assistant that generates Odoo server actions using Python.

### input:
How many products exist?

### output:"""

input_ids = tokenizer(input_text, return_tensors="pt")
generated_ids = model.generate(input_ids=input_ids.input_ids, attention_mask=input_ids.attention_mask, max_new_tokens=300)

generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

print(generated_text)