from typing import Union

from django.db import ProgrammingError
from django.db.models import Q, QuerySet, Count

from bots_management.models import Bot
from .models import Subscriber, Message, Reply


def get_subscriber(uid: str, bot: Bot) -> Union[Subscriber, None]:
    return Subscriber.objects.filter(
        Q(user_id=uid) & Q(bot=bot)
    ).first()


def get_subscriber_telegram(user: dict,
                            bot: Bot) -> Union[Subscriber, None]:
    username = user.get('username')
    if not username:
        username = user.get('first_name')
    return Subscriber.objects.update_or_create(
        user_id=user.get('id'),
        bot=bot,
        defaults={
            'user_id': user.get('id'),
            'name': username,
            'is_active': True,
            'bot': bot,
        }
    )


def get_all_active_subs(bot: Bot) -> QuerySet:
    return Subscriber.objects.filter(
        is_active=True, bot=bot
    )


def get_subscribers_of_bot(slug: str) -> QuerySet:
    return Subscriber.objects.filter(messengers_bot__channel__slug=slug)


def get_status_subscribers_of_bot(
        slug: str, messenger: str = 'all',
        status: str = 'all') -> QuerySet:
    subscribers = get_subscribers_of_bot(slug)
    if status != 'all':
        if status == 'active':
            subscribers = subscribers.filter(is_active=True)
        elif status == 'not_active':
            subscribers = subscribers.filter(is_active=True)
    return subscribers


def get_num_of_subs(bot: Bot) -> int:
    try:
        result = get_all_active_subs(bot).aggregate(
            Count('id')
        )["id__count"]
        return result
    except ProgrammingError:
        return 0


def get_num_of_subs_to_bot(bot: Bot, messenger: str) -> int:
    try:
        result = get_all_active_subs(bot).filter(
            messengers_bot__messenger=messenger
        ).aggregate(Count('id'))["id__count"]
        return result
    except ProgrammingError:
        return 0


def get_messages_subscribers_of_bot(slug: str) -> QuerySet:
    messages = Message.objects.filter(
        sender__in=get_subscribers_of_bot(slug)
    )
    return messages.order_by('-id')


def get_all_help_messages(slug: str) -> QuerySet:
    """
    Returns all messages, asking for help
    """
    return Message.objects.filter(
        is_help_message=True,
        sender__bot__slug=slug,
    )


def get_all_active_help_messages(slug: str) -> QuerySet:
    """
    Returns all active messages, asking for help
    """
    return Message.objects.filter(
        is_help_message=True,
        sender__bot__slug=slug,
        help_reply__is_started=False,
        help_reply__is_closed=False
    )


def get_all_started_help_messages(slug: str) -> QuerySet:
    """
    Returns all started messages, asking for help
    """
    return Message.objects.filter(
        is_help_message=True,
        sender__bot__slug=slug,
        help_reply__is_started=True,
        help_reply__is_closed=False
    )


def get_all_closed_help_messages(slug: str) -> QuerySet:
    """
    Returns all closed messages, asking for help
    """
    return Message.objects.filter(
        is_help_message=True,
        sender__messengers_bot__channel__slug=slug,
        help_reply__is_closed=True
    )


def get_help_message_reply(pk: int) -> Union[Reply, None]:
    return Reply.objects.filter(pk=pk).first()
