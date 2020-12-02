from os.path import basename
from urllib.parse import urlsplit
from urllib.request import urlretrieve, urlcleanup
from telebot import TeleBot
from django.core.files import File

from old_code_for_use.keyboards import Action
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardMarkup
from bots_management.models import Channel
from subscribers.models import Message
from subscribers.services import (
    get_subscriber_telegram
)


def create_markup(action: Action) -> ReplyKeyboardMarkup:
    """
    Creates markup for the telegram keyboard.

    Returns:
        ReplyKeyboardMarkup that represents markup.
    """
    markup = ReplyKeyboardMarkup()
    btn_array = action.keyboard_to_represent.get_telegram_buttons()
    for row in btn_array:
        inline_btns = [
            KeyboardButton(
                text=btn.text,
            ) for btn in row
        ]
        markup.row(*inline_btns)
    return markup


def save_message(channel: Channel, in_data: dict,
                 is_help_message: bool = False) -> None:
    """
    Save massage info from telegram subscribers in db
    field what can be saved:
    ['document', 'photo', 'audio', 'video',
     'voice', 'sticker', 'text', 'caption', 'location']
    """
    if not channel:
        raise ValueError("How did it happen?? 0_0")
    message = in_data["message"]
    message_token = message.get('message_id')

    subscriber, _ = get_subscriber_telegram(
        user=message.get('chat'),
        channel=channel
    )
    message_instance = Message(sender=subscriber, message_token=message_token)
    if 'text' in message.keys():
        message_instance.text = message.get('text')
    elif channel.is_media_allowed:

        if 'photo' in message.keys():
            # get only original size, it always last
            file_id = message['photo'][-1].get('file_id')
            message_instance.url = tg_get_path_file(
                channel.telegram_token, file_id
            )
            download_to_file_field(url=message_instance.url,
                                   field=message_instance.image)
            # save caption of the image
            message_instance.text = {message.get('caption')}

        for type_file in ['document', 'audio', 'video', 'voice', 'sticker']:
            if type_file in message.keys():
                file_id = message[type_file].get('file_id')
                message_instance.url = tg_get_path_file(
                    channel.telegram_token, file_id
                )
                download_to_file_field(url=message_instance.url,
                                       field=message_instance.file)
                # save caption of the file
                message_instance.text = {message.get('caption')}

    location = message.get('location')
    if location and channel.is_geo_allowed:
        message_instance.location = location

    if is_help_message:
        message_instance.is_help_message = True

    message_instance.save()


def tg_get_path_file(token: str, file_id: str) -> str:
    """
    return url-path for download file from telegram
    """
    tg_bot = TeleBot(token)
    file_info = tg_bot.get_file(file_id)
    return f"https://api.telegram.org/file/bot{token}/{file_info.file_path}"


def download_to_file_field(url, field) -> None:
    """
    download file on server
    """
    try:
        name, _ = urlretrieve(url)
        field.save(basename(urlsplit(url).path), File(open(name, 'rb')))
    finally:
        urlcleanup()
