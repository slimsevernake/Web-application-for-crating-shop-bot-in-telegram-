import logging
import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView,
)

from telegram_api.api import (
    get_bot_info as tg_bot_info,
    get_webhook_info as tg_webhook_info,
    set_webhook as tg_set_webhook_ajax,
    unset_webhook_ajax as tg_remove_webhook_ajax

)
from telegram_api.handlers import (
    event_handler_tg
)

from .forms import (
     BotForm
)
from .mixins import ModeratorRequiredMixin, OwnerRequiredMixin
from .models import Bot
from .services import (
    get_bot_by_slug,
    get_all_available_bots_to_moderator,
    get_all_users_bots,
    get_bots_to_json, extract_data,
    get_moderators_to_json,
)

# from keyboards.services import get_actions_related_to_channel

logger = logging.getLogger(__name__)


def root_view(request):
    return redirect("bots-management:bot-list")


def notfound(request, exception=None):
    """
    redirect to channel list if something raises Http404 or
    to login page, if user isn't logged in
    IF DEBUG = False
    """
    # TODO create normal 404 page to render it
    return redirect("bots-management:channel-list")


class BotListView(LoginRequiredMixin, ListView):
    """
    Only related to user channels will be displayed
    """
    model = Bot
    template_name = "bots_management/bot_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        user = self.request.user
        context["bots_to_management"] = get_all_available_bots_to_moderator(user)
        context["bots"] = get_all_users_bots(user)
        return context


class BotDetailView(ModeratorRequiredMixin, DetailView):
    """
    Get info can only moderator or superuser.
    """
    model = Bot
    template_name = "bots_management/bot_details.html"
    context_object_name = "bot"

    def get_context_data(self, **kwargs) -> dict:
        context = super(BotDetailView, self).get_context_data()

        # show response of action with webhook
        show_webhook = self.request.GET.get("show_webhook", None)
        if show_webhook == "true":
            messenger = self.request.GET.get("messenger", None)

            if messenger == "telegram":
                webhook_info = tg_webhook_info(
                    self.object.telegram_token
                )
                if not webhook_info:
                    webhook_info = {"ok": False,
                                    "error_code": 404,
                                    "description": "Not Found"}
                context["webhook_info"] = webhook_info
        return context


class BotUpdateView(OwnerRequiredMixin, UpdateView):
    """
    Bot can update only moderator or superuser.
    """
    model = Bot
    template_name = "bots_management/bot_update.html"
    context_object_name = "bot"

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:bot-detail",
            kwargs={"slug": self.object.slug}
        )

    def get_form(self, *args, **kwargs):
        bot = get_bot_by_slug(self.kwargs["slug"])
        if bot:
            return BotForm(**self.get_form_kwargs())
        else:
            raise Http404


class BotCreateView(LoginRequiredMixin, CreateView):
    """
    Bot can be created only by a moderator or a superuser.
    """
    model = Bot
    template_name = "bots_management/bot_add.html"

    def get_form(self, *args, **kwargs):
        user = self.request.user
        return BotForm(*args, **self.get_form_kwargs(), user=user)

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:bot-detail",
            kwargs={"slug": self.object.slug}
        )


class BotDeleteView(DeleteView):
    """
    Channel can delete only superuser.
    """
    model = Bot
    template_name = "bots_management/bot_delete.html"
    success_url = reverse_lazy("bots-management:bot-list")


@csrf_exempt
def telegram_index(request, slug):
    if request.method == "POST":
        incoming_data: dict = json.loads(request.body.decode("utf-8"))
        if settings.DEBUG:
            logger.warning(
                f"""\n {incoming_data} \n"""
            )
        event_handler_tg(incoming_data=incoming_data, channel_slug=slug)
        return HttpResponse(status=200)

    return HttpResponse(status=404)


# TODO: fix this

# def ajax_channels_update(request):
#     """
#     Create or update channel with ajax
#     """
#     if request.is_ajax() and request.method == "POST":
#         data = extract_data(request)
#         channel_id = data.pop('id')
#         if channel_id:
#             Channel.objects.update_or_create(
#                 id=channel_id,
#                 defaults=data,
#             )
#         else:
#             Channel(**data).save()
#         return HttpResponse(get_channel_to_json())
#     else:
#         raise Http404


def ajax_get_channels(request):
    """
        Get list of channels
    """
    if request.is_ajax():
        return HttpResponse(get_bots_to_json())
    return Http404


def ajax_get_moderators(request):
    """
        Get list of channels
    """
    if request.is_ajax():
        return HttpResponse(get_moderators_to_json())
    return Http404


#
# def statistics_view(request):
#     """
#         Template for new front
#     """
#     form = ChannelFrontForm()
#     return render(request, "bots_management/statistics.html", {"form": form})
