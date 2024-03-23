from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Button
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.note import keyboards, selected, states, getters


def notes_window():
    return Window(
        Const('Выберите заметку, которую хотите'),
        keyboards.paginated_notes(selected.on_chosen_note),
        Button(Const('Создать заметку'), 'create_note', selected.on_create_note),
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


def note_name_window():
    return Window(
        Const('Введите название заметки'),
        TextInput(
            id='note_enter_name',
            on_success=selected.on_entered_name
        ),
        state=states.CreateNote.name
    )


def note_is_public_window():
    return Window(
        Const('Будет ли эта заметка публичной?'),
        Button(Const('Да'), 'note_public_true', selected.on_is_public_true),
        Button(Const('Нет'), 'note_public_false', selected.on_is_public_false),
        state=states.CreateNote.is_public
    )


def note_text_window():
    return Window(
        Const('Введите текст заметки'),
        TextInput(
            id='note_enter_text',
            on_success=selected.on_entered_text
        ),
        state=states.CreateNote.text
    )
