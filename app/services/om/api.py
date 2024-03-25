import datetime
from typing import Dict, List, Tuple

import requests


async def request_current(url: str, coordinates: Tuple[float, float]) -> Dict:
    query = {
        'longitude': coordinates[0],
        'latitude': coordinates[1],
        'daily': 'weather_code,temperature_2m_max,temperature_2m_min',
        'forecast_days': 1
    }
    response = requests.get(url, params=query)
    data = response.json()
    return data


async def request_dates(url: str, coordinates: Tuple[float, float], start_date: datetime.datetime,
                        end_date: datetime.datetime) -> Dict | None:
    query = {
        'longitude': coordinates[0],
        'latitude': coordinates[1],
        'daily': 'weather_code,temperature_2m_max,temperature_2m_min',
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    response = requests.get(url, params=query)
    data: Dict = response.json()
    if data.get('error'):
        return None
    return data


async def request_om_api(coordinates: Tuple[float, float], start_date: datetime.datetime,
                         end_date: datetime.datetime) -> Tuple[Dict, bool]:
    is_dates = True
    url = 'https://api.open-meteo.com/v1/forecast'
    data = await request_dates(url, coordinates, start_date, end_date)
    if not data:
        data = await request_current(url, coordinates)
        is_dates = False
    return data['daily'], is_dates
