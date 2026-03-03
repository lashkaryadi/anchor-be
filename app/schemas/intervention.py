from pydantic import BaseModel
from typing import Optional


class InterventionOut(BaseModel):
    id: str
    employeeName: str
    type: str
    status: str
    priority: str
    assignedTo: str
    createdAt: str
    dueDate: str
    effectiveness: Optional[float] = None

    class Config:
        from_attributes = True


class InterventionListOut(BaseModel):
    interventions: list[InterventionOut]
    total: int


class InterventionCreate(BaseModel):
    employeeName: str
    type: str
    priority: str
    assignedTo: str
    dueDate: str


class InterventionUpdate(BaseModel):
    status: Optional[str] = None
    effectiveness: Optional[float] = None
    assignedTo: Optional[str] = None
    dueDate: Optional[str] = None
