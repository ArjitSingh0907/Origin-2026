from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schemas


def get_registration_by_email(db: Session, email: str):
    return (
        db.query(models.Registration)
        .filter(models.Registration.leader_email == email)
        .first()
    )


def get_registration_by_team_name(db: Session, team_name: str):
    return (
        db.query(models.Registration)
        .filter(models.Registration.team_name == team_name)
        .first()
    )


def create_registration(db: Session, data: schemas.RegistrationIn) -> models.Registration:
    reg = models.Registration(
        team_name=data.team_name,
        college=data.college,
        track=data.track,
        leader_name=data.leader_name,
        leader_email=data.leader_email,
        leader_phone=data.leader_phone,
    )
    reg.members = [
        models.TeamMember(name=m.name, email=m.email) for m in data.members
    ]
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return reg


def list_registrations(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Registration)
        .order_by(models.Registration.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
