import json
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType
import torch

# Load your dataset
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [json.loads(line.strip()) for line in f if line.strip()]
    return Dataset.from_list(lines)

dataset = load_data("training_dataset.jsonl")

# Load tokenizer and model
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

# Apply LoRA
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
)

model = get_peft_model(model, peft_config)

# Preprocessing function
def tokenize(sample):
    full_prompt = f"### Prompt:\n{sample['prompt']}\n\n### Completion:\n{sample['completion']}"
    tokenized = tokenizer(full_prompt, truncation=True, padding="max_length", max_length=512)
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize, remove_columns=["prompt", "completion"])

# Training arguments
args = TrainingArguments(
    output_dir="./tinyllama_lora",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()

# Save the adapter
model.save_pretrained("tinyllama_lora_adapter")
tokenizer.save_pretrained("tinyllama_lora_adapter")
print("✅ Adapter saved in tinyllama_lora_adapter/")
