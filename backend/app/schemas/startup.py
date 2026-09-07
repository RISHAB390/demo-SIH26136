from pydantic import BaseModel, ConfigDict

class StartupBase(BaseModel):
    name: str
    sector: str
    dpiit_status: bool = False
    profile_text: str

class StartupCreate(StartupBase):
    pass

class StartupResponse(StartupBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
