from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.intervention import Intervention
from app.schemas.intervention import InterventionOut, InterventionListOut, InterventionCreate, InterventionUpdate
from datetime import date
import uuid

router = APIRouter(prefix="/api/interventions", tags=["interventions"])


def _serialize(i: Intervention) -> InterventionOut:
    return InterventionOut(
        id=i.id,
        employeeName=i.employee_name,
        type=i.type,
        status=i.status,
        priority=i.priority,
        assignedTo=i.assigned_to,
        createdAt=i.created_at,
        dueDate=i.due_date,
        effectiveness=i.effectiveness,
    )


@router.get("", response_model=InterventionListOut)
def list_interventions(
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Intervention)
    if status:
        q = q.filter(Intervention.status == status)
    rows = q.order_by(Intervention.created_at.desc()).all()
    return InterventionListOut(
        interventions=[_serialize(r) for r in rows],
        total=len(rows),
    )


@router.post("", response_model=InterventionOut, status_code=201)
def create_intervention(body: InterventionCreate, db: Session = Depends(get_db)):
    intervention = Intervention(
        id=str(uuid.uuid4())[:8],
        employee_name=body.employeeName,
        type=body.type,
        status="pending",
        priority=body.priority,
        assigned_to=body.assignedTo,
        created_at=date.today().isoformat(),
        due_date=body.dueDate,
    )
    db.add(intervention)
    db.commit()
    db.refresh(intervention)
    return _serialize(intervention)


@router.patch("/{intervention_id}", response_model=InterventionOut)
def update_intervention(
    intervention_id: str, body: InterventionUpdate, db: Session = Depends(get_db)
):
    item = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Intervention not found")
    if body.status is not None:
        item.status = body.status
    if body.effectiveness is not None:
        item.effectiveness = body.effectiveness
    if body.assignedTo is not None:
        item.assigned_to = body.assignedTo
    if body.dueDate is not None:
        item.due_date = body.dueDate
    db.commit()
    db.refresh(item)
    return _serialize(item)
