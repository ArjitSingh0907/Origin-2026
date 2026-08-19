"""
Pydantic models: define exactly what the API accepts and returns.
Adjust TeamMemberIn / RegistrationIn fields to match your actual
frontend form field names before wiring things up.
"""
import uuid
import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field, field_validator


class TeamMemberIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr


class RegistrationIn(BaseModel):
    team_name: str = Field(..., min_length=2, max_length=120)
    college: str = Field(..., min_length=2, max_length=200)
    track: str = Field(..., min_length=2, max_length=120)

    leader_name: str = Field(..., min_length=2, max_length=120)
    leader_email: EmailStr
    leader_phone: str = Field(..., min_length=7, max_length=20)

    # Additional teammates besides the leader (0 to 3 for a 4-person team cap, adjust as needed)
    members: List[TeamMemberIn] = []

    @field_validator("members")
    @classmethod
    def cap_team_size(cls, v):
        if len(v) > 5:
            raise ValueError("A team can have at most 6 members including the leader.")
        return v


class TeamMemberOut(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class RegistrationOut(BaseModel):
    id: uuid.UUID
    team_name: str
    college: str
    track: str
    leader_name: str
    leader_email: EmailStr
    leader_phone: str
    created_at: datetime.datetime
    members: List[TeamMemberOut]

    class Config:
        from_attributes = True
