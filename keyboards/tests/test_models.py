from django.test import TestCase

from bots_management.models import Channel
from keyboards.models import Keyboard, Action, Button


class KeyboardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        c1 = Channel.objects.create(name="first", slug="first_slug")

        Channel.objects.create(name="second", slug="second_slug")

        k = Keyboard.objects.create(name="first_keyboard", channel=c1)
        a1 = Action.objects.create(
            name="first_action",
            keyboard_to_represent=k
        )
        a2 = Action.objects.create(
            name="second_action",
            keyboard_to_represent=k
        )
        Button.objects.create(
            keyboard=k, action=a1,
            name="first_button",
            text="1", position=1
        )
        Button.objects.create(
            keyboard=k, action=a2,
            name="second_button",
            text="2", position=2
        )

    def test_str_keyboard(self):
        k = Keyboard.objects.get(name="first_keyboard")
        self.assertEqual(str(k), "Клавіатура: first_keyboard")

    def test_get_sorted_by_position_buttons_list(self):
        k = Keyboard.objects.get(name="first_keyboard")
        self.assertEqual(
            k.get_sorted_by_position_buttons_list(),
            list(Button.objects.filter(keyboard=k))
        )


class ActionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        c1 = Channel.objects.create(name="first", slug="first_slug")

        Channel.objects.create(name="second", slug="second_slug")

        k = Keyboard.objects.create(name="first_keyboard", channel=c1)
        a1 = Action.objects.create(
            name="first_action",
            keyboard_to_represent=k
        )
        a2 = Action.objects.create(
            name="second_action",
            keyboard_to_represent=k
        )
        Button.objects.create(
            keyboard=k, action=a1,
            name="first_button",
            text="1", position=1
        )
        Button.objects.create(
            keyboard=k, action=a2,
            name="second_button",
            text="2", position=2
        )

    def test_str_action(self):
        a = Action.objects.get(name="first_action")
        self.assertEqual(str(a), "Подія: first_action")


class ButtonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        c1 = Channel.objects.create(name="first", slug="first_slug")

        Channel.objects.create(name="second", slug="second_slug")

        k = Keyboard.objects.create(name="first_keyboard", channel=c1)
        a1 = Action.objects.create(
            name="first_action", keyboard_to_represent=k
        )
        a2 = Action.objects.create(
            name="second_action", keyboard_to_represent=k
        )
        Button.objects.create(
            keyboard=k, action=a1,
            name="first_button",
            text="1", position=1
        )
        Button.objects.create(
            keyboard=k, action=a2,
            name="second_button",
            text="2", position=2
        )

    def test_str_button(self):
        b = Button.objects.get(name="first_button")
        self.assertEqual(str(b), "Кнопка: first_button")

    def test_params_for_template(self):
        b = Button.objects.get(name="first_button")
        self.assertEqual(
            b.params_for_template(),
            {'width': 6, 'height': 40, 'text_size': 18}
        )

    def test_v_align_for_template(self):
        b = Button.objects.get(name="first_button")
        self.assertEqual(b.v_align_for_template(), 0)
        b.text_v_align = "bottom"
        self.assertEqual(b.v_align_for_template(), 10)
        b.height = 2
        self.assertEqual(b.v_align_for_template(), 40)
        b.text_v_align = "middle"
        self.assertEqual(b.v_align_for_template(), 20)
        b.height = 1
        self.assertEqual(b.v_align_for_template(), 5)
