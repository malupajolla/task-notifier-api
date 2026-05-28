from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id           = Column(Integer, primary_key=True, index=True)
    titulo       = Column(String, nullable=False)
    data_hora    = Column(DateTime, default=datetime.now)
    destinatario = Column(String, nullable=False)
    concluida    = Column(Boolean, default=False)