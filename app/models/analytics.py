from sqlalchemy import Column, String, Integer, Float
from app.database import Base


class RetentionTrend(Base):
    __tablename__ = "retention_trends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String, nullable=False)
    retained = Column(Float, nullable=False)
    target = Column(Float, nullable=False)
    at_risk = Column(Integer, nullable=False)


class TurnoverCost(Base):
    __tablename__ = "turnover_costs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String, nullable=False)
    actual = Column(Float, nullable=False)
    prevented = Column(Float, nullable=False)


class DepartmentRiskDistribution(Base):
    __tablename__ = "department_risk_distributions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String, nullable=False, unique=True)
    critical = Column(Integer, nullable=False, default=0)
    high = Column(Integer, nullable=False, default=0)
    medium = Column(Integer, nullable=False, default=0)
    low = Column(Integer, nullable=False, default=0)
