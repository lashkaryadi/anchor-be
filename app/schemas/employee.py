from pydantic import BaseModel


class RiskFactorOut(BaseModel):
    label: str
    impact: float
    direction: str

    class Config:
        from_attributes = True


class EmployeeOut(BaseModel):
    id: str
    name: str
    role: str
    department: str
    avatar: str
    riskScore: float
    riskLevel: str
    confidence: float
    tenure: str
    lastEngagement: str
    factors: list[RiskFactorOut]
    engagementTrend: list[float]
    salary: float
    marketRate: float
    managerScore: float
    lastPromotion: str
    recentChanges: list[str]

    class Config:
        from_attributes = True


class EmployeeListOut(BaseModel):
    employees: list[EmployeeOut]
    total: int
