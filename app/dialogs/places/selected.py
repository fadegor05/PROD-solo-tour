from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from app.dialogs.places.states import PlaceMenu


async def on_chosen_category(c: CallbackQuery, widget: Select, manager: DialogManager, category_slug: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(category_slug=category_slug)
    await manager.switch_to(PlaceMenu.select_place)


async def on_chosen_place(c: CallbackQuery, widget: Select, manager: DialogManager, place_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(place_id=place_id)
    await manager.switch_to(PlaceMenu.view_place)
