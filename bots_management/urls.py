from django.urls import path, include

from .views import (
    telegram_index, BotListView,
    BotDetailView, BotDeleteView, BotUpdateView,
    BotCreateView, root_view,
    # ajax_channels_update,
    # channel_list_view,

    ajax_get_channels, ajax_get_moderators,
    #statistics_view
)

app_name = "bots-management"

urlpatterns = [
    path("", root_view, name="root"),
    # path("ajax_channels_update/",
    #      ajax_channels_update,
    #      name='ajax_channels_update'),

    path("bots/",
         BotListView.as_view(),
         name="bot-list"),
    path("bot/create/",
         BotCreateView.as_view(),
         name="bot-create"),
    path("bot/<str:slug>/",
         BotDetailView.as_view(),
         name="bot-detail"),
    path("bot/<str:slug>/delete",
         BotDeleteView.as_view(),
         name="bot-delete"),
    path("bot/<str:slug>/update/",
         BotUpdateView.as_view(),
         name="bot-update"),
    # path("statistics_new",
    #      statistics_view,
    #      name="statistics-new"),

    # bots and subscribers' analytics
    # path("bot/<str:slug>/",
    #      include("old_code_for_use.analytics.urls", namespace="analytics")),

    path("subscribers/",
         include("subscribers.urls", namespace="subscribers")),

    # bots` mailings
    path("bot/<str:slug>/",
         include("bots_mailings.urls", namespace="mailings")),

    path("telegram_prod/<str:slug>/", telegram_index),
]
