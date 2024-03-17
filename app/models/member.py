from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base

if TYPE_CHECKING:
    from .travel import Travel
    from .user import User

class Member(Base):
    __tablename__ = 'member'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped['User'] = relationship(back_populates='travels', lazy='selectin')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    is_owner: Mapped[bool] = mapped_column(default=False)

    travel: Mapped['Travel'] = relationship(back_populates='members', lazy='selectin')
    travel_id: Mapped[int] = mapped_column(ForeignKey('travel.id'))