from django.test import TestCase

from django.urls import reverse

from bots_management.models import Channel, Bot


class BotTestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        c1 = Channel.objects.create(name="first", slug="first_slug")
        Bot.objects.create(messenger="telegram", channel=c1, token='1t')
        Bot.objects.create(messenger="viber", channel=c1, token='1v')

    def test_get_update_url(self):
        b = Bot.objects.get(token="1t")
        url = b.get_update_url()
        self.assertEqual(url, "/channel/first_slug/bot_update/1/")


class ChannelTestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        c1 = Channel.objects.create(name="first", slug="first_slug")
        Bot.objects.create(messenger="telegram", channel=c1, token='1t')
        Bot.objects.create(messenger="viber", channel=c1, token='1v')

    def test_str(self):
        c = Channel.objects.get(slug="first_slug")
        url = c.__str__()
        self.assertEqual(url, "first")

    def test_get_absolute_url(self):
        c = Channel.objects.get(slug="first_slug")
        url = c.get_absolute_url()
        self.assertEqual(url, reverse(
            "bots-management:channel-detail", kwargs={"slug": "first_slug"}
        ))

    def test_get_full_detail_url(self):
        c = Channel.objects.get(slug="first_slug")
        url = c.get_full_detail_url()
        self.assertEqual(url, reverse(
            "bots-management:channel-full-detail",
            kwargs={"slug": "first_slug"}
        ))
        self.assertEqual(url, reverse(
            "bots-management:channel-full-detail",
            kwargs={"slug": "first_slug"},
        ))

    def test_get_update_url(self):
        c = Channel.objects.get(slug="first_slug")
        url = c.get_update_url()
        self.assertEqual(url, reverse(
            "bots-management:channel-update", kwargs={"slug": "first_slug"}
        ))

    def test_get_delete_url(self):
        c = Channel.objects.get(slug="first_slug")
        url = c.get_delete_url()
        self.assertEqual(url, reverse(
            "bots-management:channel-delete", kwargs={"slug": "first_slug"}
        ))

    def test_viber_token(self):
        c = Channel.objects.get(slug="first_slug")
        viber_token = c.viber_token
        self.assertEqual(viber_token, "1v")

    def test_viber_bot(self):
        c = Channel.objects.get(slug="first_slug")
        viber_bot = Bot.objects.get(messenger="viber")
        viber_func_bot = c.viber_bot
        self.assertEqual(viber_bot, viber_func_bot)

    def test_telegram_token(self):
        c = Channel.objects.get(slug="first_slug")
        telegram_token = c.telegram_token
        self.assertEqual(telegram_token, "1t")

    def test_telegram_bot(self):
        c = Channel.objects.get(slug="first_slug")
        telegram_bot = Bot.objects.get(messenger="telegram")
        telegram_func_bot = c.telegram_bot
        self.assertEqual(telegram_bot, telegram_func_bot)
