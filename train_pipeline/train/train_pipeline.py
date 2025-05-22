from unsloth import FastVisionModel, is_bf16_supported
from unsloth.trainer import UnslothVisionDataCollator
from trl import SFTTrainer
import os 


def load_model_and_tokenizer(model_id):
    model, tokenizer = FastVisionModel.from_pretrained(
        model_id, load_in_4bit=True, use_gradient_checkpointing="unsloth"
    )
    model = FastVisionModel.get_peft_model(
        model, finetune_vision_layers=True, finetune_language_layers=True,
        finetune_attention_modules=True, finetune_mlp_modules=True,
        r=16, lora_alpha=16, lora_dropout=0, bias="none",
        random_state=3443, use_rslora=False, loftq_config=None
    )
    FastVisionModel.for_training(model)
    return model, tokenizer

def train_model(model, tokenizer, dataset, config):
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        data_collator=UnslothVisionDataCollator(model, tokenizer),
        train_dataset=dataset,
        args=config
    )
    return trainer
