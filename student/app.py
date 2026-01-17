from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import json
import numpy as np
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load trained model and preprocessing objects
model_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(model_dir, 'model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(model_dir, 'scaler.pkl'), 'rb') as f:
    scaler = pickle.load(f)

with open(os.path.join(model_dir, 'label_encoders.pkl'), 'rb') as f:
    label_encoders = pickle.load(f)

with open(os.path.join(model_dir, 'feature_columns.pkl'), 'rb') as f:
    feature_columns = pickle.load(f)

with open(os.path.join(model_dir, 'model_metadata.json'), 'r') as f:
    metadata = json.load(f)

@app.route('/')
def home():
    """Home route"""
    return jsonify({
        'message': 'Student Grade Prediction API',
        'version': '1.0',
        'endpoints': {
            'predict': '/predict (POST)',
            'metadata': '/metadata (GET)',
            'health': '/health (GET)'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'r2_score': metadata['r2_score'],
        'mae': metadata['mae']
    })

@app.route('/metadata', methods=['GET'])
def get_metadata():
    """Get model metadata"""
    return jsonify({
        'r2_score': metadata['r2_score'],
        'mae': metadata['mae'],
        'features': metadata['feature_names'],
        'categorical_features': metadata['categorical_features'],
        'numerical_features': metadata['numerical_features']
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict student grade"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DataFrame with input data
        input_df = pd.DataFrame([data])
        
        # Ensure all required columns are present
        for col in feature_columns:
            if col not in input_df.columns:
                return jsonify({'error': f'Missing required feature: {col}'}), 400
        
        # Reorder columns to match training data
        input_df = input_df[feature_columns]
        
        # Encode categorical variables
        for col in metadata['categorical_features']:
            if col in input_df.columns and col in label_encoders:
                try:
                    input_df[col] = label_encoders[col].transform(input_df[col])
                except ValueError as e:
                    return jsonify({'error': f'Invalid value for {col}: {str(e)}'}), 400
        
        # Scale features
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        
        # Ensure prediction is within valid range (0-20)
        prediction = max(0, min(20, prediction))
        
        return jsonify({
            'prediction': round(float(prediction), 2),
            'confidence': {
                'r2_score': metadata['r2_score'],
                'mae': metadata['mae']
            },
            'input_features': data
        })
    
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    """Predict multiple students"""
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({'error': 'Expected list of student data'}), 400
        
        if len(data) == 0:
            return jsonify({'error': 'Empty data list'}), 400
        
        # Create DataFrame with input data
        input_df = pd.DataFrame(data)
        
        # Ensure all required columns are present
        for col in feature_columns:
            if col not in input_df.columns:
                return jsonify({'error': f'Missing required feature: {col}'}), 400
        
        # Reorder columns
        input_df = input_df[feature_columns]
        
        # Encode categorical variables
        for col in metadata['categorical_features']:
            if col in input_df.columns and col in label_encoders:
                try:
                    input_df[col] = label_encoders[col].transform(input_df[col])
                except ValueError as e:
                    return jsonify({'error': f'Invalid value for {col}: {str(e)}'}), 400
        
        # Scale features
        input_scaled = scaler.transform(input_df)
        
        # Make predictions
        predictions = model.predict(input_scaled)
        predictions = np.clip(predictions, 0, 20)
        
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                'student': i + 1,
                'prediction': round(float(pred), 2),
                'input': data[i]
            })
        
        return jsonify({
            'predictions': results,
            'count': len(results),
            'confidence': {
                'r2_score': metadata['r2_score'],
                'mae': metadata['mae']
            }
        })
    
    except Exception as e:
        return jsonify({'error': f'Batch prediction error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
