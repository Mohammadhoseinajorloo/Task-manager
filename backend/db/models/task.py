from datetime import datetime

from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship


class Task(Base):
    task_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    owner = relationship("User", back_populates="tasks_id")
    created_at = Column(DateTime, default=datetime.now())
    is_done = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
