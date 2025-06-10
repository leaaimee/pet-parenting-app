from backend.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, relationship
from backend.models.users_models import Users


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    care_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    priority = Column(String(50), nullable=True)
    recurring = Column(Boolean, default=False)
    frequency = Column(String(50), nullable=True)

    # owner = relationship("Users", back_populates="tasks")