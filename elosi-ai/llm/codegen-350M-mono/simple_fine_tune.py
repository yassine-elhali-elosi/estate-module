from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

from datasets import load_from_disk

useFeedback = input("Use feedback dataset? (y/n): ")
if useFeedback == "y":
    feedback_dataset = load_dataset("json", data_files="../feedback.json")
    odoo_dataset = load_dataset("yelosi/odoo-ir-actions-server")
    
    combined_data = {
        'input': feedback_dataset['train']['input'] + odoo_dataset['train']['input'],
        'output': feedback_dataset['train']['output'] + odoo_dataset['train']['output']
    }
    dataset = Dataset.from_dict(combined_data)
else:
    dataset = load_dataset("yelosi/odoo-ir-actions-server")

# dataset = load_from_disk('ir_actions_server_dataset')
# print("Custom ir.actions.server dataset loaded")

model_name = "Salesforce/codegen-350M-mono"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# le padding token de fin
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# conversion du dataset en token pour le model
def format_and_tokenize(examples):
    formatted_texts = []

    # Remove this line as it's causing confusion
    # print(examples['train'])
    
    for i in range(len(examples['input'])):
        text = (
            f"### input:\n{examples['input'][i]}\n"
            f"### output:\n{examples['output'][i]}\n\n"
        )
        formatted_texts.append(text)

    encoded = tokenizer(
        formatted_texts,
        padding="max_length",
        max_length=512,
        truncation=True,
        return_tensors="pt"
    )

    # For training, the labels are the same as the inputs
    encoded["labels"] = encoded["input_ids"].clone()
    
    return encoded

tokenized_dataset = dataset.map(
    format_and_tokenize,
    batched=True,
    remove_columns=['input', 'output']
)

# le training
output_dir = "./fine-tuned-codegen-350M-mono"
# output_dir = "./fine-tuned-codegen-350M-mono-actions-server"

training_args = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    warmup_steps=100,
    save_strategy="epoch",
    eval_steps=10 if useFeedback == "y" else None,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=None 
)

trainer.train()
print("Training complete")

model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print("New model saved")