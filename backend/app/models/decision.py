from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    pilot_id: Mapped[int] = mapped_column(Integer, ForeignKey("pilots.id", ondelete="CASCADE"), unique=True, nullable=False)
    recommendation: Mapped[str] = mapped_column(String(100), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    pilot = relationship("Pilot", back_populates="decision")
