from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from bots_management.models import Channel
from keyboards.models import Keyboard, Action, Button


class ButtonUpdateViewTest(TestCase):
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
        a1 = Action.objects.create(
            name="first_action", keyboard_to_represent=k
        )
        a2 = Action.objects.create(
            name="second_action", keyboard_to_represent=k
        )
        Button.objects.create(
            id=1, keyboard=k, action=a1,
            name="first_button", text="1", position=1
        )
        Button.objects.create(
            id=2, keyboard=k, action=a2,
            name="second_button", text="2", position=2
        )

    def test_login_required(self):
        c = Client()
        response = c.get(
            "/channel/first_slug/keyboard/1/button_update/1/"
        )
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(
            "/channel/first_slug/keyboard/1/button_update/1/"
        )
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/keyboard/1/button_update/1/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            "/channel/first_slug/keyboard/1/button_update/1/"
        )
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:button-update",
            kwargs={'slug': "first_slug", 'pk': 1, 'pk_button': 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/keyboard/1/button_update/1/")
        self.assertTemplateUsed(response, "keyboards/button_update.html")


class ButtonDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        moder = get_user_model().objects.create(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(
            name="first", slug="first_slug"
        )
        c1.moderators.add(moder)

        Channel.objects.create(
            name="second", slug="second_slug"
        )

        k = Keyboard.objects.create(
            id=1, name="first_keyboard", channel=c1
        )
        a1 = Action.objects.create(
            id=1, name="first_action", keyboard_to_represent=k
        )
        a2 = Action.objects.create(
            id=2, name="second_action", keyboard_to_represent=k
        )
        Button.objects.create(
            id=1, keyboard=k, action=a1,
            name="first_button", text="1", position=1
        )
        Button.objects.create(
            id=2, keyboard=k, action=a2,
            name="second_button", text="2", position=2
        )

    def test_login_required(self):
        c = Client()
        response = c.get(
            "/channel/first_slug/keyboard/1/button_delete/1/"
        )
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(
            "/channel/first_slug/keyboard/1/button_delete/1/"
        )
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/keyboard/1/button_delete/1/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(
            "/channel/first_slug/keyboard/1/button_delete/1/"
        )
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:button-delete",
            kwargs={'slug': "first_slug", 'pk': 1, 'pk_button': 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:button-delete",
            kwargs={'slug': "first_slug", 'pk': 1, 'pk_button': 1}
        ))
        self.assertTemplateUsed(response, "keyboards/button_delete.html")

    def test_view_delete_keyboard(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.post(reverse(
            "bots-management:keyboards:button-delete",
            kwargs={'slug': "first_slug", "pk": 1, 'pk_button': 1}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/channel/first_slug/keyboard/1/")
        self.assertEqual(list(Button.objects.filter(pk=1)), list())
