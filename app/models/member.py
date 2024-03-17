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
    user: Mapped['User'] = relationship(back_populates='travels')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    travel: Mapped['Travel'] = relationship(back_populates='members')
    travel_id: Mapped[int] = mapped_column(ForeignKey('travel.id'))