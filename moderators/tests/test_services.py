from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

from moderators.services import generate_password, change_user_password


class ServicesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )

    def test_generate_password(self):
        password = generate_password()
        self.assertEqual(len(password), 8)
        self.assertEqual(type(password), type(""))

    def test_change_user_password(self):
        u = get_user_model().objects.get(username="super")
        change_user_password(user=u, password="abc")
        user = authenticate(username="super", password="abc")
        self.assertNotEqual(user, None)
