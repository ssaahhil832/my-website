from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load a pre-trained conversational model
model_name = "microsoft/DialoGPT-medium"  # You can replace this with other conversational models
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

app = Flask(__name__)

# AI Chatbot logic
def generate_response(user_input, chat_history_ids=None):
    # Tokenize user input
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    
    # Append tokens to chat history (for context)
    bot_input_ids = new_input_ids if chat_history_ids is None else torch.cat([chat_history_ids, new_input_ids], dim=-1)

    # Generate a response
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return bot_response, chat_history_ids

# API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("user_input")

    # Use the chatbot logic to generate a response
    bot_response, _ = generate_response(user_input)
    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
