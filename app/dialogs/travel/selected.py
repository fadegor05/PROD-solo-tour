from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from app.dialogs.travel.states import TravelMenu


async def on_chosen_travel(c: CallbackQuery, widget: Select, manager: DialogManager, item_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(travel_id=item_id)
    await manager.switch_to(TravelMenu.select_action)