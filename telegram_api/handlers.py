# import logging
# from typing import Union
#
# from django.conf import settings
# from django.db.models import QuerySet
#
# from keyboards.models import Action, Keyboard
# from keyboards.services import (
#     get_button_and_joined_action, get_home_action,
#     get_emergency_action, get_action_by_name
# )
# from bots_management.services import get_channel_by_slug
# from .api import (
#     send_message, send_photo,
#     send_video, send_document,
#     send_location, send_sticker
# )
# from .utils import create_markup, save_message
# from subscribers.services import get_subscriber_telegram
#
#
# logger = logging.getLogger(__name__)
#
#
def event_handler_tg(incoming_data: dict, channel_slug: str) -> None:
    pass
#     if incoming_data.get('edited_message'):
#         # TODO now we don't do anything with it
#         return
#     channel = get_channel_by_slug(slug=channel_slug)
#     message = incoming_data["message"]
#     if message:
#         if 'text' in message:
#             if message.get("text") == "/start":
#                 subscribed_handler(
#                     in_data=incoming_data, channel=channel
#                 )
#             elif message.get("text").startswith("/"):
#                 sys_action_handler(
#                     in_data=incoming_data, channel_slug=channel_slug
#                 )
#             else:
#                 action_handler(
#                     in_data=incoming_data, channel_slug=channel_slug
#                 )
#         if settings.SAVE_MESSAGE:
#             save_message(channel=channel, in_data=incoming_data)
#
#
def action_handler(in_data: dict, channel_slug: str) -> None:
    pass

#     user_text: str = in_data["message"]["text"]
#     tag: QuerySet = get_button_and_joined_action(user_text,
#                                                  channel_slug=channel_slug)
#     actions = get_action_by_name(user_text, channel_slug=channel_slug)
#     if tag.exists():
#         action: Action = tag.first().action
#     elif actions.exists():
#         action = actions.first()
#     else:
#         # TODO maybe we can think of something
#         #  more interesting on on not expected actions
#         action: Action = get_home_action(slug=channel_slug)
#
#     keyboard: Keyboard = action.keyboard_to_represent
#     action_type: str = action.action_type
#
#     if action_type != "text":
#         if action_type == "picture" and action.picture:
#             send_photo(
#                 chat_id=in_data["message"]["chat"]["id"],
#                 file_path=action.picture.path,
#                 token=keyboard.channel.telegram_token,
#                 action=action,
#             )
#         elif action_type == "url" and action.url:
#             send_message(
#                 chat_id=in_data["message"]["chat"]["id"],
#                 text=action.url,
#                 token=keyboard.channel.telegram_token
#             )
#         elif action_type == "video" and action.video:
#             send_video(
#                 chat_id=in_data["message"]["chat"]["id"],
#                 file_path=action.video.path,
#                 token=keyboard.channel.telegram_token,
#                 action=action,
#             )
#         elif action_type == "file" and action.file:
#             send_document(
#                 chat_id=in_data["message"]["chat"]["id"],
#                 file_path=action.file.path,
#                 token=keyboard.channel.telegram_token,
#                 action=action,
#             )
#         elif all([action_type == "location",
#                   action.location_latitude,
#                   action.location_longitude]):
#             send_location(
#                 chat_id=in_data["message"]["chat"]["id"],
#                 lon=float(action.location_longitude),
#                 lat=float(action.location_latitude),
#                 token=keyboard.channel.telegram_token
#             )
#         elif action_type == "sticker" and action.sticker_id:
#             data = action.sticker_id
#             send_sticker(
#                 chat_id=in_data["message"]["chat"]["id"],
#                 file_path=data,
#                 token=keyboard.channel.telegram_token
#             )
#     send_message(
#         chat_id=in_data["message"]["chat"]["id"],
#         text=action.text,
#         reply_markup=create_markup(action),
#         token=keyboard.channel.telegram_token
#     )
#
#
def help_message_handler(in_data: dict, channel_slug: str) -> None:
    pass

#     """
#     Sends message to user, that his help message was sent and
#     moderator will contact him
#     """
#     # TODO create help message and send notification to moderator
#
#     action: Union[Action, None] = get_emergency_action(
#         channel_slug=channel_slug
#     )
#
#     if not action:
#         action: Action = get_home_action(slug=channel_slug)
#
#     keyboard: Keyboard = action.keyboard_to_represent
#
#     send_message(
#         chat_id=in_data["message"]["chat"]["id"],
#         text=action.text,
#         reply_markup=create_markup(action),
#         token=keyboard.channel.telegram_token
#     )
#
#
def sys_action_handler(in_data: dict, channel_slug: str) -> None:
    pass

#     if in_data["message"]["text"][:5].upper() == "/HELP":
#         help_message_handler(in_data=in_data, channel_slug=channel_slug)
#         save_message(channel=get_channel_by_slug(channel_slug),
#                      in_data=in_data,
#                      is_help_message=True)
#     # TODO if other system commands add elif
#     else:
#         action: Action = get_home_action(slug=channel_slug)
#         keyboard: Keyboard = action.keyboard_to_represent
#         send_message(
#             chat_id=in_data["message"]["chat"]["id"],
#             text=action.text,
#             reply_markup=create_markup(action),
#             token=keyboard.channel.telegram_token
#         )
#
#
def subscribed_handler(in_data: dict, channel: object) -> None:
    pass

#     start_action = channel.welcome_action
#     if start_action:
#         text: str = start_action.text
#     else:
#         text = 'No welcome action'
#     # TODO what about a 'is_bot': True?
#     user = in_data.get('message').get('chat')
#     # TODO id_user or id_chat? now i save id_chat (how sent)
#     subscraber, created = get_subscriber_telegram(user, channel)
#     logger.warning(
#         f"""Subscraber {subscraber} create new {created} (False=update)"""
#     )
#     # TODO next create welcome action > not only text message
#     send_message(
#         chat_id=subscraber.user_id,
#         text=text,
#         reply_markup=create_markup(start_action),
#         token=channel.telegram_token
#     )
#
#
# # TODO
# # we can't receive information, that user unsubscribe
# # Only by getting an error while sending user something
#
# # def unsubscribed_handler(in_data: dict, channel_slug: str) -> None:
# #     # TODO log that unsubscribed and
# #     #  Subscriber.object.get(uid=uid).is_active=False
# #     print(in_data)
# #     pass
