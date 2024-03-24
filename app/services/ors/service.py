from io import BytesIO
from typing import List, Tuple

from aiogram.types import InputMediaPhoto, InputFile, BufferedInputFile
from polyline import decode
from PIL.Image import Image

from app.services.ors.api import request_ors_api
from app.services.ors.map import create_map


async def get_rendered_map(points_coordinates: List[Tuple[float, float]]) -> Image | None:
    if len(points_coordinates) == 0:
        return None
    data = await request_ors_api(points_coordinates)
    encoded_polyline = data["routes"][0]["geometry"]
    line_coordinates = decode(encoded_polyline, geojson=True)
    static_map = await create_map(line_coordinates, points_coordinates)
    return static_map.render()


async def get_wrapped_rendered_map(points_coordinates: List[Tuple[float, float]]) -> InputFile:
    image = await get_rendered_map(points_coordinates)
    bytesio = BytesIO()
    bytesio.name = 'map.png'
    image.save(bytesio, "PNG")
    bytesio.seek(0)
    return BufferedInputFile(bytesio.read(), 'map.png')
