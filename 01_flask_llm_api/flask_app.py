from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Route for LLM processing
@app.route('/')
def index():
    return 'Hello, World! This is task: Build a Flask Project Integrating LLMs with API Testing'
                                     
@app.route('/api/generate', methods=['POST'])
def generate_response():
    try:
        # Ensure the request is in JSON format
        user_input = request.get_json()

        if 'input' not in user_input:
            return jsonify({'error': 'Invalid input format. Please provide "input" field in JSON.'}), 400

        # Get user input
        prompt = user_input['input']

        # Call the LLM API (e.g., Hugging Face)
        api_key = "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"  # Replace with your key
        api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {"inputs": prompt}

        # Make a request to the LLM API
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code != 200:
            return jsonify({'error': 'LLM API request failed.'}), 500

        # Get LLM response
        generated_text = response.json()[0]['generated_text']
        return jsonify({'response': generated_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
