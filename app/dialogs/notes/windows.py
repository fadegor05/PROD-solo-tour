from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Cancel
from aiogram_dialog.widgets.text import Const

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
        Const('Хаки ваки'),
        Back(Const('Назад')),
        state=states.NoteMenu.select_action,
    )
