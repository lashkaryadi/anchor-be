from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.intervention import Intervention
from app.models.analytics import RetentionTrend, TurnoverCost, DepartmentRiskDistribution
from app.models.team import Team
from app.schemas.analytics import (
    DashboardSummary, RetentionTrendOut, TurnoverCostOut, DepartmentRiskOut
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    total = db.query(Employee).count()
    at_risk = db.query(Employee).filter(
        Employee.risk_level.in_(["critical", "high"])
    ).count()

    costs = db.query(TurnoverCost).all()
    total_prevented = sum(c.prevented for c in costs)

    total_interventions = db.query(Intervention).count()
    completed = db.query(Intervention).filter(
        Intervention.status == "completed"
    ).count()
    rate = int((completed / total_interventions * 100)) if total_interventions > 0 else 0

    return DashboardSummary(
        totalEmployees=total,
        atRiskCount=at_risk,
        costPrevented=f"${int(total_prevented / 1000)}K",
        interventionRate=f"{rate}%",
        retentionHealthScore=74,
        retentionHealthChange=2.3,
    )


@router.get("/retention-trend", response_model=list[RetentionTrendOut])
def get_retention_trend(db: Session = Depends(get_db)):
    rows = db.query(RetentionTrend).order_by(RetentionTrend.id).all()
    return [
        RetentionTrendOut(
            month=r.month, retained=r.retained, target=r.target, atRisk=r.at_risk
        )
        for r in rows
    ]


@router.get("/turnover-costs", response_model=list[TurnoverCostOut])
def get_turnover_costs(db: Session = Depends(get_db)):
    rows = db.query(TurnoverCost).order_by(TurnoverCost.id).all()
    return [TurnoverCostOut(month=r.month, actual=r.actual, prevented=r.prevented) for r in rows]


@router.get("/risk-distribution", response_model=list[DepartmentRiskOut])
def get_risk_distribution(db: Session = Depends(get_db)):
    rows = db.query(DepartmentRiskDistribution).all()
    return [
        DepartmentRiskOut(
            department=r.department, critical=r.critical, high=r.high,
            medium=r.medium, low=r.low
        )
        for r in rows
    ]
