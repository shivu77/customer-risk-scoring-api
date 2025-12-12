from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.config.database import get_db
from app.config.models_base import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerResponse

router = APIRouter()

@router.post("/add", response_model=CustomerResponse)
def add_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    try:
        customer = Customer(
            name=payload.name,
            age=payload.age,
            income=payload.income,
            activity_score=payload.activity_score,
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{id}", response_model=CustomerResponse)
def get_customer(id: int, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.id == id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")

