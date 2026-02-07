from pydantic import BaseModel

from app.shared.types.enum import CurrentSession, RoleUser


class UserStatus(BaseModel):
    session: CurrentSession
    role: RoleUser
