from datetime import datetime

from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship


class Task(Base):
    task_id = Column(Integer, primary_key=True)
    title = Column(String , nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("user.user_id"))
    owner = relationship("User", back_populates="tasks")
    create_at = Column(DateTime, default=datetime.now)
    is_done = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
