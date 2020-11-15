from django.test import TestCase
import json

from bots_management.models import Bot, Channel
from bots_management.services import (
    get_channel_by_slug,
    get_all_available_channels_to_moderator,
    get_moderators_to_json,
    get_all_bots,
    get_all_related_bots,
    get_bot_to_channel
)

from django.contrib.auth import get_user_model


class ChannelsTestCase(TestCase):

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(username="super")
        u = get_user_model().objects.create_user(username="notsuper")
        Channel.objects.create(name="first", slug="first_slug")

        c2 = Channel.objects.create(name="second", slug="second_slug")
        c2.moderators.add(u)

    def test_get_channel_by_slug(self):
        c1 = Channel.objects.get(slug="first_slug")
        c2 = Channel.objects.get(slug="second_slug")
        self.assertEqual(c1, get_channel_by_slug("first_slug"))
        self.assertEqual(c2, get_channel_by_slug("second_slug"))

    def test_get_all_available_channels_to_moderator(self):
        us = get_user_model().objects.get(username="super")
        u = get_user_model().objects.get(username="notsuper")

        self.assertEqual(
            list(Channel.objects.all()),
            list(get_all_available_channels_to_moderator(us))
        )
        self.assertEqual(
            list((Channel.objects.filter(name="second"))),
            list((get_all_available_channels_to_moderator(u)))
        )

    def test_get_moderators_to_json(self):
        # Find all auth users, does not check if the moderator
        moderators = get_user_model().objects.all()
        moderators = [
            {'name': moderator.username, 'id': moderator.id}
            for moderator in moderators
        ]
        self.assertEqual(json.dumps(moderators), get_moderators_to_json())


class BotsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        c1 = Channel.objects.create(name="first", slug="first_slug")
        c2 = Channel.objects.create(name="second", slug="second_slug")
        b1t = Bot.objects.create(messenger="telegram", channel=c1, token='1t')
        b1v = Bot.objects.create(messenger="viber", channel=c1, token='1v')
        b2t = Bot.objects.create(messenger="telegram", channel=c2, token='2t')
        b2v = Bot.objects.create(messenger="viber", channel=c2, token='2v')

    def test_get_all_bots(self):
        self.assertEqual(list(Bot.objects.all()), list(get_all_bots()))

    def test_get_all_related_bots(self):
        c1 = Channel.objects.get(slug="first_slug")
        b1 = Bot.objects.filter(channel=c1)

        self.assertEqual(list(b1), list(get_all_related_bots(c1)))

        c2 = Channel.objects.get(slug="second_slug")
        b2 = Bot.objects.filter(channel=c2)

        self.assertEqual(list(b2), list(get_all_related_bots(c2)))

    def test_get_bot_to_channel(self):
        c1 = Channel.objects.get(slug="first_slug")
        b1t = Bot.objects.get(channel=c1, messenger="telegram")

        self.assertEqual(b1t, get_bot_to_channel("first_slug", "telegram"))

        c2 = Channel.objects.get(slug="second_slug")
        b2v = Bot.objects.get(channel=c2, messenger="viber")

        self.assertEqual(b2v, get_bot_to_channel("second_slug", "viber"))
