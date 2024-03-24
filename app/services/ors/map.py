from typing import Tuple, List

from staticmap import StaticMap, Line, CircleMarker


async def create_map(line_coordinates: List[Tuple[float, float]], points_coordinates: List[Tuple[float, float]]) -> StaticMap:
    static_map = StaticMap(800, 800)
    static_map.add_line(Line(line_coordinates, 'green', 3))
    for point in points_coordinates:
        static_map.add_marker(CircleMarker(point, 'green', 8))
    return static_map
