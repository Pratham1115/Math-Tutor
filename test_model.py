# test_model.py

from transformers import AutoModelForCausalLM, AutoTokenizer

# Use a base model (you can replace with your fine-tuned model later)
model_name = "tiiuae/falcon-7b-instruct"
print("Loading model, this may take a few minutes...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to explain any math topic
def explain_topic(topic):
    inputs = tokenizer(f"Explain {topic} from basics with examples", return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=200)
    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return explanation

# Example usage
topic = input("Enter a math topic you want explained: ")
result = explain_topic(topic)
print("\nAI Explanation:\n", result)
