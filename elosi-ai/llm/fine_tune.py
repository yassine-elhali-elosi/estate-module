import json
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType
import torch

def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [json.loads(line.strip()) for line in f if line.strip()]
    return Dataset.from_list(lines)

dataset = load_data("training_dataset.jsonl")

model_name = "Salesforce/codegen-350M-mono"

tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
)

model = get_peft_model(model, peft_config)

def tokenize(sample):
    full_prompt = f"### Prompt:\n{sample['prompt']}\n\n### Completion:\n{sample['completion']}"
    tokenized = tokenizer(full_prompt, truncation=True, padding="max_length", max_length=512)
    tokenized["labels"] = tokenized["input_ids"].copy()
    tokenized["labels"] = [label if label != tokenizer.pad_token_id else -100 for label in tokenized["labels"]]
    return tokenized

tokenized_dataset = dataset.map(tokenize, remove_columns=["prompt", "completion"])

args = TrainingArguments(
    output_dir="./codegen_lora_training_output",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()

model.save_pretrained("codegen_lora_adapter")
tokenizer.save_pretrained("codegen_lora_adapter")
print("✅ Adapter saved in codegen_lora_adapter/")
# ------------------------------------