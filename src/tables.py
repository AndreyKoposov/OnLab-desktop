import json
from sqlalchemy import Column, Integer, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, TEXT


Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(TEXT)
    created_at = Column(DateTime, server_default='now()')

    def __repe__(self):
        return f"<user {self.id}>"

class ProcessTable(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True)
    data = Column(JSONB)
    created_at = Column(DateTime, server_default='now()')

    def __repe__(self):
        return f"<process {self.id}>"
