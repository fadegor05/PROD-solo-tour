from typing import TYPE_CHECKING, List
from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .member import Member
    from .note import Note
    from .invitation import Invitation

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(nullable=False, default=str(uuid4()))
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    travels: Mapped[List['Member']] = relationship(back_populates='user', lazy='selectin')
    notes: Mapped[List['Note']] = relationship(back_populates='user')
    invitations: Mapped[List['Invitation']] = relationship(back_populates='user', lazy='selectin')