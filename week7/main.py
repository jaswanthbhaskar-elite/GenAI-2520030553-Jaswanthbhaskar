
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load a small pretrained language model
MODEL_NAME = "distilgpt2"

print("=" * 60)
print("NEXT-TOKEN PROBABILITY INSPECTION")
print("=" * 60)

print("\nLoading model:", MODEL_NAME)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

model.eval()

# Input prompt
prompt = "Artificial intelligence is"

print("\nInput Prompt:", prompt)

# Convert text into token IDs
inputs = tokenizer(prompt, return_tensors="pt")

print("\nInput Token IDs:")
print(inputs["input_ids"][0].tolist())

print("\nInput Tokens:")
print(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))

# Generate model predictions without calculating gradients
with torch.no_grad():
    outputs = model(**inputs)

# Extract logits for the next token
logits = outputs.logits[0, -1, :]

print("\nNext Token Logits:")
print(logits)

# Convert logits into probabilities
probabilities = torch.softmax(logits, dim=-1)

# Find the Top-K candidates
top_k = 10
top_probs, top_ids = torch.topk(probabilities, top_k)

print("\n" + "=" * 60)
print(f"TOP {top_k} NEXT-TOKEN CANDIDATES")
print("=" * 60)

print(f"{'Rank':<8}{'Token':<25}{'Token ID':<12}{'Probability':<15}")
print("-" * 60)

for rank, (token_id, probability) in enumerate(
    zip(top_ids, top_probs), start=1
):
    token = tokenizer.decode([token_id.item()])

    print(
        f"{rank:<8}{repr(token):<25}"
        f"{token_id.item():<12}{probability.item():.6f}"
    )

print("\nMost likely next token:")
print(repr(tokenizer.decode([top_ids[0].item()])))

print("\nExperiment completed successfully!")
