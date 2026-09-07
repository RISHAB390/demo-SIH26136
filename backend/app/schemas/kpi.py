from pydantic import BaseModel, ConfigDict, Field

class KPIBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    target_value: float
    unit: str = Field(..., max_length=50)

class KPICreate(KPIBase):
    pass

class KPIResponse(KPIBase):
    id: int
    pilot_id: int

    model_config = ConfigDict(from_attributes=True)
