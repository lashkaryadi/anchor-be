from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.employee import Employee, EngagementScore
from app.schemas.employee import EmployeeOut, EmployeeListOut, RiskFactorOut

router = APIRouter(prefix="/api/employees", tags=["employees"])


def _serialize_employee(emp: Employee) -> EmployeeOut:
    trend = sorted(emp.engagement_scores, key=lambda s: s.period)
    return EmployeeOut(
        id=emp.id,
        name=emp.name,
        role=emp.role,
        department=emp.department,
        avatar=emp.avatar,
        riskScore=emp.risk_score,
        riskLevel=emp.risk_level,
        confidence=emp.confidence,
        tenure=emp.tenure,
        lastEngagement=emp.last_engagement,
        factors=[RiskFactorOut(label=f.label, impact=f.impact, direction=f.direction) for f in emp.factors],
        engagementTrend=[s.score for s in trend],
        salary=emp.salary,
        marketRate=emp.market_rate,
        managerScore=emp.manager_score,
        lastPromotion=emp.last_promotion,
        recentChanges=emp.recent_changes or [],
    )


@router.get("", response_model=EmployeeListOut)
def list_employees(
    department: str | None = Query(None),
    risk_level: str | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Employee).options(
        joinedload(Employee.factors),
        joinedload(Employee.engagement_scores),
    )
    if department:
        q = q.filter(Employee.department == department)
    if risk_level:
        q = q.filter(Employee.risk_level == risk_level)
    if search:
        q = q.filter(Employee.name.ilike(f"%{search}%"))

    employees = q.order_by(Employee.risk_score.desc()).all()
    # Deduplicate due to joinedload producing duplicates
    seen = set()
    unique = []
    for e in employees:
        if e.id not in seen:
            seen.add(e.id)
            unique.append(e)

    return EmployeeListOut(
        employees=[_serialize_employee(e) for e in unique],
        total=len(unique),
    )


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    emp = (
        db.query(Employee)
        .options(
            joinedload(Employee.factors),
            joinedload(Employee.engagement_scores),
        )
        .filter(Employee.id == employee_id)
        .first()
    )
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return _serialize_employee(emp)
