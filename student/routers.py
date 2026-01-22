"""
API routes for prediction endpoints
"""
from fastapi import APIRouter, HTTPException, status
from schemas import (
    StudentInput,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    HealthResponse,
    MetadataResponse
)
from services import prediction_service


router = APIRouter()


@router.get("/", tags=["General"])
async def root():
    """API information endpoint"""
    return {
        'message': 'Student Grade Prediction API',
        'version': '2.0',
        'status': 'running',
        'documentation': '/docs',
        'endpoints': {
            'predict': '/api/predict (POST)',
            'batch_predict': '/api/predict-batch (POST)',
            'metadata': '/api/metadata (GET)',
            'health': '/api/health (GET)'
        }
    }


@router.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """
    Health check endpoint
    
    Returns model status and performance metrics
    """
    try:
        metadata = prediction_service.get_metadata()
        return {
            'status': 'healthy',
            'model_loaded': prediction_service.is_healthy(),
            'r2_score': metadata['r2_score'],
            'mae': metadata['mae']
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )


@router.get("/metadata", response_model=MetadataResponse, tags=["General"])
async def get_model_metadata():
    """
    Get model metadata
    
    Returns information about the model including:
    - Performance metrics (R2 score, MAE)
    - Feature names and types
    """
    try:
        return prediction_service.get_metadata()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve metadata: {str(e)}"
        )


@router.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_grade(student: StudentInput):
    """
    Predict student's final grade
    
    Takes student features and returns predicted grade (0-20 scale)
    along with model confidence metrics.
    
    Args:
        student: Student features including demographics, family background,
                school performance indicators, and lifestyle factors
    
    Returns:
        Predicted grade with confidence metrics
    """
    try:
        # Convert Pydantic model to dict
        student_data = student.dict()
        
        # Make prediction
        result = prediction_service.predict_single(student_data)
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/predict-batch", response_model=BatchPredictionResponse, tags=["Predictions"])
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict grades for multiple students
    
    Takes a list of students and returns predictions for all of them.
    Useful for batch processing and data analysis.
    
    Args:
        request: Object containing list of students
    
    Returns:
        List of predictions with confidence metrics
    """
    try:
        # Convert Pydantic models to dicts
        students_data = [student.dict() for student in request.students]
        
        # Make batch prediction
        result = prediction_service.predict_batch(students_data)
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )
