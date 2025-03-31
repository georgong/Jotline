from flask import Flask, send_from_directory, request, jsonify, render_template
import os
import json

app = Flask(__name__, static_folder='static', template_folder='templates')
SAVE_FILE = 'saved_notes.json'


@app.route('/llm', methods=['POST'])
def mock_llm():
    data = request.get_json()
    prompt = data.get('prompt', '')

    # 匹配 \[hello]
    if "\\[hello]" in prompt:
        return jsonify({"reply": "hello human"})
    else:
        return jsonify({"reply": ""})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_notes():
    data = request.get_json()
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/load', methods=['GET'])
def load_notes():
    if not os.path.exists(SAVE_FILE):
        return jsonify({'status': 'empty', 'data': {}})
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500