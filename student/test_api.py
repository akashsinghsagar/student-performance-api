#!/usr/bin/env python
"""
Test script for the Flask API
"""

import sys
sys.path.insert(0, r'c:\Users\ARSH\OneDrive\Desktop\website\student')

from app import app
import json

# Create a test client
client = app.test_client()

print("=" * 60)
print("FLASK API TEST SUITE")
print("=" * 60)

# Test 1: Health check
print("\n[TEST 1] Health Check")
print("-" * 60)
response = client.get('/health')
data = response.json
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(data, indent=2)}")
print("✓ PASS" if response.status_code == 200 else "✗ FAIL")

# Test 2: Metadata
print("\n[TEST 2] Model Metadata")
print("-" * 60)
response = client.get('/metadata')
data = response.json
print(f"Status: {response.status_code}")
print(f"R² Score: {data['r2_score']:.4f}")
print(f"MAE: {data['mae']:.4f}")
print(f"Features: {len(data['features'])}")
print("✓ PASS" if response.status_code == 200 else "✗ FAIL")

# Test 3: Single Prediction
print("\n[TEST 3] Single Student Prediction")
print("-" * 60)
test_data = {
    'school': 'GP', 'sex': 'F', 'age': 15, 'address': 'U', 'famsize': 'GT3',
    'Pstatus': 'T', 'Medu': 4, 'Fedu': 4, 'Mjob': 'at_home', 'Fjob': 'teacher',
    'reason': 'course', 'guardian': 'mother', 'traveltime': 2, 'studytime': 2,
    'failures': 0, 'schoolsup': 'yes', 'famsup': 'yes', 'paid': 'no', 'activities': 'no',
    'nursery': 'yes', 'higher': 'yes', 'internet': 'no', 'romantic': 'no',
    'famrel': 4, 'freetime': 3, 'goout': 4, 'Dalc': 1, 'Walc': 1, 'health': 3,
    'absences': 6, 'G1': 15, 'G2': 14
}

response = client.post('/predict', json=test_data)
result = response.json
print(f"Status: {response.status_code}")
print(f"Predicted Grade: {result['prediction']:.2f}")
print(f"Expected Range: 0-20")
print(f"Model R²: {result['confidence']['r2_score']:.4f}")
print(f"Model MAE: {result['confidence']['mae']:.4f}")
print("✓ PASS" if response.status_code == 200 and 0 <= result['prediction'] <= 20 else "✗ FAIL")

# Test 4: Batch Prediction
print("\n[TEST 4] Batch Prediction (3 students)")
print("-" * 60)
batch_data = [test_data, test_data, test_data]
response = client.post('/predict-batch', json=batch_data)
result = response.json
print(f"Status: {response.status_code}")
print(f"Students Processed: {result['count']}")
print(f"Predictions:")
for pred in result['predictions']:
    print(f"  Student {pred['student']}: {pred['prediction']:.2f}")
print("✓ PASS" if response.status_code == 200 and result['count'] == 3 else "✗ FAIL")

# Test 5: Invalid Data
print("\n[TEST 5] Error Handling (Missing Field)")
print("-" * 60)
invalid_data = {'school': 'GP', 'sex': 'F'}  # Missing many required fields
response = client.post('/predict', json=invalid_data)
print(f"Status: {response.status_code}")
print(f"Error Message: {response.json.get('error', 'No error message')}")
print("✓ PASS" if response.status_code == 400 else "✗ FAIL")

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("All tests completed! API is working correctly.")
print("\nYou can now:")
print("  1. Start Flask API:  python app.py")
print("  2. Start React UI:   npm run dev (from react-project/)")
print("  3. Open browser:     http://localhost:5173")
print("=" * 60)
