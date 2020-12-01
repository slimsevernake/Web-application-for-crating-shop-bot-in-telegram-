import json
from typing import Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from django.forms import model_to_dict
from django.contrib.auth.models import User

from .models import Bot


def get_bot_by_slug(slug: str) -> Union[Bot, None]:
    """
    Find and return bot using slug
    """
    return Bot.objects.filter(slug=slug).first()


def get_all_available_bots_to_moderator(user: User) -> QuerySet:
    """
    Returns all available bots to moderator.
    """
    return user.bots_to_management.all()


def get_all_users_bots(user: User) -> QuerySet:
    """
    Returns all available channels to moderator.
    """
    return user.bots.all()


def get_all_bots() -> QuerySet:
    """
    Return all existed bots
    """
    return Bot.objects.all()


# TODO add filter for moderators
def get_bots_to_json() -> json:  # it returns str btw
    bots = Bot.objects.all().select_related()
    bots = [model_to_dict(bot) for bot in bots]
    for bot in bots:
        bot['moderators'] = [
            model_to_dict(moderator).get('username')
            for moderator in bot['moderators']
        ]
    return json.dumps(bots)


# TODO find a better solution
def extract_data(request):
    tmp = request.POST.dict()
    for key, value in tmp.items():
        if value == 'true':
            tmp[key] = True
        if value == 'false':
            tmp[key] = False
    return tmp


def get_moderators_to_json() -> json:   # it returns str btw
    moderators = get_user_model().objects.all()
    moderators = [{'name': moderator.username,
                   'id': moderator.id} for moderator in moderators]
    return json.dumps(moderators)
