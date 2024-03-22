from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from app.dialogs.notes.states import NoteMenu


async def on_chosen_note(c: CallbackQuery, widget: Select, manager: DialogManager, note_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(note_id=note_id)
    await manager.switch_to(NoteMenu.select_action)