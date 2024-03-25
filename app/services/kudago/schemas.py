from typing import List

from pydantic import BaseModel


class PlaceKudago(BaseModel):
    id: int
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    images: List | None = None
    categories: List | None = None


class ExtendedPlaceKudago(PlaceKudago):
    address: str | None = None
    timetable: str | None = None
    phone: str | None = None
    site_url: str | None = None
    favorites_count: int | None = None



class CategoryKudago(BaseModel):
    id: int
    slug: str
    name: str
