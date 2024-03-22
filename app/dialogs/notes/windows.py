from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Cancel
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.notes import keyboards, selected, states, getters


def notes_window():
    return Window(
        Const('Выберите заметку, которую хотите'),
        keyboards.paginated_notes(selected.on_chosen_note),
        Cancel(Const('Назад')),
        state=states.NoteMenu.select_note,
        getter=getters.get_notes,
    )


def note_info_window():
    return Window(
        Format('Заметка {note_name}\n\n{note_text}\n\nАвтор: {user}'),
        Back(Const('Назад')),
        state=states.NoteMenu.select_action,
        getter=getters.get_note,
    )
