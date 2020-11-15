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
from keyboards.models import Action


logger = logging.getLogger(__name__)


def send_action_to_telegram_user(
        chat_id: int, action: Action, post: Post) -> None:
    """
    Parse action due to it`s type
    and send message with provided content to chat_id
    """
    token = post.channel.telegram_token
    if not action.action_type == "text":

        if action.action_type == "picture" and action.picture:
            response: Message = tg_send_photo(
                chat_id=chat_id,
                file_path=action.picture.path,
                token=token
            )
            create_sent_message_object(
                chat_id=response.chat.id,
                message_id=response.message_id,
                post=post,
                action=action
            )

        elif action.action_type == "url" and action.url:
            response: Message = tg_send_message(
                chat_id=chat_id,
                text=action.url,
                token=token
            )
            create_sent_message_object(
                chat_id=response.chat.id,
                message_id=response.message_id,
                post=post,
                action=action
            )
        elif action.action_type == "video" and action.video:
            response: Message = tg_send_video(
                chat_id=chat_id,
                file_path=action.video.path,
                token=token
            )
            create_sent_message_object(
                chat_id=response.chat.id,
                message_id=response.message_id,
                post=post,
                action=action
            )
        elif action.action_type == "file" and action.file:
            response: Message = tg_send_document(
                chat_id=chat_id,
                file_path=action.file.path,
                token=token
            )
            create_sent_message_object(
                chat_id=response.chat.id,
                message_id=response.message_id,
                post=post,
                action=action
            )
        elif all([action.action_type == "location",
                  action.location_latitude,
                  action.location_longitude]):
            response: Message = tg_send_location(
                chat_id=chat_id,
                lon=int(action.location_longitude),
                lat=int(action.location_latitude),
                token=token
            )
            create_sent_message_object(
                chat_id=response.chat.id,
                message_id=response.message_id,
                post=post,
                action=action
            )
        elif action.action_type == "sticker" and action.sticker_id:
            data = action.sticker_id
            response: Message = tg_send_sticker(
                chat_id=chat_id,
                sticker_id=data,
                token=token
            )
            create_sent_message_object(
                chat_id=response.chat.id,
                message_id=response.message_id,
                post=post,
                action=action
            )
    response: Message = tg_send_message(
        chat_id=chat_id,
        text=action.text,
        token=token
    )
    create_sent_message_object(
        chat_id=response.chat.id,
        message_id=response.message_id,
        post=post,
        action=action
    )


def send_action_to_telegram_users(
        subscriber_list: list, action: Action, post: Post) -> None:
    """
    Send action to all telegram subscribers in subscriber_list
    """
    for subscriber in subscriber_list:
        send_action_to_telegram_user(
            chat_id=subscriber.user_id,
            action=action,
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
