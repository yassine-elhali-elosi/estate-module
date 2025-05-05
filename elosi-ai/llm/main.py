from transformers import AutoTokenizer, AutoModelForCausalLM
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "codegen-350M-mono/fine-tuned-codegen-350M-mono")

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)

def generate_code(prompt):
    #prompt = "How many delivery orders are there in the system?"
    input_text = f"""### system:
    You are an assistant that generates Odoo server actions using Python.
    Odoo server actions use the Odoo ORM API with methods like:
    - self.env[model_name].search(domain)
    - self.env[model_name].search_count(domain)
    Always use proper Odoo syntax with self.env and appropriate domain filters.

    ### input:
    {prompt}

    ### output:"""

    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=500)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(response)
    return response

def feedback(input_prompt, output_prompt):
    # stores feedback in a json file for future training
    feedback_data = {
        "input_prompt": input_prompt,
        "output_prompt": output_prompt
    }
    feedback_file = os.path.join(current_dir, "feedback.json")
    with open(feedback_file, "a") as f:
        f.write(str(feedback_data) + "\n")
    print("Feedback stored:", feedback_data)