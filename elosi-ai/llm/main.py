from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "codegen-350M-mono/fine-tuned-codegen-350M-mono")

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

def generate_code(prompt):
    # Remove indentation and use a clean format
    input_text = f"""### system:
You are an assistant that generates Odoo server actions using Python.

### input:
{prompt}

### output:"""
    
    input_ids = tokenizer(input_text, return_tensors="pt")
    generated_ids = model.generate(
        input_ids=input_ids.input_ids, 
        attention_mask=input_ids.attention_mask, 
        max_new_tokens=300,
        pad_token_id=tokenizer.eos_token_id,
        # Add parameters to improve generation quality
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        #repetition_penalty=1.2,
        # Add a stopping criteria
        eos_token_id=tokenizer.encode("### system")[0]  # Stop when it tries to start a new system block
    )

    response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    print("Raw response:")
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