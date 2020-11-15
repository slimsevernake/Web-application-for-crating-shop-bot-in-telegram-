import logging
from typing import Union

import requests

from django.conf import settings

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, Message
from telebot.apihelper import ApiException

from moviepy.editor import VideoFileClip

from keyboards.models import IdFilesInMessenger

logger = logging.getLogger(__name__)


def get_webhook_info(token: str) -> dict:
    """
    Get information about tg webhook
    """
    res = requests.get(settings.TELEGRAM_BASE_URL % (token, "getWebhookInfo"))
    return res.json().get('result')


def get_bot_info(token: str) -> dict:
    """
        Get information about tg bot
    """
    res = requests.get(settings.TELEGRAM_BASE_URL % (token, "getMe"))
    return res.json().get('result')


def send_message(chat_id: int, text: str, token: str,
                 reply_markup: ReplyKeyboardMarkup = None,
                 **kwargs) -> Message:
    """Sends `sendMessage` API request to the telegramAPI.

    chat_id: Id of the chat.
    text: Text of the message.
    reply_markup: Instance of the `InlineKeyboardMarkup`.
    token: bot's token

    Returns: None.
    """
    try:
        response: Message = TeleBot(token).send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )
        return response
    except ApiException as e:
        logger.warning(
            f"""Send message to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )
    except Exception as e:
        logger.critical(
            f"""Send message to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )


def send_photo(chat_id: int, token: str,
               action: object, file_path: str = None,
               file_id: str = None, **kwargs) -> Message:
    """Sends `sendPhoto` API request to the telegramAPI.

    chat_id: Id of the chat.
    file_path: path to the file.
    file_id: id of the file
    token: bot's token

    Returns: None.
    """
    if not file_id:
        file_id = check_file_id(action, file_path, token)
    if not file_id and not file_path:
        raise ValueError('file_id or file_path  must be provided')

    try:
        if file_id:
            response: Message = TeleBot(token).send_photo(
               chat_id=chat_id, photo=file_id
            )
        else:
            with open(file_path, 'rb') as file:
                response: Message = TeleBot(token).send_photo(
                    chat_id=chat_id, photo=file
                )
                file_id = response.json.get('photo')[-1].get('file_id')
                update_or_create_file_id(action, file_path, file_id, token)
        return response

    except ApiException as e:
        logger.warning(
            f"""Send photo to {chat_id} failed.
            token: {token}.
            Error ApiException: {e}"""
        )
    except Exception as e:
        logger.critical(
            f"""Send photo to {chat_id} failed.
            token: {token}.
            Error Exception: {e}"""
        )


def check_file_id(action: object,
                  file_path: str,
                  token: str) -> Union[str, None]:
    info = IdFilesInMessenger.objects.filter(action=action, token_tg=token)
    if info.exists():
        info = info.first()
        if info.path_media_tg == file_path:
            return info.telegram_id


def update_or_create_file_id(action: object,
                             file_path: str = None,
                             file_id: str = None,
                             token: str = None) -> IdFilesInMessenger:
    return IdFilesInMessenger.objects.update_or_create(
        action=action,
        token_tg=token,
        defaults={
            'action': action,
            'path_media_tg': file_path,
            'telegram_id': file_id,
            'token_tg': token,
        }
    )


def send_video(chat_id: int, token: str,
               action: object, file_path: str = None,
               file_id: str = None, **kwargs) -> Message:
    """Sends `sendVideo` API request to the telegramAPI.

    chat_id: Id of the chat.
    file_path: path to the file.
    file_id: id of the file.
    token: bot's token

    Returns: None.
    """
    if not file_id:
        file_id = check_file_id(action, file_path, token)
    if not file_id and not file_path:
        raise ValueError('file_id or file_path  must be provided')
    try:
        if file_id:
            response: Message = TeleBot(token).send_video(
                chat_id=chat_id, data=file_id
            )
        else:
            with open(file_path, 'rb') as file:
                clip = VideoFileClip(file_path)
                response: Message = TeleBot(token).send_video(
                    chat_id=chat_id, data=file, duration=clip.duration
                )
                file_id = response.json.get('video').get('file_id')
                update_or_create_file_id(action, file_path, file_id)
        return response

    except ApiException as e:
        logger.warning(
            f"""Send video to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )
    except Exception as e:
        logger.warning(
            f"""Send video to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )


