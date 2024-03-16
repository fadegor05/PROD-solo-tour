from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .location import Location
    from .member import Member

class Travel(Base):
    __tablename__ = 'travel'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    locations: Mapped[List['Location']] = relationship(back_populates='travel')
    members: Mapped[List['Member']] = relationship(back_populates='travel')