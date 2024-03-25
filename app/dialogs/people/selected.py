from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from app.dialogs.people.states import PersonMenu


async def on_chosen_person(c: CallbackQuery, widget: Select, manager: DialogManager, user_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(user_id=user_id)
    await manager.switch_to(PersonMenu.view_person)