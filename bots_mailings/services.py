from typing import Union

from bots_mailings.models import Post, SentMessage
from keyboards.models import Action


#TODO: fix
def create_sent_message_object(
        chat_id: Union[int, str], message_id: str,
        action: Action, post: Post) -> None:
    """
    Create an object of SentMessage model
    """
    sent_post = SentMessage(
        chat_id=chat_id,
        message_id=message_id,
        post=post,
    )
    sent_post.save()
