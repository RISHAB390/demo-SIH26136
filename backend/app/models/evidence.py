from datetime import datetime
from sqlalchemy import Integer, String, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    pilot_id: Mapped[int] = mapped_column(Integer, ForeignKey("pilots.id", ondelete="CASCADE"), nullable=False)
    kpi_id: Mapped[int] = mapped_column(Integer, ForeignKey("kpis.id", ondelete="CASCADE"), nullable=False)
    submitted_value: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    submitted_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending, approved, rejected
    file_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    pilot = relationship("Pilot", back_populates="evidence_records")
    kpi = relationship("KPI", back_populates="evidence_records")
