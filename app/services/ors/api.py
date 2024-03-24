from typing import Dict, List, Tuple
from config import ORS_KEY

import requests


async def request_ors_api(coordinates: List[Tuple[float, float]]) -> Dict:
    url = 'https://api.openrouteservice.org/v2/directions/driving-hgv'
    body = {
        'coordinates': coordinates,
        'radiuses': [-1]
    }
    response = requests.post(url, json=body, headers={'Authorization': ORS_KEY})
    data = response.json()
    return data
