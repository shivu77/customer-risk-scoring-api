from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    income = Column(Float, nullable=False)
    activity_score = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    risk_scores = relationship("RiskScore", backref="customer", cascade="all, delete-orphan")

class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    final_score = Column(Integer, nullable=False)
    explanation = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

