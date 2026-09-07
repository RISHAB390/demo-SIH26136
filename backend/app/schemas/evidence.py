from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class EvidenceBase(BaseModel):
    submitted_value: float
    description: str = Field(..., min_length=3)
    file_ref: str | None = None

class EvidenceCreate(EvidenceBase):
    pass

class EvidenceStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(approved|rejected)$")

class EvidenceResponse(EvidenceBase):
    id: int
    pilot_id: int
    kpi_id: int
    submitted_date: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)
