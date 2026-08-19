"""
Database tables for ORIGIN '26 registrations.

Registration  -> one row per team
TeamMember    -> one row per member of that team (leader included)
"""
import datetime
import uuid

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_name = Column(String(120), unique=True, nullable=False, index=True)
    college = Column(String(200), nullable=False)
    track = Column(String(120), nullable=False)  # e.g. chosen "Solution Pathway"

    leader_name = Column(String(120), nullable=False)
    leader_email = Column(String(200), unique=True, nullable=False, index=True)
    leader_phone = Column(String(20), nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    members = relationship(
        "TeamMember", back_populates="registration", cascade="all, delete-orphan"
    )


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_id = Column(
        UUID(as_uuid=True), ForeignKey("registrations.id"), nullable=False
    )
    name = Column(String(120), nullable=False)
    email = Column(String(200), nullable=False)

    registration = relationship("Registration", back_populates="members")