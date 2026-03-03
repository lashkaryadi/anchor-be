from sqlalchemy import Column, String, Integer, Float
from app.database import Base


class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(String, primary_key=True)
    employee_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending|in_progress|completed|expired
    priority = Column(String, nullable=False, default="medium")  # critical|high|medium|low
    assigned_to = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    due_date = Column(String, nullable=False)
    effectiveness = Column(Float, nullable=True)
