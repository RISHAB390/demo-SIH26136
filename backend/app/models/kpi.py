from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class KPI(Base):
    __tablename__ = "kpis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    pilot_id: Mapped[int] = mapped_column(Integer, ForeignKey("pilots.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    pilot = relationship("Pilot", back_populates="kpis")
    evidence_records = relationship("Evidence", back_populates="kpi", cascade="all, delete-orphan")
