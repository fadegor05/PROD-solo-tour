from aiogram_dialog import DialogManager

from app.database import async_session


async def get_notes(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        #user_id = dialog_manager.middleware_data.get('event_chat').id
        #user = await get_user_by_telegram_id(session, user_id)
        #travels = []
        #for member in user.travels:
        #    travel = member.travel
        #    travels.append(travel)

        return {
            'notes': [
                (
                    32,
                    'temp_name'
                )
            ]
        }