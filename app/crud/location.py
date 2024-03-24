import datetime
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Location, Travel


async def delete_location(session: AsyncSession, location: Location) -> None:
    await session.delete(location)
    await session.commit()



async def delete_locations_by_travel(session: AsyncSession, travel: Travel) -> None:
    for location in travel.locations:
        await session.delete(location)
    await session.commit()


async def get_location_by_id(session: AsyncSession, id: int) -> Location | None:
    stmt = Select(Location).where(Location.id == id)
    location = await session.scalar(stmt)
    return location


async def create_location(session: AsyncSession, travel: Travel, city: str, country: str, arrive_at: datetime.datetime,
                          departure_at: datetime.datetime) -> Location:
    location = Location(travel=travel, city=city, country=country, arrive_at=arrive_at, departure_at=departure_at)
    session.add(location)
    await session.commit()
    await session.refresh(location)
    return location
