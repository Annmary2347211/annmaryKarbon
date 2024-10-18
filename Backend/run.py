import json
from flask import Flask, jsonify, request
from model import probe_model_5l_profit  # Correct import from model.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    # Assuming it's a JSON file
    data = file.read().decode("utf-8")
    json_data = json.loads(data)
    
    # Pass the data to model.py and get the result
    result = probe_model_5l_profit(json_data["data"])
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
