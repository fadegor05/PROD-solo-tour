import datetime
from typing import Tuple

from app.services.om.api import request_om_api
from app.services.om.schema import Weather


async def weather_code_handler(code: int) -> str:
    if 0 <= code <= 1:
        return '☀️ Ясно'
    elif 2 <= code < 61:
        return '☁️ Облачно'
    elif 61 <= code <= 67:
        return '🌧️ Дождь'
    elif 71 <= code <= 77:
        return '🌨️ Снег'
    elif 80 <= code <= 82:
        return '🌧️ Ливень'
    elif 85 <= code <= 86:
        return '🌨️ Снегопад'
    elif 95 <= code <= 99:
        return '⛈️ Гроза'
    return '⚠️ Не удалось определить погоду'


async def get_location_weather(coordinates: Tuple[int, int], start_date: datetime.datetime,
                               end_date: datetime.datetime) -> Weather:
    data = await request_om_api(coordinates, start_date, end_date)
    om_response = data[0]
    weather = await weather_code_handler(om_response['weather_code'][0])
    temperature = sum(om_response['temperature_2m_max'])/len(om_response['temperature_2m_max'])
    return Weather(weather=weather, temperature=temperature, is_dates=data[1])

