from datetime import datetime
from pydantic import BaseModel, validator

class RiskScoreCreate(BaseModel):
    customer_id: int
    income: float
    activity_score: int
    age: int

    @validator("customer_id")
    def customer_id_positive(cls, v):
        if v <= 0:
            raise ValueError("customer_id must be positive")
        return v

    @validator("age")
    def age_range(cls, v):
        if v < 18 or v > 80:
            raise ValueError("Age must be between 18 and 80")
        return v

    @validator("income")
    def income_non_negative(cls, v):
        if v < 0:
            raise ValueError("Income must be greater than or equal to 0")
        return v

    @validator("activity_score")
    def activity_score_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Activity score must be between 0 and 100")
        return v

    class Config:
        orm_mode = True

class RiskScoreResponse(BaseModel):
    id: int
    customer_id: int
    final_score: int
    explanation: str
    created_at: datetime

    class Config:
        orm_mode = True

