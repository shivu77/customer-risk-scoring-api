from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.config.database import get_db
from app.config.models_base import Customer, RiskScore
from app.core.scoring_engine import RiskScoringEngine
from app.schemas.risk_schema import RiskScoreCreate, RiskScoreResponse

router = APIRouter()

@router.post("/score", response_model=RiskScoreResponse)
def score(payload: RiskScoreCreate, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.id == payload.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        result = RiskScoringEngine().calculate_with_explanation(payload)
        risk = RiskScore(
            customer_id=payload.customer_id,
            final_score=result["final_score"],
            explanation=result["explanation"],
        )
        db.add(risk)
        db.commit()
        db.refresh(risk)
        return risk
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{customer_id}", response_model=List[RiskScoreResponse])
def list_scores(customer_id: int, db: Session = Depends(get_db)):
    try:
        scores = db.query(RiskScore).filter(RiskScore.customer_id == customer_id).all()
        return scores
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")

