from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # officer, startup, evaluator
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, default="")  # bcrypt hash

    # Relationships
    startup = relationship("Startup", back_populates="user", uselist=False)
    challenges = relationship("Challenge", back_populates="officer")
    evaluations = relationship("Evaluation", back_populates="evaluator")
