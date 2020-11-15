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
    set_webhook_ajax as tg_set_webhook_ajax,
    unset_webhook_ajax as tg_remove_webhook_ajax

)
from telegram_api.handlers import (
    event_handler_tg
)

from .forms import (
    BotUpdateForm, BotForm
)
from .mixins import ModeratorRequiredMixin
from .models import Bot
from .services import (
    get_bot_by_slug,
    get_all_available_bots_to_moderator,
    get_bots_to_json, extract_data,
    get_moderators_to_json,
)
# from keyboards.services import get_actions_related_to_channel

logger = logging.getLogger(__name__)


def root_view(request):
    return redirect("bots-management:channel-list")


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
    template_name = "bots_management/channel_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        user = self.request.user
        context["channels"] = get_all_available_bots_to_moderator(user)
        return context


class BotDetailView(ModeratorRequiredMixin, DetailView):
    """
    Get info can only moderator or superuser.
    """
    model = Bot
    template_name = "bots_management/channel_details.html"
    context_object_name = "channel"

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


class BotUpdateView(ModeratorRequiredMixin, UpdateView):
    """
    Bot can update only moderator or superuser.
    """
    model = Bot
    template_name = "bots_management/bot_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:channel-detail",
            kwargs={"slug": self.object.channel.slug}
        )

    # TODO: fix this

    # def get_form(self, *args, **kwargs):
    #     channel = get_channel_by_slug(self.kwargs["slug"])
    #     if channel:
    #         return BotUpdateForm(**self.get_form_kwargs(), channel=channel)
    #     else:
    #         raise Http404


class BotCreateView(ModeratorRequiredMixin, CreateView):
    """
    Channel can create only moderator or superuser.
    """
    model = Bot
    template_name = "bots_management/bot_add.html"

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:channel-detail",
            kwargs={"slug": self.object.channel.slug}
        )


class BotDeleteView(DeleteView):
    """
    Channel can delete only superuser.
    """
    model = Bot
    template_name = "bots_management/channel_delete.html"
    success_url = reverse_lazy("bots-management:channel-list")


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


# def channel_list_view(request):
#     """
#         Template for new front
#     """
#     form = ChannelFrontForm()
#     return render(request, "bots_management/channels_new.html", {"form": form})


def ajax_get_channels(request):
    """
        Get list of channels
    """
    if request.is_ajax():
        return HttpResponse(get_bots_to_json())
    return Http404


def ajax_webhook(request):
    if request.is_ajax():
        token = request.POST.get('token')
        host = request.META['HTTP_HOST']
        slug = request.POST.get('channel_url')
        messenger = request.POST.get('messenger')
        response = tg_set_webhook_ajax(slug, host, token)
        return HttpResponse(json.dumps(response))
    return Http404


def ajax_unset_webhook(request):
    if request.is_ajax():
        token = request.POST.get('token')
        messenger = request.POST.get('messenger')
        response = tg_remove_webhook_ajax(token)
        return HttpResponse(json.dumps(response))
    return Http404


def ajax_get_moderators(request):
    """
        Get list of channels
    """
    if request.is_ajax():
        return HttpResponse(get_moderators_to_json())
    return Http404


def keyboards_constructor_view(request):
    """
        Template for new front
    """
    form = BotForm()
    return render(
        request,
        "bots_management/keyboards_constructor.html",
        {"form": form}
    )

#
# def statistics_view(request):
#     """
#         Template for new front
#     """
#     form = ChannelFrontForm()
#     return render(request, "bots_management/statistics.html", {"form": form})
