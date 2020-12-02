import logging

from time import sleep

from telebot.types import Message

from telegram_api.api import (
    send_photo as tg_send_photo,
    send_message as tg_send_message,
    send_video as tg_send_video,
    send_document as tg_send_document,
    send_location as tg_send_location,
    send_sticker as tg_send_sticker,
    delete_message as tg_delete_message
)
from bots_mailings.models import Post, SentMessage
from bots_mailings.services import create_sent_message_object


logger = logging.getLogger(__name__)


def send_action_to_telegram_user(
        chat_id: int, ac, post: Post) -> None:
    """
    Parse action due to it`s type
    and send message with provided content to chat_id
    """
    pass

def send_action_to_telegram_users(
        subscriber_list: list, post: Post) -> None:
    """
    Send action to all telegram subscribers in subscriber_list
    """
    for subscriber in subscriber_list:
        send_action_to_telegram_user(
            chat_id=subscriber.user_id,
            post=post
        )

        # Telegram API will not allow send more than 30 messages per second
        # to bypass blocking sleep thread for 0.5 secs
        # TODO: try to find more efficient way to bypass blocking
        sleep(0.1)


def delete_telegram_messages(messages: SentMessage):
    """
    Delete all messages of the post in Telegram
    """
    for message in messages:
        tg_delete_message(
            chat_id=message.chat_id,
            message_id=message.message_id,
            token=message.post.channel.telegram_token
        )
        # Telegram API will not allow send more than 30 messages per second
        # to bypass blocking sleep thread for 0.5 secs
        # TODO: try to find more efficient way to bypass blocking
        sleep(0.1)
