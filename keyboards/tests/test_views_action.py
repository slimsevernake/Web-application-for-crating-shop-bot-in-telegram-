from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from bots_management.models import Channel
from keyboards.models import Keyboard, Action


class ActionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        c1.moderators.add(moder)

        Channel.objects.create(name="second", slug="second_slug")

        k = Keyboard.objects.create(name="first_keyboard", channel=c1)
        Action.objects.create(
            name="first_action",
            keyboard_to_represent=k
        )
        Action.objects.create(
            name="second_action",
            keyboard_to_represent=k
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/actions/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/actions/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/actions/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/actions/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-list",
            kwargs={'slug': "first_slug", }
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-list",
            kwargs={'slug': "first_slug", }
        ))
        self.assertTemplateUsed(
            response, "keyboards/action_list.html"
        )

    def test_view_all_keyboards(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-list",
            kwargs={'slug': "first_slug", }
        ))
        self.assertEqual(len(response.context['object_list']), 2)


class ActionDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        c1.moderators.add(moder)

        Channel.objects.create(name="second", slug="second_slug")

        k = Keyboard.objects.create(id=1, name="first_keyboard", channel=c1)
        Action.objects.create(
            id=1, name="first_action",
            keyboard_to_represent=k
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/action/1/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/action/1/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/action/1/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/action/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-detail",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-detail",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertTemplateUsed(response, "keyboards/action_detail.html")

    def test_view_detail_keyboard(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-detail",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertEqual(
            str(response.context["object"]),
            "Подія: first_action"
        )


class KeyboardCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        c1.moderators.add(moder)

        Channel.objects.create(name="second", slug="second_slug")

        Keyboard.objects.create(name="first_keyboard", channel=c1)

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/action_create/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/action_create/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/action_create/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/action_create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-create",
            kwargs={'slug': "first_slug"}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-create",
            kwargs={'slug': "first_slug"}
        ))
        self.assertTemplateUsed(response, "keyboards/action_create.html")


class ActionUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        c1.moderators.add(moder)

        Channel.objects.create(name="second", slug="second_slug")

        k = Keyboard.objects.create(
            id=1, name="first_keyboard",
            channel=c1
        )
        Action.objects.create(
            id=1, name="first_action",
            keyboard_to_represent=k
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/action_update/1/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/action_update/1/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/action_update/1/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/action_update/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-update",
            kwargs={'slug': "first_slug", 'pk': 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-update",
            kwargs={'slug': "first_slug", 'pk': 1}
        ))
        self.assertTemplateUsed(response, "keyboards/action_update.html")


class ActionDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        c1.moderators.add(moder)

        Channel.objects.create(name="second", slug="second_slug")

        k = Keyboard.objects.create(
            id=1, name="first_keyboard", channel=c1
        )
        Action.objects.create(
            id=1, name="first_action",
            keyboard_to_represent=k
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/action_delete/1/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/action_delete/1/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/action_delete/1/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/action_delete/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-delete",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:action-delete",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertTemplateUsed(response, "keyboards/action_delete.html")

    def test_view_delete_keyboard(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.post(reverse(
            "bots-management:keyboards:action-delete",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/channel/first_slug/actions/")
        self.assertEqual(list(Action.objects.filter(pk=1)), list())
