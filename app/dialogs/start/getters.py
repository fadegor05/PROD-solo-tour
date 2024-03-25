from aiogram_dialog import DialogManager


async def get_city_confirm(dialog_manager: DialogManager, **kwargs):
    return {
        'city': dialog_manager.current_context().dialog_data.get('city'),
        'country': dialog_manager.current_context().dialog_data.get('country')
    }