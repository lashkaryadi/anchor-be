from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamOut, TeamListOut

router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.get("", response_model=TeamListOut)
def list_teams(db: Session = Depends(get_db)):
    rows = db.query(Team).order_by(Team.avg_risk.desc()).all()
    return TeamListOut(
        teams=[
            TeamOut(
                name=t.name,
                headcount=t.headcount,
                avgRisk=t.avg_risk,
                highRiskCount=t.high_risk_count,
                turnoverRate=t.turnover_rate,
                trend=t.trend,
            )
            for t in rows
        ]
    )
