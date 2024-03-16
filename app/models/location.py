from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
import datetime

from app.database import Base

if TYPE_CHECKING:
    from .travel import Travel

class Location(Base):
    __tablename__ = 'location'

    id: Mapped[int] = mapped_column(primary_key=True)
    travel: Mapped['Travel'] = relationship(back_populates='locations')
    travel_id: Mapped[int] = mapped_column(ForeignKey('travel.id'))
    city: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    arrive_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    departure_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)