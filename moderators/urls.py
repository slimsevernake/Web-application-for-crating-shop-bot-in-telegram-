from django.urls import path

from .views import (
    ModeratorRegisterView,
    ModeratorLoginView,
    ModeratorProfileView,
    ModeratorUpdateView,
    ModeratorChangePasswordView,
    reset_password_ajax,
    ModeratorLogoutView,
)

app_name = "moderators"

urlpatterns = [
    path("signup/",
         ModeratorRegisterView.as_view(),
         name="signup"),
    path("login/",
         ModeratorLoginView.as_view(),
         name="login"),
    path("logout/",
         ModeratorLogoutView.as_view(),
         name="logout"),
    path("profile/",
         ModeratorProfileView.as_view(),
         name="user-profile"),
    path("profile/edit/",
         ModeratorUpdateView.as_view(),
         name="user-profile-edit"),
    path("profile/change_password/",
         ModeratorChangePasswordView.as_view(),
         name="user-change-password"),
    path("reset_password_ajax/",
         reset_password_ajax,
         name="reset-password"),
]
