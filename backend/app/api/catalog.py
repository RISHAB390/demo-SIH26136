from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.database import get_db
from app.models.decision import Decision
from app.models.pilot import Pilot
from app.models.application import Application
from app.models.challenge import Challenge
from app.models.startup import Startup
from app.models.evaluation import Evaluation

router = APIRouter(prefix="/catalog", tags=["Innovations Catalog"])

class CatalogItem(BaseModel):
    pilot_id: int
    application_reference_id: str
    startup_name: str
    startup_sector: str
    dpiit_status: bool
    women_led: bool
    make_in_india_class: Optional[str]
    challenge_title: str
    challenge_budget_band: str
    pilot_scope: str
    recommendation: str
    evaluation_score: Optional[int] = None
    model_config = ConfigDict(from_attributes=False)

@router.get("", response_model=list[CatalogItem])
def get_innovations_catalog(db: Session = Depends(get_db)):
    """Public catalog of proven innovations - pilots with Recommend Scale decision."""
    decisions = db.query(Decision).filter(
        Decision.recommendation == "Recommend Scale"
    ).all()

    items = []
    for d in decisions:
        pilot = db.query(Pilot).options(
            joinedload(Pilot.application).joinedload(Application.startup),
            joinedload(Pilot.application).joinedload(Application.challenge),
            joinedload(Pilot.application).joinedload(Application.evaluation),
        ).filter(Pilot.id == d.pilot_id).first()
        if not pilot or not pilot.application:
            continue
        app_obj = pilot.application
        startup = app_obj.startup
        challenge = app_obj.challenge
        evaluation = app_obj.evaluation

        from datetime import date
        year = date.today().year
        ref_id = f"APP-{year}-{app_obj.id:05d}"

        items.append(CatalogItem(
            pilot_id=pilot.id,
            application_reference_id=ref_id,
            startup_name=startup.name if startup else "N/A",
            startup_sector=startup.sector if startup else "N/A",
            dpiit_status=startup.dpiit_status if startup else False,
            women_led=getattr(startup, "women_led", False),
            make_in_india_class=getattr(startup, "make_in_india_class", None),
            challenge_title=challenge.title if challenge else "N/A",
            challenge_budget_band=challenge.budget_band if challenge else "N/A",
            pilot_scope=pilot.scope,
            recommendation=d.recommendation,
            evaluation_score=int(evaluation.score) if evaluation else None,
        ))
    return items
