from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.decision import Decision
from app.models.pilot import Pilot
from app.models.kpi import KPI
from app.models.evidence import Evidence
from app.models.application import Application
from app.models.startup import Startup
from app.models.user import User
from app.schemas.decision import DecisionCreate, DecisionResponse, DecisionSupportResponse
from app.auth import get_current_user, require_role
from app.services.decision_support import compute_decision_support

router = APIRouter(tags=["Decisions"])

@router.get("/pilots/{pilot_id}/decision-support", response_model=DecisionSupportResponse)
def get_pilot_decision_support(
    pilot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dynamically compute decision support recommendation.
    Not stored in database; computed from current approved evidence.
    Available to Officer, and Startup (for its own pilot).
    """
    pilot = db.query(Pilot).join(Application).filter(Pilot.id == pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pilot not found")

    if current_user.role == "startup":
        startup = db.query(Startup).filter(Startup.user_id == current_user.id).first()
        if not startup or pilot.application.startup_id != startup.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Startups may only view decision support for their own pilots."
            )
    elif current_user.role not in ("officer", "evaluator"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Fetch total KPIs
    kpis = db.query(KPI).filter(KPI.pilot_id == pilot_id).all()
    total_kpis = len(kpis)

    # Count KPIs that have at least one approved evidence
    kpi_ids = [k.id for k in kpis]
    if total_kpis > 0:
        approved_kpi_ids = db.query(Evidence.kpi_id).filter(
            Evidence.pilot_id == pilot_id,
            Evidence.kpi_id.in_(kpi_ids),
            Evidence.status == "approved"
        ).distinct().all()
        approved_kpis = len(approved_kpi_ids)
    else:
        approved_kpis = 0

    res = compute_decision_support(
        pilot_id=pilot_id,
        total_kpis=total_kpis,
        approved_kpis=approved_kpis
    )

    return DecisionSupportResponse(
        pilot_id=res.pilot_id,
        total_kpis=res.total_kpis,
        approved_kpis=res.approved_kpis,
        achievement_ratio=res.achievement_ratio,
        recommendation=res.recommendation,
        explanation=res.explanation
    )

@router.post("/pilots/{pilot_id}/decision", response_model=DecisionResponse, status_code=status.HTTP_201_CREATED)
def record_final_decision(
    pilot_id: int,
    decision_in: DecisionCreate,
    current_user: User = Depends(require_role("officer")),
    db: Session = Depends(get_db)
):
    """Officer only: record final formal decision for a pilot in the Decision table."""
    pilot = db.query(Pilot).filter(Pilot.id == pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pilot not found")

    existing = db.query(Decision).filter(Decision.pilot_id == pilot_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A final decision has already been recorded for this pilot."
        )

    decision = Decision(
        pilot_id=pilot_id,
        recommendation=decision_in.recommendation,
        notes=decision_in.notes
    )
    db.add(decision)

    # Update pilot status to completed or the recorded outcome
    if decision_in.recommendation.lower() in ("recommend scale", "scale"):
        pilot.status = "completed"
    elif "extend" in decision_in.recommendation.lower():
        pilot.status = "extended"
    elif "discontinue" in decision_in.recommendation.lower():
        pilot.status = "discontinued"
    else:
        pilot.status = "completed"

    db.commit()
    db.refresh(decision)
    return decision
