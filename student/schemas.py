"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional


class StudentInput(BaseModel):
    """Single student prediction input"""
    school: str = Field(..., description="Student's school (GP or MS)")
    sex: str = Field(..., description="Student's gender (M or F)")
    age: int = Field(..., ge=15, le=22, description="Student's age (15-22)")
    address: str = Field(..., description="Home address type (U=Urban, R=Rural)")
    famsize: str = Field(..., description="Family size (LE3=<=3, GT3=>3)")
    Pstatus: str = Field(..., description="Parent cohabitation status (T=Together, A=Apart)")
    Medu: int = Field(..., ge=0, le=4, description="Mother's education (0-4)")
    Fedu: int = Field(..., ge=0, le=4, description="Father's education (0-4)")
    Mjob: str = Field(..., description="Mother's job")
    Fjob: str = Field(..., description="Father's job")
    reason: str = Field(..., description="Reason to choose school")
    guardian: str = Field(..., description="Student's guardian")
    traveltime: int = Field(..., ge=1, le=4, description="Travel time (1-4)")
    studytime: int = Field(..., ge=1, le=4, description="Weekly study time (1-4)")
    failures: int = Field(..., ge=0, le=4, description="Past class failures (0-4)")
    schoolsup: str = Field(..., description="Extra educational support (yes/no)")
    famsup: str = Field(..., description="Family educational support (yes/no)")
    paid: str = Field(..., description="Extra paid classes (yes/no)")
    activities: str = Field(..., description="Extra-curricular activities (yes/no)")
    nursery: str = Field(..., description="Attended nursery school (yes/no)")
    higher: str = Field(..., description="Wants higher education (yes/no)")
    internet: str = Field(..., description="Internet access at home (yes/no)")
    romantic: str = Field(..., description="In romantic relationship (yes/no)")
    famrel: int = Field(..., ge=1, le=5, description="Family relationship quality (1-5)")
    freetime: int = Field(..., ge=1, le=5, description="Free time after school (1-5)")
    goout: int = Field(..., ge=1, le=5, description="Going out with friends (1-5)")
    Dalc: int = Field(..., ge=1, le=5, description="Workday alcohol consumption (1-5)")
    Walc: int = Field(..., ge=1, le=5, description="Weekend alcohol consumption (1-5)")
    health: int = Field(..., ge=1, le=5, description="Current health status (1-5)")
    absences: int = Field(..., ge=0, description="Number of school absences")
    G1: int = Field(..., ge=0, le=20, description="First period grade (0-20)")
    G2: int = Field(..., ge=0, le=20, description="Second period grade (0-20)")

    @validator('school')
    def validate_school(cls, v):
        if v not in ['GP', 'MS']:
            raise ValueError('school must be GP or MS')
        return v

    @validator('sex')
    def validate_sex(cls, v):
        if v not in ['M', 'F']:
            raise ValueError('sex must be M or F')
        return v

    @validator('address')
    def validate_address(cls, v):
        if v not in ['U', 'R']:
            raise ValueError('address must be U (Urban) or R (Rural)')
        return v

    @validator('schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic')
    def validate_yes_no(cls, v):
        if v not in ['yes', 'no']:
            raise ValueError(f'{v} must be yes or no')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "school": "GP",
                "sex": "F",
                "age": 18,
                "address": "U",
                "famsize": "GT3",
                "Pstatus": "A",
                "Medu": 4,
                "Fedu": 4,
                "Mjob": "at_home",
                "Fjob": "teacher",
                "reason": "course",
                "guardian": "mother",
                "traveltime": 2,
                "studytime": 2,
                "failures": 0,
                "schoolsup": "yes",
                "famsup": "no",
                "paid": "no",
                "activities": "no",
                "nursery": "yes",
                "higher": "yes",
                "internet": "no",
                "romantic": "no",
                "famrel": 4,
                "freetime": 3,
                "goout": 4,
                "Dalc": 1,
                "Walc": 1,
                "health": 3,
                "absences": 6,
                "G1": 10,
                "G2": 11
            }
        }


class PredictionResponse(BaseModel):
    """Single prediction response"""
    prediction: float = Field(..., description="Predicted final grade (0-20)")
    confidence: dict = Field(..., description="Model confidence metrics")
    input_features: dict = Field(..., description="Input features used for prediction")


class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    students: List[StudentInput]


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    predictions: List[dict]
    count: int
    confidence: dict


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    r2_score: float
    mae: float


class MetadataResponse(BaseModel):
    """Model metadata response"""
    r2_score: float
    mae: float
    features: List[str]
    categorical_features: List[str]
    numerical_features: List[str]


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_type: Optional[str] = None
