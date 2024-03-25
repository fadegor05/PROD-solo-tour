from typing import List, Tuple

from app.services.kudago.api import request_categories_kudago, request_places_kudago, request_place_kudago
from app.services.kudago.schemas import CategoryKudago, PlaceKudago, ExtendedPlaceKudago


async def get_categories_kudago() -> List[CategoryKudago]:
    data = await request_categories_kudago()
    categories = []
    for category in data:
        categories.append(CategoryKudago(**category))
    return categories


async def get_places_kudago(coordinates: Tuple[float, float], category: str) -> List[PlaceKudago]:
    data = await request_places_kudago(coordinates[0], coordinates[1], category)
    places = []
    for place in data['results']:
        places.append(PlaceKudago(**place))
    return places


async def get_place_kudago(place_id: int) -> ExtendedPlaceKudago:
    data = await request_place_kudago(place_id)
    return ExtendedPlaceKudago(**data)
