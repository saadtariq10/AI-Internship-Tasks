# # app.py

# from flask import Flask, request, jsonify
# import requests
# from config import LLM_API_URL, LLM_API_KEY

# app = Flask(__name__)

# @app.route('/generate', methods=['POST'])
# def generate_response():
#     try:
#         # Parse JSON data from the request
#         data = request.get_json()

#         # Validate the input data
#         if 'input' not in data:
#             return jsonify({"error": "Invalid input format. Please provide 'input' key."}), 400

#         user_input = data['input']

#         # Set up headers and call the Hugging Face API
#         headers = {
#             'Authorization': f'Bearer {LLM_API_KEY}',
#             'Content-Type': 'application/json'
#         }
#         llm_response = requests.post(LLM_API_URL, json={"inputs": user_input}, headers=headers)

#         # Check if the request was successful
#         if llm_response.status_code != 200:
#             return jsonify({"error": "Failed to get response from LLM API.", "details": llm_response.json()}), llm_response.status_code

#         # Process and return the LLM response
#         response_data = llm_response.json()
#         generated_text = response_data[0].get("generated_text", "No response generated")
#         return jsonify({"response": generated_text}), 200

#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": str(e)}), 500
#     except Exception as e:
#         return jsonify({"error": "An unexpected error occurred."}), 500

# if __name__ == '__main__':
#     app.run(debug=True)














from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Initialize the Flask app
app = Flask(__name__)

# Load the model and tokenizer (for direct use without pipeline)
tokenizer = AutoTokenizer.from_pretrained("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")
model = AutoModelForCausalLM.from_pretrained("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")

# Set up a pipeline for text generation
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Define the POST endpoint for the API
@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Get the JSON input from the user
        user_input = request.json.get("input")
        
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Generate the response using the LLM pipeline
        response = pipe(user_input, max_length=150, num_return_sequences=1)

        # Return the response
        return jsonify({"response": response[0]['generated_text']}), 200

    except Exception as e:
        # Handle errors (e.g., invalid input or API issues)
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
