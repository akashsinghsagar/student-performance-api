from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json
import numpy as np
import pandas as pd
import os
from typing import List, Dict

# Initialize FastAPI app
app = FastAPI(title="Student Grade Prediction API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Define the input data model
class StudentInput(BaseModel):
    school: str
    sex: str
    age: int
    address: str
    famsize: str
    Pstatus: str
    Medu: int
    Fedu: int
    Mjob: str
    Fjob: str
    reason: str
    guardian: str
    traveltime: int
    studytime: int
    failures: int
    schoolsup: str
    famsup: str
    paid: str
    activities: str
    nursery: str
    higher: str
    internet: str
    romantic: str
    famrel: int
    freetime: int
    goout: int
    Dalc: int
    Walc: int
    health: int
    absences: int
    G1: int
    G2: int

class BatchStudentInput(BaseModel):
    students: List[StudentInput]

class PredictionResponse(BaseModel):
    predicted_grade: float

class BatchPredictionResponse(BaseModel):
    predictions: List[float]

# Helper function to preprocess input data
def preprocess_student_data(data: StudentInput) -> pd.DataFrame:
    """Convert student input to preprocessed DataFrame ready for model prediction"""
    # Create dictionary from input data
    student_dict = data.model_dump()
    
    # Create DataFrame
    df = pd.DataFrame([student_dict])
    
    # Encode categorical variables
    categorical_columns = ['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 
                          'Fjob', 'reason', 'guardian', 'schoolsup', 'famsup', 'paid',
                          'activities', 'nursery', 'higher', 'internet', 'romantic']
    
    for col in categorical_columns:
        if col in label_encoders and col in df.columns:
            df[col] = label_encoders[col].transform(df[col])
    
    # Ensure all feature columns are present in correct order
    df = df[feature_columns]
    
    # Scale features
    df_scaled = scaler.transform(df)
    
    return df_scaled

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Student Grade Prediction API",
        "version": "2.0",
        "framework": "FastAPI",
        "endpoints": {
            "/predict": "POST - Predict student grade",
            "/predict-batch": "POST - Batch predictions",
            "/metadata": "GET - Model metadata",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": True}

@app.get("/metadata")
def get_metadata():
    """Get model metadata and performance metrics"""
    return metadata

@app.post("/predict", response_model=PredictionResponse)
def predict(data: StudentInput):
    """
    Predict student final grade (G3) based on various features
    
    Returns predicted grade on a scale of 0-20
    """
    try:
        # Preprocess the input data
        processed_data = preprocess_student_data(data)
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        
        # Ensure prediction is within valid range (0-20)
        prediction = max(0, min(20, prediction))
        
        return {"predicted_grade": float(prediction)}
    
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}

@app.post("/predict-batch", response_model=BatchPredictionResponse)
def predict_batch(data: BatchStudentInput):
    """
    Batch prediction endpoint for multiple students
    """
    try:
        predictions = []
        
        for student in data.students:
            processed_data = preprocess_student_data(student)
            prediction = model.predict(processed_data)[0]
            prediction = max(0, min(20, prediction))
            predictions.append(float(prediction))
        
        return {"predictions": predictions}
    
    except Exception as e:
        return {"error": f"Batch prediction error: {str(e)}"}

if __name__ == '__main__':
    import uvicorn
    print('=' * 50)
    print('Starting FastAPI Server on http://localhost:5000')
    print('Backend API ready for React frontend')
    print('Interactive docs: http://localhost:5000/docs')
    print('=' * 50)
    uvicorn.run(app, host="localhost", port=5000)
