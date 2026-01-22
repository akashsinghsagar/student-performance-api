"""
Business logic for predictions
"""
import pickle
import json
import numpy as np
import pandas as pd
import os
from typing import List, Dict, Any


class PredictionService:
    """Service for handling prediction logic"""
    
    def __init__(self):
        """Load model and preprocessing objects"""
        model_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load model
        with open(os.path.join(model_dir, 'model.pkl'), 'rb') as f:
            self.model = pickle.load(f)
        
        # Load preprocessing objects
        with open(os.path.join(model_dir, 'scaler.pkl'), 'rb') as f:
            self.scaler = pickle.load(f)
        
        with open(os.path.join(model_dir, 'label_encoders.pkl'), 'rb') as f:
            self.label_encoders = pickle.load(f)
        
        with open(os.path.join(model_dir, 'feature_columns.pkl'), 'rb') as f:
            self.feature_columns = pickle.load(f)
        
        # Load metadata
        with open(os.path.join(model_dir, 'model_metadata.json'), 'r') as f:
            self.metadata = json.load(f)
    
    def preprocess_input(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Preprocess input data for prediction
        
        Args:
            data: Input features dictionary
            
        Returns:
            Preprocessed numpy array
            
        Raises:
            ValueError: If preprocessing fails
        """
        # Create DataFrame
        input_df = pd.DataFrame([data])
        
        # Ensure all required columns are present
        missing_cols = set(self.feature_columns) - set(input_df.columns)
        if missing_cols:
            raise ValueError(f'Missing required features: {missing_cols}')
        
        # Reorder columns to match training data
        input_df = input_df[self.feature_columns]
        
        # Encode categorical variables
        for col in self.metadata['categorical_features']:
            if col in input_df.columns and col in self.label_encoders:
                try:
                    input_df[col] = self.label_encoders[col].transform(input_df[col])
                except ValueError as e:
                    raise ValueError(f'Invalid value for {col}: {str(e)}')
        
        # Scale features
        input_scaled = self.scaler.transform(input_df)
        
        return input_scaled
    
    def predict_single(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction for single student
        
        Args:
            data: Student features
            
        Returns:
            Prediction result with confidence metrics
        """
        # Preprocess input
        input_scaled = self.preprocess_input(data)
        
        # Make prediction
        prediction = self.model.predict(input_scaled)[0]
        
        # Ensure prediction is within valid range (0-20)
        prediction = max(0, min(20, prediction))
        
        return {
            'prediction': round(float(prediction), 2),
            'confidence': {
                'r2_score': self.metadata['r2_score'],
                'mae': self.metadata['mae']
            },
            'input_features': data
        }
    
    def predict_batch(self, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Make predictions for multiple students
        
        Args:
            data_list: List of student features
            
        Returns:
            Batch prediction results
        """
        if not data_list:
            raise ValueError('Data list cannot be empty')
        
        # Create DataFrame
        input_df = pd.DataFrame(data_list)
        
        # Ensure all required columns are present
        missing_cols = set(self.feature_columns) - set(input_df.columns)
        if missing_cols:
            raise ValueError(f'Missing required features: {missing_cols}')
        
        # Reorder columns
        input_df = input_df[self.feature_columns]
        
        # Encode categorical variables
        for col in self.metadata['categorical_features']:
            if col in input_df.columns and col in self.label_encoders:
                try:
                    input_df[col] = self.label_encoders[col].transform(input_df[col])
                except ValueError as e:
                    raise ValueError(f'Invalid value for {col}: {str(e)}')
        
        # Scale features
        input_scaled = self.scaler.transform(input_df)
        
        # Make predictions
        predictions = self.model.predict(input_scaled)
        predictions = np.clip(predictions, 0, 20)
        
        # Format results
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                'student': i + 1,
                'prediction': round(float(pred), 2),
                'input': data_list[i]
            })
        
        return {
            'predictions': results,
            'count': len(results),
            'confidence': {
                'r2_score': self.metadata['r2_score'],
                'mae': self.metadata['mae']
            }
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get model metadata"""
        return {
            'r2_score': self.metadata['r2_score'],
            'mae': self.metadata['mae'],
            'features': self.metadata['feature_names'],
            'categorical_features': self.metadata['categorical_features'],
            'numerical_features': self.metadata['numerical_features']
        }
    
    def is_healthy(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None


# Singleton instance
prediction_service = PredictionService()
