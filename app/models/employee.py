from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    department = Column(String, nullable=False, index=True)
    avatar = Column(String, nullable=False)
    risk_score = Column(Float, nullable=False, default=0)
    risk_level = Column(String, nullable=False, default="low")  # critical|high|medium|low
    confidence = Column(Float, nullable=False, default=0)
    tenure = Column(String, nullable=False)
    last_engagement = Column(String, nullable=False)
    salary = Column(Float, nullable=False, default=0)
    market_rate = Column(Float, nullable=False, default=0)
    manager_score = Column(Float, nullable=False, default=0)
    last_promotion = Column(String, nullable=False)
    recent_changes = Column(JSON, nullable=False, default=list)

    factors = relationship("RiskFactor", back_populates="employee", cascade="all, delete-orphan")
    engagement_scores = relationship("EngagementScore", back_populates="employee", cascade="all, delete-orphan", order_by="EngagementScore.period")


class RiskFactor(Base):
    __tablename__ = "risk_factors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    label = Column(String, nullable=False)
    impact = Column(Float, nullable=False)
    direction = Column(String, nullable=False)  # up|down

    employee = relationship("Employee", back_populates="factors")


class EngagementScore(Base):
    __tablename__ = "engagement_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    period = Column(Integer, nullable=False)  # sequential ordering (0, 1, 2...)
    score = Column(Float, nullable=False)

    employee = relationship("Employee", back_populates="engagement_scores")
