from django.urls import path

from bots_mailings.views import (
    MailingListView,
    MailingCreateView,
    MailingDetailedView,
    MailingUpdateView,
    MailingDeleteView,
)

app_name = "mailings"

urlpatterns = [
    path(
        "mailings/",
        MailingListView.as_view(),
        name="mailing-list"
    ),
    path(
        "mailing/create/",
        MailingCreateView.as_view(),
        name="mailing-create"
    ),
    path(
        "mailing/<int:pk>/",
        MailingDetailedView.as_view(),
        name="mailing-detailed"
    ),
    path(
        "mailing/<int:pk>/update",
        MailingUpdateView.as_view(),
        name="mailing-update"
    ),
    path(
        "mailing/<int:pk>/delete",
        MailingDeleteView.as_view(),
        name="mailing-delete"
    ),
]
