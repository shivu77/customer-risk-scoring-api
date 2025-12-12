from datetime import datetime
from pydantic import BaseModel, validator

class CustomerCreate(BaseModel):
    name: str
    age: int
    income: float
    activity_score: int

    @validator("name")
    def name_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
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

class CustomerResponse(BaseModel):
    id: int
    name: str
    age: int
    income: float
    activity_score: int
    created_at: datetime

    class Config:
        orm_mode = True

