from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.schemas.kpi import KPIResponse
from app.schemas.decision import DecisionResponse

class PilotBase(BaseModel):
    scope: str = Field(..., min_length=5)
    timeline_start: date
    timeline_end: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.timeline_end < self.timeline_start:
            raise ValueError("timeline_end must be greater than or equal to timeline_start")
        return self

class PilotCreate(PilotBase):
    application_id: int

class PilotResponse(PilotBase):
    id: int
    application_id: int
    status: str
    kpis: list[KPIResponse] = []
    decision: DecisionResponse | None = None

    model_config = ConfigDict(from_attributes=True)
