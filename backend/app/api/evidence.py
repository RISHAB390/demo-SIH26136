from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.evidence import Evidence
from app.models.kpi import KPI
from app.models.pilot import Pilot
from app.models.application import Application
from app.models.startup import Startup
from app.models.user import User
from app.schemas.evidence import EvidenceCreate, EvidenceStatusUpdate, EvidenceResponse
from app.auth import get_current_user, require_role

router = APIRouter(tags=["Evidence"])

@router.post("/kpis/{kpi_id}/evidence", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
def submit_evidence(
    kpi_id: int,
    evidence_in: EvidenceCreate,
    current_user: User = Depends(require_role("startup")),
    db: Session = Depends(get_db)
):
    """Startup only: submit KPI evidence for its own pilot."""
    kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KPI not found")

    pilot = db.query(Pilot).join(Application).filter(Pilot.id == kpi.pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated pilot not found")

    startup = db.query(Startup).filter(Startup.user_id == current_user.id).first()
    if not startup or pilot.application.startup_id != startup.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Startups can only submit evidence for their own pilots."
        )

    evidence = Evidence(
        pilot_id=kpi.pilot_id,
        kpi_id=kpi_id,
        submitted_value=evidence_in.submitted_value,
        description=evidence_in.description,
        status="pending",
        file_ref=evidence_in.file_ref
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence

@router.get("/pilots/{pilot_id}/evidence", response_model=list[EvidenceResponse])
def list_pilot_evidence(
    pilot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pilot = db.query(Pilot).join(Application).filter(Pilot.id == pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pilot not found")

    if current_user.role == "startup":
        startup = db.query(Startup).filter(Startup.user_id == current_user.id).first()
        if not startup or pilot.application.startup_id != startup.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return db.query(Evidence).filter(Evidence.pilot_id == pilot_id).order_by(Evidence.id.desc()).all()

@router.patch("/evidence/{evidence_id}/status", response_model=EvidenceResponse)
def update_evidence_status(
    evidence_id: int,
    status_update: EvidenceStatusUpdate,
    current_user: User = Depends(require_role("officer")),
    db: Session = Depends(get_db)
):
    """Officer only: approve or reject submitted evidence."""
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence not found")

    if evidence.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Evidence has already been processed with status '{evidence.status}'."
        )

    evidence.status = status_update.status
    db.commit()
    db.refresh(evidence)
    return evidence
