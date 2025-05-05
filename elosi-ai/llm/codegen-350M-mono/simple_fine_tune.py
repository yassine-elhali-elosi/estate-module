from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

from datasets import load_from_disk

dataset = load_dataset("yelosi/odoo-ir-actions-server")
print("Dataset loaded")
print("Dataset structure:", dataset)  # Print dataset structure to understand what we're working with

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

    for i in range(len(examples['input'])):
        text = (
            f"### input:\n{examples['input'][i]}\n"
            f"### output:\n{examples['output'][i]}\n\n"
        )
        formatted_texts.append(text)

    #print(formatted_texts)

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

# Process each split in the dataset
tokenized_dataset = {}
for split in dataset.keys():
    tokenized_dataset[split] = dataset[split].map(
        format_and_tokenize,
        batched=True,
        remove_columns=dataset[split].column_names
    )

# If the dataset doesn't already have train/test splits, create them
if 'train' not in tokenized_dataset:
    if 'train' not in dataset:
        # If there's no explicit train split, use the first available split and create a train/test split
        first_split = list(dataset.keys())[0]
        train_test = dataset[first_split].train_test_split(test_size=0.1)
        tokenized_dataset = {
            'train': train_test['train'].map(
                format_and_tokenize,
                batched=True,
                remove_columns=train_test['train'].column_names
            ),
            'test': train_test['test'].map(
                format_and_tokenize,
                batched=True,
                remove_columns=train_test['test'].column_names
            )
        }

# le training
output_dir = "./fine-tuned-codegen-350M-mono"
# output_dir = "./fine-tuned-codegen-350M-mono-actions-server"

training_args = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=5,
    per_device_train_batch_size=4,
    warmup_steps=100,
    save_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['test'] if 'test' in tokenized_dataset else None,
)

trainer.train()
print("Training complete")

model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print("New model saved")