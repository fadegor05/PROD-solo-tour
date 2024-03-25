from typing import TYPE_CHECKING, List
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .image import Image
    from .travel import Travel
    from .user import User

class Note(Base):
    __tablename__ = 'note'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    text: Mapped[str]
    is_public: Mapped[bool] = mapped_column(default=True)
    travel: Mapped['Travel'] = relationship(back_populates='notes', lazy='selectin')
    travel_id: Mapped[int] = mapped_column(ForeignKey('travel.id'))
    user: Mapped['User'] = relationship(back_populates='notes', lazy='selectin')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
