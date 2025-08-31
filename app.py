import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pytesseract
import PyPDF2
import speech_recognition as sr
from PIL import Image

from prompts import get_prompt

load_dotenv()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ⚙️ Utility


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()

    try:
        if ext in ['png', 'jpg', 'jpeg']:
            image = Image.open(filepath)
            return pytesseract.image_to_string(image)
        elif ext == 'pdf':
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == 'wav':
            recognizer = sr.Recognizer()
            with sr.AudioFile(filepath) as source:
                audio = recognizer.record(source)
            return recognizer.recognize_google(audio)
    except Exception as e:
        return f"Error processing file: {e}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'file_path': filepath})
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/run_agent', methods=['POST'])
def run_agent():
    agent = request.form.get('agent')
    model = request.form.get('model')
    input_type = request.form.get('input_type')
    user_input = ""

    if input_type == 'text':
        user_input = request.form.get('text_input', '').strip()
    elif input_type == 'file':
        file_path = request.form.get('uploaded_file_path')
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Uploaded file not found'}), 400
        user_input = extract_text_from_file(file_path)

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    prompt_template = get_prompt(agent)
    full_prompt = f"{prompt_template}\n\nUser Input:\n{user_input}"

    # 🧠 Replace with real model API call here
    response = fake_llm_response(model, full_prompt)
    return jsonify({'response': response})


def fake_llm_response(model, prompt):
    # Placeholder for LLM API call
    return f"[Model: {model}] Response to prompt:\n\n{prompt}"


if __name__ == '__main__':
    app.run(debug=True)
