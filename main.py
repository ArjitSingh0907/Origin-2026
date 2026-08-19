from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models, schemas, crud
from app.database import engine, get_db, Base
from app.email_utils import send_confirmation_email
from app.config import settings

# Creates tables if they don't exist yet. For production, prefer Alembic
# migrations instead of relying on this (see README).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ORIGIN '26 Registration API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/register", response_model=schemas.RegistrationOut, status_code=201)
def register_team(
    payload: schemas.RegistrationIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if crud.get_registration_by_email(db, payload.leader_email):
        raise HTTPException(
            status_code=409, detail="This email has already registered a team."
        )
    if crud.get_registration_by_team_name(db, payload.team_name):
        raise HTTPException(
            status_code=409, detail="This team name is already taken."
        )

    try:
        registration = crud.create_registration(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate registration.")

    background_tasks.add_task(
        send_confirmation_email,
        to_email=registration.leader_email,
        team_name=registration.team_name,
        leader_name=registration.leader_name,
    )

    return registration


@app.get("/api/registrations", response_model=list[schemas.RegistrationOut])
def get_registrations(
    x_admin_key: str = Header(...),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin key.")
    return crud.list_registrations(db, skip=skip, limit=limit)