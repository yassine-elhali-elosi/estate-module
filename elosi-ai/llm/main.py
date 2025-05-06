from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "codegen-350M-mono/fine-tuned-codegen-350M-mono")

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

def generate_code(prompt):
    # Clean format without any indentation
    input_text = f"""### input:
{prompt}

### output:"""
    
    input_ids = tokenizer(input_text, return_tensors="pt")
    generated_ids = model.generate(
        input_ids=input_ids.input_ids, 
        attention_mask=input_ids.attention_mask, 
        max_new_tokens=150,  # Reduce max tokens to prevent wandering
        pad_token_id=tokenizer.eos_token_id,
        # Lower temperature for more deterministic output
        do_sample=False,  # Switch to greedy decoding
        num_beams=3,  # Use beam search instead
        repetition_penalty=1.5,  # Increase repetition penalty
        # Stop at specific tokens
        eos_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    print("Raw response:")
    print(response)
    
    # Extract only the output section
    try:
        parts = response.split("### output:")
        if len(parts) > 1:
            output = parts[1].strip()
            # Remove any text after another section marker if present
            if "###" in output:
                output = output.split("###")[0].strip()
            return output
        else:
            return response  # Return the whole response if parsing fails
    except Exception as e:
        print(f"Error parsing response: {e}")
        return response

def feedback(feedback_value, input_prompt, output_prompt):
    input_prompt = input_prompt.replace('"', '\\"')

    feedback_raw_file = os.path.join(current_dir, "feedback_raw.json")
    with open(feedback_raw_file, "a") as f:
        f.write("{\"feedback_value\": \"" + feedback_value + "\", \"input_prompt\": \"" + input_prompt + "\", \"output_prompt\": \"" + output_prompt + "\"}\n")

    if feedback_value == "yes":
        feedback_file = os.path.join(current_dir, "feedback.json")
        with open(feedback_file, "a") as f:
            f.write("{\"input_prompt\": \"" + input_prompt + "\", \"output_prompt\": \"" + output_prompt + "\"}\n")
    #print("Feedback stored:", feedback_data)