from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .note import Note

class Image(Base):
    __tablename__ = 'image'

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped['Note'] = relationship(back_populates='images')
    note_id: Mapped[int] = mapped_column(ForeignKey('note.id'))
    path: Mapped[str]

