from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.career import CareerPath, InternalOpportunity
from app.schemas.career import CareerPathOut, CareerSkillOut, OpportunityOut

router = APIRouter(prefix="/api/careers", tags=["careers"])


@router.get("/paths", response_model=list[CareerPathOut])
def get_career_paths(db: Session = Depends(get_db)):
    rows = db.query(CareerPath).options(joinedload(CareerPath.skills)).all()
    return [
        CareerPathOut(
            employee=cp.employee_name,
            avatar=cp.avatar,
            current=cp.current_role,
            next=cp.next_role,
            readiness=cp.readiness,
            timeline=cp.timeline,
            skills=[CareerSkillOut(name=s.name, level=s.level) for s in cp.skills],
        )
        for cp in rows
    ]


@router.get("/opportunities", response_model=list[OpportunityOut])
def get_opportunities(db: Session = Depends(get_db)):
    rows = db.query(InternalOpportunity).all()
    return [
        OpportunityOut(
            title=o.title, department=o.department,
            openSince=o.open_since, matches=o.matches,
        )
        for o in rows
    ]
