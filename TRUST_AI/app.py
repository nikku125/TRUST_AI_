from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load Model
model_path = 'model.pkl'
vectorizer_path = 'vectorizer.pkl'

# Global variables for model and vectorizer
model = None
vectorizer = None

def load_model():
    global model, vectorizer
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            print("Model and Vectorizer loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("Model/Vectorizer not found. Please run train_model.py first.")

load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global model, vectorizer
    if not model or not vectorizer:
        # Try loading again just in case
        load_model()
        if not model or not vectorizer:
            return jsonify({'error': 'Model not loaded. Server configuration error.'}), 500

    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Preprocess and Predict
        processed_text = text.lower()
        vectorized_text = vectorizer.transform([processed_text])
        prediction = model.predict(vectorized_text)[0]
        proba = model.predict_proba(vectorized_text)[0]
        
        result = "Fake/Scam" if prediction == 1 else "Real"
        # prediction is 0 or 1. proba is [prob_0, prob_1].
        # if prediction is 1 (fake), we want proba[1]. If 0 (real), proba[0].
        confidence_value = proba[prediction]
        confidence = round(confidence_value * 100, 2)
        
        return jsonify({'result': result, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
