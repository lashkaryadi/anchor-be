from sqlalchemy import Column, String, Integer, Float
from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    headcount = Column(Integer, nullable=False)
    avg_risk = Column(Float, nullable=False)
    high_risk_count = Column(Integer, nullable=False)
    turnover_rate = Column(Float, nullable=False)
    trend = Column(String, nullable=False)  # up|down|stable
