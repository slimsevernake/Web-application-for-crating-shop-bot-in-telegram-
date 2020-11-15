from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse


class ModeratorRegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_unlogin_access(self):
        c = Client()
        response = c.get("/signup/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        response = c.get(reverse("moderators:signup"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        response = c.get(reverse("moderators:signup"))
        self.assertTemplateUsed(response, "moderators/signup.html")

    def test_view_signup(self):
        c = Client()
        users = get_user_model().objects.filter(username="user")
        self.assertEqual(len(users), 0)
        response = c.post(reverse("moderators:signup"), {
            "username": "user",
            "email": "asd@asd.com",
        })
        self.assertEqual(response.url, "/login/")
        users = get_user_model().objects.filter(username="user")
        self.assertEqual(len(users), 1)


class ModeratorLoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create(
            username="moderator", password="1234"
        )

    def test_unlogin_required(self):
        c = Client()
        response = c.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:login"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:login"))
        self.assertTemplateUsed(response, "moderators/login.html")

    def test_view_login(self):
        c = Client()
        response = c.post(reverse("moderators:login"), {
            "username": "super",
            "password": "1234",
        })
        self.assertRedirects(
            response, reverse('moderators:user-profile'), 302, 200
        )


class ModeratorLogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create(
            username="moderator", password="1234"
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/logout/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/logout/")
        self.assertEqual(response.url, "/login/?next=/logout/")

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/logout/")
        self.assertEqual(response.url, '/login/')

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:logout"))
        self.assertEqual(response.url, '/login/')

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:logout"))
        self.assertTemplateNotUsed(response)

    def test_view_create_bot(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.post(reverse("moderators:logout"), {})
        self.assertEqual(response.url, '/login/')


class ModeratorUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create(
            username="moderator", password="1234"
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/profile/edit/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/profile/edit/")
        self.assertEqual(
            response.url, "/login/?next=/profile/edit/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/profile/edit/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:user-profile-edit"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:user-profile-edit"))
        self.assertTemplateUsed(
            response, "moderators/edit-profile.html"
        )

    def test_view_update_profile_login(self):
        c = Client()
        c.login(username="super", password="1234")
        users = get_user_model().objects.filter(first_name="name")
        self.assertEqual(len(users), 0)
        response = c.post(reverse("moderators:user-profile-edit"), {
            "username": "supersuper",
            "email": "asd@asd.com",
        })
        users = get_user_model().objects.filter(username="supersuper")
        self.assertEqual(len(users), 1)
        self.assertEqual(response.url, "/profile/")

    def test_view_update_profile_first_name(self):
        c = Client()
        c.login(username="super", password="1234")
        users = get_user_model().objects.filter(first_name="name")
        self.assertEqual(len(users), 0)
        response = c.post(reverse("moderators:user-profile-edit"), {
            "username": "super",
            "first_name": "name",
            "email": "asd@asd.com",
        })
        users = get_user_model().objects.filter(first_name="name")
        self.assertEqual(len(users), 1)
        self.assertEqual(response.url, "/profile/")


class ModeratorChangePasswordViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234"
        )
        get_user_model().objects.create(
            username="moderator", password="1234"
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/profile/change_password/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/profile/change_password/")
        self.assertEqual(
            response.url, "/login/?next=/profile/change_password/"
        )

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/profile/change_password/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:user-change-password"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:user-change-password"))
        self.assertTemplateUsed(
            response, "moderators/change-password.html"
        )

    def test_view_change_password(self):
        c = Client()
        c.login(username="super", password="1234")
        users = get_user_model().objects.filter(first_name="name")
        self.assertEqual(len(users), 0)
        response = c.post(reverse("moderators:user-change-password"), {
            "old_password": "1234",
            "new_password1": "aSfGmKlKiwe",
            "new_password2": "aSfGmKlKiwe",
        })
        self.assertEqual(response.url, "/profile/")
        user = authenticate(username="super", password="aSfGmKlKiwe")
        self.assertNotEqual(user, None)

    def test_view_change_password_fail(self):
        c = Client()
        c.login(username="super", password="1234")
        users = get_user_model().objects.filter(first_name="name")
        self.assertEqual(len(users), 0)
        response = c.post(reverse("moderators:user-change-password"), {
            "old_password": "12345",
            "new_password1": "aSfGmKlKiwe",
            "new_password2": "aSfGmKlKiwe",
        })
        self.assertEqual(response.status_code, 200)
        user = authenticate(username="super", password="aSfGmKlKiwe")
        self.assertEqual(user, None)
        user = authenticate(username="super", password="1234")
        self.assertNotEqual(user, None)


class ModeratorProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="super", password="1234", email="asd@asd.com"
        )
        get_user_model().objects.create(
            username="moderator", password="1234"
        )

    def test_login_required(self):
        c = Client()
        response = c.get("/profile/")
        self.assertEqual(response.status_code, 302)

    def test_moderator_access(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get("/profile/")
        self.assertEqual(response.url, "/login/?next=/profile/")

    def test_view_url_exist(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get("/profile/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:user-profile"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:user-profile"))
        self.assertTemplateUsed(response, "moderators/profile.html")

    def test_view_profile(self):
        c = Client()
        c.login(username="super", password="1234")
        response = c.get(reverse("moderators:user-change-password"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "super")
