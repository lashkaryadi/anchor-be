from pydantic import BaseModel


class RetentionTrendOut(BaseModel):
    month: str
    retained: float
    target: float
    atRisk: int

    class Config:
        from_attributes = True


class TurnoverCostOut(BaseModel):
    month: str
    actual: float
    prevented: float

    class Config:
        from_attributes = True


class DepartmentRiskOut(BaseModel):
    department: str
    critical: int
    high: int
    medium: int
    low: int

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    totalEmployees: int
    atRiskCount: int
    costPrevented: str
    interventionRate: str
    retentionHealthScore: int
    retentionHealthChange: float


class TurnoverReasonOut(BaseModel):
    name: str
    value: int
    color: str


class RadarDataOut(BaseModel):
    factor: str
    current: float
    benchmark: float


class PredictionOut(BaseModel):
    segment: str
    probability: float
    count: int
    trend: str
