from pydantic import BaseModel


class CareerSkillOut(BaseModel):
    name: str
    level: float

    class Config:
        from_attributes = True


class CareerPathOut(BaseModel):
    employee: str
    avatar: str
    current: str
    next: str
    readiness: float
    skills: list[CareerSkillOut]
    timeline: str

    class Config:
        from_attributes = True


class OpportunityOut(BaseModel):
    title: str
    department: str
    openSince: str
    matches: int

    class Config:
        from_attributes = True
