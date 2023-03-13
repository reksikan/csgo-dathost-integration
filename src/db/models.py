from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import ARRAY, UUID, Column, DateTime, SmallInteger, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Match(Base):
    __tablename__ = 'match'

    class Status(str, Enum):
        in_process = 'in_process'
        finished = 'finished'

    id: str = Column(Text, primary_key=True)
    secret_key: str = Column(UUID, nullable=False)
    server_id: str = Column(Text, nullable=False)
    server_host: str = Column(Text, nullable=False)
    status: Status = Column(Text, default=Status.in_process)
    created_at: datetime = Column(DateTime, default=datetime.utcnow())
    map: str = Column(Text, nullable=False)
    max_rounds: str = Column(SmallInteger, nullable=False)

    team1_name: str = Column(Text, nullable=False)
    team1_score: int = Column(SmallInteger, default=0)
    team1_roster: List[str] = Column(ARRAY(Text), nullable=False)

    team2_name: str = Column(Text, nullable=False)
    team2_score: int = Column(SmallInteger, default=0)
    team2_roster: List[str] = Column(ARRAY(Text), nullable=False)
