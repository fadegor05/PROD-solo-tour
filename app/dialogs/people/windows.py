from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Cancel
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.people import getters, states, selected, keyboards


def people_window():
    return Window(
        Const('Выберите пользователя из нашей рекомендации, который вам интересен 👥'),
        keyboards.paginated_people(selected.on_chosen_person),
        Cancel(Const('⬅️ Назад')),
        getter=getters.get_people,
        state=states.PersonMenu.select_person
    )


def person_info_window():
    return Window(
        Format('Пользователь {name} ({age}) 👤\n\n{bio}\n\n📍{city}, {country}\n🔑 Код для приглашения в путешествие:\n{uuid}'),
        Back(Const('⬅️ Назад')),
        getter=getters.get_person,
        state=states.PersonMenu.view_person
    )