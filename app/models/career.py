from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CareerPath(Base):
    __tablename__ = "career_paths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String, nullable=False)
    avatar = Column(String, nullable=False)
    current_role = Column(String, nullable=False)
    next_role = Column(String, nullable=False)
    readiness = Column(Float, nullable=False)
    timeline = Column(String, nullable=False)

    skills = relationship("CareerSkill", back_populates="career_path", cascade="all, delete-orphan")


class CareerSkill(Base):
    __tablename__ = "career_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    level = Column(Float, nullable=False)

    career_path = relationship("CareerPath", back_populates="skills")


class InternalOpportunity(Base):
    __tablename__ = "internal_opportunities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    open_since = Column(String, nullable=False)
    matches = Column(Integer, nullable=False)
