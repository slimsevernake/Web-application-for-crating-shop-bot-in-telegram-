from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from bots_management.models import Channel, Bot


class BotCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create_user(
            username="moderator", password="1234", is_superuser=False
        )

        c1 = Channel.objects.create(
            name="first", slug="first_slug"
        )
        Bot.objects.create(
            messenger="telegram", channel=c1, token='1t'
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/bot_create/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/bot_create/")
        self.assertEqual(response.status_code, 403)

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/bot_create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:bot-create",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:bot-create",
                    kwargs={'slug': "first_slug", })
        )
        self.assertTemplateUsed(response, "bots_management/bot_add.html")

    def test_view_create_bot(self):
        c = Client()
        c.login(username="super", password="1234")
        self.assertEqual(len(Bot.objects.filter(messenger="viber")), 0)
        c.post(reverse(
            "bots-management:bot-create",
            kwargs={'slug': "first_slug", }), {
                "messenger": "viber",
                "token": "1v111132",
                "channel": Channel.objects.get(slug="first_slug"),
             }
        )
        self.assertEqual(len(Bot.objects.filter(messenger="viber")), 1)


class BotUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create_superuser(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        c1.moderators.add(moder)

        Channel.objects.create(name="second", slug="second_slug")
        c1.moderators.add(moder)

        Bot.objects.create(id=1, messenger="telegram", channel=c1, token='1t')
        Bot.objects.create(id=2, messenger="viber", channel=c1, token='1v')

    def test_login_required(self):
        c = Client()
        bpk = Bot.objects.get(token="1t").pk
        response = c.get("/channel/first_slug/bot_update/{}/".format(bpk))
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        bpk = Bot.objects.get(token="1t").pk
        # TODO fix this we cannot be allowed to edit
        #  the bot through another channel
        response = c.get(f"/channel/second_slug/bot_update/{bpk}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        bpk = Bot.objects.get(token="1t").pk
        response = c.get("/channel/first_slug/bot_update/{}/".format(bpk))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        bpk = Bot.objects.get(token="1t").pk
        response = c.get(reverse(
            "bots-management:bot-update",
            kwargs={'slug': "first_slug", 'pk': bpk, }
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        bpk = Bot.objects.get(token="1t").pk
        response = c.get(reverse(
            "bots-management:bot-update",
            kwargs={'slug': "first_slug", 'pk': bpk, }
        ))
        self.assertTemplateUsed(response, "bots_management/bot_update.html")

    def test_view_update_bot(self):
        c = Client()
        c.login(username="super", password="1234")
        b = Bot.objects.get(token="1t")
        response = c.post(reverse(
            "bots-management:bot-update",
            kwargs={'slug': "second_slug", 'pk': b.id, }), {
                "token": "1t_edited",
                "messenger": "telegram",
            }
        )
        self.assertEqual(response.status_code, 302)

        b.refresh_from_db()
        self.assertEqual(b.token, "1t_edited")
