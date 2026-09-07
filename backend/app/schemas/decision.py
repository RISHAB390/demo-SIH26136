from pydantic import BaseModel, ConfigDict, Field

class DecisionBase(BaseModel):
    recommendation: str = Field(..., min_length=2, max_length=100)
    notes: str = Field(..., min_length=3)

class DecisionCreate(DecisionBase):
    pass

class DecisionResponse(DecisionBase):
    id: int
    pilot_id: int

    model_config = ConfigDict(from_attributes=True)

class DecisionSupportResponse(BaseModel):
    pilot_id: int
    total_kpis: int
    approved_kpis: int
    achievement_ratio: float
    recommendation: str
    explanation: str
