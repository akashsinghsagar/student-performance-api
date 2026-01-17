import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import warnings

warnings.filterwarnings('ignore')

# Load data
print("Loading data...")
df = pd.read_csv('student-mat.csv', sep=';')

print(f"Dataset shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")

# DATA CLEANING
print("\n=== DATA CLEANING ===")

# Check missing values
print(f"Missing values:\n{df.isnull().sum()}")

# Remove duplicates
initial_rows = len(df)
df = df.drop_duplicates()
print(f"Removed {initial_rows - len(df)} duplicate rows")

# Target variable
target = 'G3'
print(f"Target variable: {target}")
print(f"Target statistics:\n{df[target].describe()}")

# FEATURE ENGINEERING & SELECTION
print("\n=== FEATURE SELECTION ===")

# Separate features and target
X = df.drop('G3', axis=1)
y = df['G3']

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"Categorical features: {categorical_cols}")
print(f"Numerical features: {numerical_cols}")

# Encode categorical variables
label_encoders = {}
X_encoded = X.copy()

for col in categorical_cols:
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X[col])
    label_encoders[col] = le
    print(f"Encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# Feature selection - use correlation with target
correlation_with_target = X_encoded.corrwith(y).abs().sort_values(ascending=False)
print(f"\nTop 10 features by correlation with target:\n{correlation_with_target.head(10)}")

# Select top features (keep all for now, but you can adjust this)
X_selected = X_encoded

# TRAIN-TEST SPLIT
print("\n=== TRAIN-TEST SPLIT ===")
X_train, X_test, y_train, y_test = train_test_split(
    X_selected, y, test_size=0.2, random_state=42
)

print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# STANDARDIZATION
print("\n=== STANDARDIZATION ===")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# TRAIN REGRESSION MODEL
print("\n=== TRAINING REGRESSION MODEL ===")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled, y_train)
print("Model trained successfully!")

# EVALUATION
print("\n=== MODEL EVALUATION ===")
y_pred_train = model.predict(X_train_scaled)
y_pred_test = model.predict(X_test_scaled)

train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)
train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)

print(f"Training R²: {train_r2:.4f}")
print(f"Test R²: {test_r2:.4f}")
print(f"Training MAE: {train_mae:.4f}")
print(f"Test MAE: {test_mae:.4f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X_selected.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\nTop 10 most important features:\n{feature_importance.head(10)}")

# SAVE MODEL & ENCODERS
print("\n=== SAVING MODEL ===")
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(X_selected.columns.tolist(), f)

print("Model, scaler, and encoders saved successfully!")

# Save metadata for API
metadata = {
    'r2_score': test_r2,
    'mae': test_mae,
    'feature_names': X_selected.columns.tolist(),
    'categorical_features': categorical_cols,
    'numerical_features': numerical_cols
}

import json
with open('model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)

print("\nMetadata saved to model_metadata.json")
