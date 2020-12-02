from django.test import TestCase

from old_code_for_use.keyboards import Keyboard, Action
from bots_management.models import Channel

from old_code_for_use.keyboards import (
    get_home_action,
    get_emergency_action,
)


class ServicesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        c1 = Channel.objects.create(name="first", slug="first_slug")
        Keyboard.objects.create(name="first_keyboard1", channel=c1)
        Keyboard.objects.create(name="second_keyboard1", channel=c1)

        c2 = Channel.objects.create(name="second", slug="second_slug")
        k = Keyboard.objects.create(name="first_keyboard2", channel=c2)
        Action.objects.create(name="first_action", keyboard_to_represent=k)
        Action.objects.create(name="second_action", keyboard_to_represent=k)

    def test_get_home_action(self):
        action1 = Action.objects.get(name="first_action")
        self.assertEqual(get_home_action("second_slug"), action1)
        c2 = Channel.objects.get(slug="second_slug")
        action2 = Action.objects.get(name="second_action")
        c2.welcome_action = action2
        c2.save()
        self.assertEqual(get_home_action("second_slug"), action2)

    def test_get_emergency_action(self):
        self.assertEqual(get_emergency_action("second_slug"), None)
        k = Keyboard.objects.get(name="first_keyboard2")
        action = Action.objects.create(
            name="emergency_action",
            keyboard_to_represent=k
        )
        self.assertEqual(get_home_action("second_slug"), action)
