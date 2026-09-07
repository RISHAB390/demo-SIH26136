from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.kpi import KPI
from app.models.pilot import Pilot
from app.models.application import Application
from app.models.startup import Startup
from app.models.user import User
from app.schemas.kpi import KPICreate, KPIResponse
from app.auth import get_current_user, require_role

router = APIRouter(tags=["KPIs"])

@router.post("/pilots/{pilot_id}/kpis", response_model=KPIResponse, status_code=status.HTTP_201_CREATED)
def create_kpi(
    pilot_id: int,
    kpi_in: KPICreate,
    current_user: User = Depends(require_role("officer")),
    db: Session = Depends(get_db)
):
    """Officer only: define a KPI for a pilot."""
    pilot = db.query(Pilot).filter(Pilot.id == pilot_id).first()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pilot not found")

    kpi = KPI(
        pilot_id=pilot_id,
        name=kpi_in.name,
        target_value=kpi_in.target_value,
        unit=kpi_in.unit
    )
    db.add(kpi)
    db.commit()
    db.refresh(kpi)
    return kpi

@router.get("/pilots/{pilot_id}/kpis", response_model=list[KPIResponse])
def list_pilot_kpis(
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

    return db.query(KPI).filter(KPI.pilot_id == pilot_id).all()
