from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor

def save_and_push(model, tokenizer, processor, base_model, save_method, repo, token):
    model.save_pretrained_merged(base_model, tokenizer, save_method=save_method)
    
    model = AutoModelForCausalLM.from_pretrained(base_model)
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    processor = AutoProcessor.from_pretrained(base_model)

    model.push_to_hub(repo, token=token)
    tokenizer.push_to_hub(repo, token=token)
    processor.push_to_hub(repo, token=token)
