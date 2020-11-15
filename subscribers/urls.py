from django.urls import path

from subscribers.views import (
    SubscribersListView, SubscriberMessagesListView,
    HelpMessagesListView, HelpMessageReplyView,
    HelpMessageReplyDetailView, SubscriberUpdateView
)

app_name = "subscribers"

urlpatterns = [

    path("<str:slug>/<int:pk>/", SubscriberUpdateView.as_view(),
         name="subscriber-update"),
    path("<str:slug>/<str:messenger>_<str:status>/",
         SubscribersListView.as_view(),
         name="subscriber-list"),

    path("<str:slug>/messages/<str:messenger>",
         SubscriberMessagesListView.as_view(),
         name="subscriber-messages"),

    path("<str:slug>/help-messages",
         HelpMessagesListView.as_view(),
         name="help-messages"),
    path("<str:slug>/help-messages/<int:pk>/",
         HelpMessageReplyDetailView.as_view(),
         name="help-message-detail"),
    path("<str:slug>/help-messages/<int:pk>/reply/",
         HelpMessageReplyView.as_view(),
         name="help-message-reply")
]
