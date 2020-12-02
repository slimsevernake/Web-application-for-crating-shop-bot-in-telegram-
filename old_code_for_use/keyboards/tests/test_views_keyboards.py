from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from bots_management.models import Channel
from old_code_for_use.keyboards import Keyboard


class KeyboardsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        Keyboard.objects.create(name="first_keyboard", channel=c1)
        Keyboard.objects.create(name="second_keyboard", channel=c1)
        Keyboard.objects.create(name="third_keyboard", channel=c1)
        Keyboard.objects.create(name="fourth_keyboard", channel=c1)

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/keyboards/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/keyboards/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/keyboards/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/keyboards/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-list",
            kwargs={'slug': "first_slug", }
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-list",
            kwargs={'slug': "first_slug", })
        )
        self.assertTemplateUsed(response, "keyboards/keyboard_list.html")

    def test_view_all_keyboards(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-list",
            kwargs={'slug': "first_slug", }))
        self.assertEqual(len(response.context['object_list']), 4)


class KeyboardDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create(
            username="moderator", password="1234"
        )

        c1 = Channel.objects.create(name="first", slug="first_slug")
        Keyboard.objects.create(id=1, name="first_keyboard", channel=c1)

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/keyboard/1/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/keyboard/1/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/keyboard/1/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/keyboard/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-detail",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-detail",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertTemplateUsed(
            response, "keyboards/keyboard_detail.html"
        )

    def test_view_detail_keyboard(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-detail",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertEqual(
            str(response.context["object"]),
            "Клавіатура: first_keyboard"
        )


class KeyboardUpdateViewTest(TestCase):
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

        Keyboard.objects.create(
            id=1, name="first_keyboard", channel=c1
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/keyboard_update/1/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/keyboard_update/1/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/keyboard_update/1/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/keyboard_update/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-update",
            kwargs={'slug': "first_slug", 'pk': 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-update",
            kwargs={'slug': "first_slug", 'pk': 1}
        ))
        self.assertTemplateUsed(
            response, "keyboards/keyboard_detail.html"
        )

    def test_view_update_keyboard(self):
        keyboard = Keyboard.objects.get(name="first_keyboard")
        c = Client()
        c.login(username="super", password="1234")
        response = c.post(reverse(
            "bots-management:keyboards:keyboard-update",
            kwargs={'slug': "first_slug", 'pk': 1}), {
            "name": "first_keyboard_edited",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/channel/first_slug/keyboard/1/"
        )
        keyboard.refresh_from_db()
        self.assertEqual(keyboard.name, "first_keyboard_edited")


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
        response = c.get(
            "/channel/first_slug/keyboard_create/"
        )
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(
            "/channel/first_slug/keyboard_create/"
        )
        self.assertEqual(
            response.url, "/login/?next=/channel/first_slug/keyboard_create/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/keyboard_create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-create",
            kwargs={'slug': "first_slug"}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-create",
            kwargs={'slug': "first_slug"}
        ))
        self.assertTemplateUsed(
            response, "keyboards/keyboard_create.html"
        )

    def test_view_create_keyboard(self):
        c = Client()
        c.login(username="super", password="1234")
        c.post(reverse(
            "bots-management:keyboards:keyboard-create",
            kwargs={'slug': "first_slug"}), {
            "name": "second_keyboard",
        })
        self.assertEqual(len(
            Keyboard.objects.filter(name="second_keyboard")
        ), 1)


class KeyboardDeleteViewTest(TestCase):
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

        Keyboard.objects.create(id=1, name="first_keyboard", channel=c1)

    def test_login_required(self):
        c = Client()
        response = c.get("/channel/first_slug/keyboard_delete/1/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/channel/first_slug/keyboard_delete/1/")
        self.assertEqual(
            response.url,
            "/login/?next=/channel/first_slug/keyboard_delete/1/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/channel/first_slug/keyboard_delete/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-delete",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse(
            "bots-management:keyboards:keyboard-delete",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertTemplateUsed(response, "keyboards/keyboard_delete.html")

    def test_view_delete_keyboard(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.post(reverse(
            "bots-management:keyboards:keyboard-delete",
            kwargs={'slug': "first_slug", "pk": 1}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/channel/first_slug/keyboards/")
        self.assertEqual(list(Keyboard.objects.filter(pk=1)), list())
