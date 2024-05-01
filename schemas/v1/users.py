from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from utils.enums import DomainType, EnvType


class UserOperationOk(BaseModel):
    id: UUID


class UserCreatingData(BaseModel):
    login: EmailStr
    password: str
    project_id: UUID
    domain: DomainType


class User(UserOperationOk):
    login: str
    project_id: UUID
    env: EnvType
    domain: DomainType
    locktime: datetime | None
    created_ad: datetime
