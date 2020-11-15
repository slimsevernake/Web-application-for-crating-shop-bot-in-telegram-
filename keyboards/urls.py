from django.urls import path, include

from keyboards.views import (
    KeyboardListView, KeyboardDetailView, KeyboardUpdateView,
    KeyboardCreateView, KeyboardDeleteView, ButtonDeleteView,
    create_button_view, ButtonUpdateView, ActionListView,
    ActionDetailView, ActionCreateView, ActionUpdateView, ActionDeleteView
)

app_name = "keyboards"

button_urlpatterns = [
    path("button_create/",
         create_button_view,
         name="button-create"),
    path("button_update/<int:pk_button>/",
         ButtonUpdateView.as_view(),
         name="button-update"),
    path("button_delete/<int:pk_button>/",
         ButtonDeleteView.as_view(),
         name="button-delete")
]

urlpatterns = [
    path("keyboards/", KeyboardListView.as_view(), name="keyboard-list"),
    path("keyboard/<int:pk>/",
         KeyboardDetailView.as_view(),
         name="keyboard-detail"),
    path("keyboard_update/<int:pk>/",
         KeyboardUpdateView.as_view(),
         name="keyboard-update"),
    path("keyboard_create/",
         KeyboardCreateView.as_view(),
         name="keyboard-create"),
    path("keyboard_delete/<int:pk>/",
         KeyboardDeleteView.as_view(),
         name="keyboard-delete"),

    path("keyboard/<int:pk>/", include(button_urlpatterns)),

    path("actions/", ActionListView.as_view(), name="action-list"),
    path("action/<int:pk>/",
         ActionDetailView.as_view(),
         name="action-detail"),
    path("action_create/",
         ActionCreateView.as_view(),
         name="action-create"),
    path("action_update/<int:pk>/",
         ActionUpdateView.as_view(),
         name="action-update"),
    path("action_delete/<int:pk>/",
         ActionDeleteView.as_view(),
         name="action-delete"),
]
