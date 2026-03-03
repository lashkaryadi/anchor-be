from pydantic import BaseModel


class TeamOut(BaseModel):
    name: str
    headcount: int
    avgRisk: float
    highRiskCount: int
    turnoverRate: float
    trend: str

    class Config:
        from_attributes = True


class TeamListOut(BaseModel):
    teams: list[TeamOut]
