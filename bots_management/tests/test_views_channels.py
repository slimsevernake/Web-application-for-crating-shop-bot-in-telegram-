from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from bots_management.models import Channel, Bot


class ChannelListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create_user(
            username="moderator", password="1234", is_superuser=False
        )

        Channel.objects.create(name="first", slug="first_slug")
        Channel.objects.create(name="second", slug="second_slug")
        Channel.objects.create(name="third", slug="third_slug")
        Channel.objects.create(name="fourth", slug="fourth_slug")

    def test_login_required(self):
        c = Client()
        response = c.get("/channels/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/")
        self.assertEqual(response.status_code, 403)

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channels/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get('/channel/first_slug/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("bots-management:channel-list"))
        self.assertTemplateUsed(
            response, "bots_management/channel_list.html"
        )

    def test_view_all_channels(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("bots-management:channel-list"))
        self.assertEqual(len(response.context['channel_list']), 4)


class ChannelDetailViewTest(TestCase):
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

        Bot.objects.create(messenger="telegram", channel=c1, token='1t')
        Bot.objects.create(messenger="viber", channel=c1, token='1v')

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-detail",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-detail",
                    kwargs={'slug': "first_slug", })
        )
        self.assertTemplateUsed(
            response, "bots_management/channel_details.html"
        )

    def test_view_detail_channel(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-detail",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(
            response.context["channel"].slug, "first_slug"
        )

    def test_view_detail_channels_bots(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-detail",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(len(response.context["bots"]), 2)


class ChannelFullDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create_user(
            username="moderator", password="1234", is_superuser=False,
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        c1.moderators.add(moder)

        Bot.objects.create(messenger="telegram", channel=c1, token='1t')
        Bot.objects.create(messenger="viber", channel=c1, token='1v')

    def test_login_required(self):
        response = self.client.get("/channel_full/first_slug/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel_full/first_slug/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel_full/first_slug/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-full-detail",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-full-detail",
                    kwargs={'slug': "first_slug", })
        )
        self.assertTemplateUsed(
            response, "bots_management/channel_details.html"
        )

    def test_view_detail_channel(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-full-detail",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(
            response.context["channel"].slug, "first_slug"
        )

    def test_view_detail_channels_bots(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-full-detail",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(len(response.context["bots"]), 2)


class ChannelCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create_user(
            username="moderator", password="1234", is_superuser=False
        )

        Channel.objects.create(
            name="first", slug="first_slug"
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/channels_create/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel_create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel_create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-create")
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-create")
        )
        self.assertTemplateUsed(
            response, "bots_management/channel_add.html"
        )

    def test_view_create_channel(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.post(
            reverse("bots-management:channel-create"), {
                "name": "second",
                "slug": "second_slug",
                "moderators": [
                    get_user_model().objects.get(username="super")
                ],
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "second")
        self.assertContains(response, "second_slug")


class ChannelUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create_user(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        c1.moderators.add(moder)

        Channel.objects.create(name="second", slug="second_slug")

        Bot.objects.create(id=1, messenger="telegram", channel=c1, token='1t')
        Bot.objects.create(id=2, messenger="viber", channel=c1, token='1v')

    def test_login_required(self):
        c = Client()
        response = c.get("/channel_update/first_slug/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel_update/first_slug/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel_update/first_slug/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-update",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-update",
                    kwargs={'slug': "first_slug", })
        )
        self.assertTemplateUsed(
            response, "bots_management/channel_update.html"
        )

    def test_view_update_channels_bots(self):
        channel = Channel.objects.get(slug="second_slug")
        c = Client()
        c.login(username="super", password="1234")
        response = c.post(
            reverse("bots-management:channel-update",
                    kwargs={'slug': "second_slug", }), {
                        "name": "second_edit",
                        "slug": "second_slug_edit",
            }
        )
        self.assertEqual(response.status_code, 302)

        channel.refresh_from_db()
        self.assertEqual(channel.name, "second_edit")
        self.assertEqual(channel.slug, "second_slug_edit")


class ChannelDeleteViewTest(TestCase):
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

        Bot.objects.create(messenger="telegram", channel=c1, token='1t')
        Bot.objects.create(messenger="viber", channel=c1, token='1v')

    def test_login_required(self):
        c = Client()
        response = c.get("/channel_delete/first_slug/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel_delete/first_slug/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel_delete/first_slug/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-delete",
                    kwargs={'slug': "first_slug", })
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            reverse("bots-management:channel-delete",
                    kwargs={'slug': "first_slug", })
        )
        self.assertTemplateUsed(
            response, "bots_management/channel_delete.html"
        )

    def test_view_delete_channels_bots(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.post(
            reverse("bots-management:channel-delete",
                    kwargs={'slug': "second_slug", })
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(list(
            Channel.objects.filter(slug="second_slug")
        ), list())
