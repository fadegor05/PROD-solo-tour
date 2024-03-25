from typing import Dict

import requests

BASE_KUDAGO_URL = 'https://kudago.com/public-api/v1.4'


async def request_categories_kudago() -> Dict:
    url = f'{BASE_KUDAGO_URL}/place-categories/'
    query = {
        'lang': 'ru'
    }
    response = requests.get(url, params=query)
    return response.json()


async def request_places_kudago(lon: float, lat: float, category: str) -> Dict:
    url = f'{BASE_KUDAGO_URL}/places/'
    query = {
        'lang': 'ru',
        'lon': lon,
        'lat': lat,
        'radius': 50000,
        'categories': category,
        'text_format': 'text',
        'page': 1,
        'page_size': 100
    }
    response = requests.get(url, params=query)
    return response.json()


async def request_place_kudago(place_id: int) -> Dict:
    url = f'{BASE_KUDAGO_URL}/places/{place_id}'
    query = {
        'lang': 'ru',
        'text_format': 'text'
    }
    response = requests.get(url, params=query)
    return response.json()
