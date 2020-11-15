from django.urls import path, include

from .views import (
    telegram_index, BotListView,
    BotDetailView, BotDeleteView, BotUpdateView,
    BotCreateView, root_view,
    # ajax_channels_update,
    # channel_list_view,

    ajax_get_channels,
    ajax_webhook, ajax_get_moderators, ajax_unset_webhook,
    keyboards_constructor_view, #statistics_view
)

app_name = "bots-management"

urlpatterns = [
    path("", root_view, name="root"),
    path("ajax_get_channels/",
         ajax_get_channels,
         name='ajax_get_channels'),
    path("ajax_get_moderators/",
         ajax_get_moderators,
         name='ajax_get_moderators'),
    # path("ajax_channels_update/",
    #      ajax_channels_update,
    #      name='ajax_channels_update'),
    # path("channels_new/",
    #      channel_list_view,
    #      name="channel-list-new"),
    path("ajax_webhook/",
         ajax_webhook,
         name="ajax_webhook"),
    path("ajax_unset_webhook/",
         ajax_unset_webhook,
         name="ajax_unset_webhook"),


    path("bots/",
         BotListView.as_view(),
         name="channel-list"),
    path("bot/<str:slug>/",
         BotDetailView.as_view(),
         name="channel-detail"),
    path("bot/<str:slug>/delete",
         BotDeleteView.as_view(),
         name="channel-delete"),
    path("bot/create/",
         BotCreateView.as_view(),
         name="bot-create"),
    path("bot/<str:slug>/update/",
         BotUpdateView.as_view(),
         name="bot-update"),
    path("keyboards_new",
         keyboards_constructor_view,
         name="keyboards-new"),
    # path("statistics_new",
    #      statistics_view,
    #      name="statistics-new"),

    # actions with keyboards, related to certain channel
    path("bot/<str:slug>/",
         include("keyboards.urls", namespace="keyboards")),

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
