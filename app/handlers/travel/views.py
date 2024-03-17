from app.models.travel import Travel

async def travel_out(travel: Travel) -> str:
    string = f'*Путешествие {travel.name}* 💼\n{travel.description}'
    return string