import json
from typing import Union

from aiogram import Bot
from aiogram.types import InputFile
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.manager.message_manager import MessageManager

from app.services.ors.service import get_wrapped_rendered_map

CUSTOM_URL_PREFIX = "memory://"


class CustomMessageManager(MessageManager):
    async def get_media_source(
        self, media: MediaAttachment, bot: Bot,
    ) -> Union[InputFile, str]:
        if media.file_id:
            return await super().get_media_source(media, bot)
        if media.url and media.url.startswith(CUSTOM_URL_PREFIX):
            text = media.url[len(CUSTOM_URL_PREFIX):]
            points = json.loads(text)
            return await get_wrapped_rendered_map(points['points'])
        return await super().get_media_source(media, bot)