# Backend (FastAPI) container
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/student

# Install OS packages if needed (uncomment if pandas/scikit need build deps)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY student/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and model artifacts from student backend
COPY student/main.py ./main.py
COPY student/routers.py ./routers.py
COPY student/schemas.py ./schemas.py
COPY student/services.py ./services.py
COPY student/feature_columns.pkl student/label_encoders.pkl student/model.pkl student/model_metadata.json student/scaler.pkl ./

# Expose API port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
