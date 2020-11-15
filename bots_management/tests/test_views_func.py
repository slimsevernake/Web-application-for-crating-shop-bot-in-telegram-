from django.test import TestCase
from django.test import Client

from django.urls import reverse
from django.contrib.auth import get_user_model

from bots_management.models import Channel


class FuncTestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )

        Channel.objects.create(name="first", slug="first_slug")
        Channel.objects.create(name="second", slug="second_slug")
        Channel.objects.create(name="third", slug="third_slug")
        Channel.objects.create(name="fourth", slug="fourth_slug")

    def test_root_view(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("bots-management:root"))
        self.assertEqual(response.url, "/channels/")

    def test_notfound_view(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/sadsadsadsadsad/")
        self.assertEqual(response.url, "/channels/")
