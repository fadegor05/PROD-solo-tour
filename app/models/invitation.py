from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base

if TYPE_CHECKING:
    from .travel import Travel
    from .user import User

class Invitation(Base):
    __tablename__ = 'invitation'

    id: Mapped[int] = mapped_column(primary_key=True)
    travel: Mapped['Travel'] = relationship(back_populates='invitations', lazy='selectin')
    travel_id: Mapped[int] = mapped_column(ForeignKey('travel.id'))
    user: Mapped['User'] = relationship(back_populates='invitations', lazy='selectin')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))