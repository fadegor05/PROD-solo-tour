from pydantic import BaseModel


class Weather(BaseModel):
    weather: str
    temperature: float
    is_dates: bool
