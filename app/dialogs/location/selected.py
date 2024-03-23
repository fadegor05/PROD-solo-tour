from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from app.dialogs.location.states import LocationMenu


async def on_chosen_location(c: CallbackQuery, widget: Select, manager: DialogManager, location_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(location_id=location_id)
    await manager.switch_to(LocationMenu.select_action)


async def on_create_location(c: CallbackQuery, widget: Button, manager: DialogManager):
    pass
    #await manager.start(CreateNote.name, data={'travel_id': manager.start_data.get('travel_id')})