def send_document(chat_id: int, token: str,
                  action: object, file_path: str = None,
                  file_id: str = None, **kwargs) -> Message:
    """Sends `sendDocument` API request to the telegramAPI.

    chat_id: Id of the chat.
    file_path: path to the file.
    file_id: id of the file
    token: bot's token

    Returns: None.
    """
    if not file_id:
        file_id = check_file_id(action, file_path, token)
    if not file_id and not file_path:
        raise ValueError('file_id or file_path  must be provided')
    try:
        if file_id:
            response: Message = TeleBot(token).send_document(
                chat_id=chat_id, data=file_id
            )
        else:
            with open(file_path, 'rb') as file:
                response: Message = TeleBot(token).send_document(
                    chat_id=chat_id, data=file
                )
                file_id = response.json.get('document').get('file_id')
                update_or_create_file_id(action, file_path, file_id)
        return response

    except ApiException as e:
        print(f"LOGGING: {e}")
    except Exception as e:
        print(f"LOGGING: {e}")


def send_location(chat_id: int, token: str,
                  lat: int, lon: int, **kwargs) -> Message:
    """Sends `sendLocation` API request to the telegramAPI.

    chat_id: Id of the chat.
    lat: Latitude.
    lon: Longitude.
    token: bot's token

    Returns: None.
    """
    try:
        response: Message = TeleBot(token).send_location(
            chat_id=chat_id,
            longitude=lon,
            latitude=lat
        )
        return response
    except ApiException as e:
        print(f"LOGGING: {e}")
    except Exception as e:
        print(f"LOGGING: {e}")


def send_sticker(chat_id: int, token: str,
                 sticker_path: str = None,
                 sticker_id: str = None, **kwargs) -> Message:
    """Sends `sendSticker` API request to the telegramAPI.

    chat_id: Id of the chat.
    sticker_path: path to the sticker.
    sticker_id: id of the sticker
    token: bot's token

    Returns: None.
    """
    if not sticker_id and not sticker_path:
        # TODO change it after realization telegram stiker
        return

    try:
        if sticker_path:
            with open(sticker_path, 'rb') as file:
                TeleBot(token).send_sticker(
                    chat_id=chat_id, data=file
                )
        else:
            TeleBot(token).send_sticker(
                chat_id=chat_id, data=sticker_id
            )

    except ApiException as e:
        print(f"LOGGING: {e}")
    except Exception as e:
        print(f"LOGGING: {e}")


def delete_message(chat_id: Union[str, int], message_id: int,
                   token: str) -> None:
    """
    Delete message using Telegram API
    :param chat_id: Id of a chat.
    :param message_id: Id of a message.
    :param token: Bot`s token
    """
    try:
        TeleBot(token).delete_message(chat_id=chat_id, message_id=message_id)
    except ApiException as e:
        logger.warning(
            f"""Delete message {message_id} in {chat_id} failed.
                    token: {token}.
                    Error: {e}"""
        )
    except Exception as e:
        logger.warning(
            f"""Delete message with id {message_id} in {chat_id} failed.
                    token: {token}.
                    Error: {e}"""
        )


def set_webhook_ajax(slug: str, host: str, token: str) -> dict:
    """
    Sets telegram webhook for certain channel.
    """
    webhook = f"https://{host}/telegram_prod/{slug}/"
    url = f"https://api.telegram.org/bot{token}/setWebhook?url={webhook}"
    response = requests.get(url)
    logger.warning(
        f"""Set telegram-webhook with ajax {url}.
            token {token}. Answer: {response.text}"""
    )
    return response.json()


def unset_webhook_ajax(token: str) -> dict:
    """
    Sets telegram webhook for certain channel.
    """
    webhook = ""
    url = f"https://api.telegram.org/bot{token}/setWebhook?url={webhook}"
    response = requests.get(url)
    logger.warning(
        f"""Set telegram-webhook with ajax {url}.
            token {token}. Answer: {response.text}"""
    )
    return response.json()
