import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

load_dotenv()
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

model = None

def setup_api():
    global model
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: API key not found.")
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        print(f"API config error: {str(e)}")
        return None

def generate_poem(word_phrase, model=None):
    if model is None:
        model = setup_api()
        if model is None:
            return "API setup failed."

    prompt = f"""Write a poem inspired by "{word_phrase}".
- Use vivid imagery, metaphors, and emotion.
- Avoid clichés.
- Around 12-16 lines.
- Use your creativity!"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/generate_poem', methods=['POST'])
def generate_poem_route():
    data = request.get_json()
    word_phrase = data.get('word_phrase', '')
    poem = generate_poem(word_phrase, model)
    return jsonify({'poem': poem})

if __name__ == '__main__':
    model = setup_api()
    app.run(host='0.0.0.0', port=5000, debug=True)
