from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = Flask(__name__)

# Load your fine-tuned model and tokenizer
model_path = "llama-2-7b-chat-stack-overflow"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)


@app.route('/prompt', methods=['POST'])
def prompt():
    prompt = request.json['prompt']

    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
    result = pipe(f"<s>[INST] {prompt} [/INST]")
    response = result[0]['generated_text']

    #reformat
    idx = response.find("[/INST]") + 8
    response = response[idx:]

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True, port=9090)
