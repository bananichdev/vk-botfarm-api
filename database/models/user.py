from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from utils.enums import DomainType, EnvType

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[UUID] = mapped_column(nullable=False)
    env: Mapped[EnvType] = mapped_column(nullable=False)
    domain: Mapped[DomainType] = mapped_column(nullable=False)
    locktime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "login ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$'",
            name="login_validation",
        ),
    )
