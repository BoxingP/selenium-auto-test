import datetime

from sqlalchemy import Column, Integer, String, Time, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Step(Base):
    __tablename__ = 'step'
    id = Column(Integer, primary_key=True, nullable=False)
    page = Column(String, nullable=False)
    test = Column(String, nullable=False)
    is_summary = Column(Boolean, nullable=False)
    step = Column(String)
    log_dt = Column(Time)
    spent_time = Column(Float)
    created_dt = Column(Time, default=datetime.datetime.utcnow() + datetime.timedelta(hours=8), nullable=False)
    created_by = Column(String, default='System', nullable=False)
