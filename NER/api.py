from flask import Flask,request, jsonify
import os
import spacy
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
input_dir = MODEL_DIR

app = Flask(__name__)
CORS(app)

nlp = spacy.load(input_dir)

@app.route('/predict', methods=['POST'])
def predict():
    test_text = request.json["text"]
    try:
        doc = nlp(test_text)
        for ent in doc.ents:
            return jsonify(ent.label_, ent.text), 200
    except Exception as e:
        print(e)
        return jsonify({"result": "Model failed"})

if __name__ == '__main__':
    app.run('0.0.0.0',port=8000)
