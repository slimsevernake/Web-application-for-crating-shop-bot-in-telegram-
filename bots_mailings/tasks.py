import logging

from celery import shared_task
from django.db.models import QuerySet

from bots_mailings.models import Post
from bots_mailings.utils import (
    send_action_to_telegram_users,
    delete_telegram_messages
)
from subscribers.services import (
    get_all_active_subs
)
logger = logging.getLogger(__name__)


@shared_task
def send_mailing(post_id: int) -> None:
    """
    Celery task for sending a mailing to a user/group of users
    """

    # try:
    #     # Moderator can delete post model before this function starts
    #     post: Post = Post.objects.get(id=post_id)
    # except Post.DoesNotExist as e:
    #     logger.info(e)
    #     return
    #
    # receivers: QuerySet = post.send_to.all()
    # if not receivers:
    #     receivers: QuerySet = get_all_active_subs(bot=post.bot)
    #
    # telegram_users: list = []
    # viber_users: list = []
    # [telegram_users.append(receiver) if is_telegram_subscriber(receiver)
    #  else viber_users.append(receiver) for receiver in receivers]
    #
    # for action in post.actions.all():
    #     send_action_to_telegram_users(
    #         subscriber_list=telegram_users,
    #         action=action,
    #         post=post
    #     )
    #
    # post.is_done = True
    # post.save()
    pass


@shared_task
def delete_mailing(post_id: int) -> None:
    """
        Celery task for deleting a mailing to a user/group of users
    """
    # try:
    #     print(post_id)
    #     post: Post = Post.objects.get(id=post_id)
    # except Post.DoesNotExist as e:
    #     logger.info(e)
    #     return
    #
    # delete_telegram_messages(post.sent_messages.all())
    pass