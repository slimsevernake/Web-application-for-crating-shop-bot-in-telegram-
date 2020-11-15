from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from bots_management.mixins import ModeratorRequiredMixin
from bots_management.services import get_bot_by_slug
from keyboards.services import get_actions_related_to_bot
from subscribers.forms import (
    ReplyHelpMessageForm, SubscribersChoiceForm
)
from subscribers.models import Subscriber, HelpReply
from subscribers.services import (
    get_messages_subscribers_of_bot, get_all_help_messages,
    get_all_active_help_messages, get_all_started_help_messages,
    get_all_closed_help_messages, get_help_message_reply,
    get_status_subscribers_of_bot,
)


class SubscribersListView(ModeratorRequiredMixin, generic.ListView):
    """
    List of all subscribers of a particular channel.
    """

    template_name = "subscribers/subscriber_list.html"
    context_object_name = "subscribers"

    def get_queryset(self):
        return get_status_subscribers_of_bot(
            self.kwargs["slug"],
            self.kwargs["messenger"],
            self.kwargs["status"],
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel"] = get_bot_by_slug(self.kwargs["slug"])
        context['form'] = SubscribersChoiceForm(initial={'messenger': 'all',
                                                         'status': 'all'})
        return context

    def post(self, request, *args, **kwargs):
        form = SubscribersChoiceForm(request.POST or None)
        slug = self.kwargs['slug']
        if form.is_valid():
            form = form.cleaned_data
        return redirect(
            f"/subscribers/{slug}/{form['messenger']}_{form['status']}/"
        )


class SubscriberUpdateView(ModeratorRequiredMixin, generic.UpdateView):
    """
    Update subscriber activity status.
    """

    model = Subscriber
    fields = ["is_active", "info"]
    template_name = 'subscribers/subscriber_update.html'
    context_object_name = "subscriber"

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:subscribers:subscriber-list",
            kwargs={
                "slug": self.kwargs["slug"],
                "messenger": 'all',
                "status": 'all',
            }
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel"] = get_bot_by_slug(self.kwargs["slug"])
        return context


class SubscriberMessagesListView(ModeratorRequiredMixin, generic.ListView):
    """
    List of all message subscribers of a particular channel.
    """

    template_name = "subscribers/subscriber_messages_list.html"
    context_object_name = "messages"
    paginate_by = 100

    def get_queryset(self):
        return get_messages_subscribers_of_bot(self.kwargs["slug"])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['messenger'] = self.kwargs["messenger"]
        context['slug'] = self.kwargs["slug"]
        context["channel"] = get_bot_by_slug(self.kwargs["slug"])
        return context


class HelpMessagesListView(ModeratorRequiredMixin, generic.ListView):
    template_name = "subscribers/help_messages_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        show = self.request.GET.get("show", "active")
        slug = self.kwargs["slug"]

        if show == "all":
            return get_all_help_messages(slug).order_by("-created")
        elif show == "started":
            return get_all_started_help_messages(slug)
        elif show == "closed":
            return get_all_closed_help_messages(slug)
        else:
            return get_all_active_help_messages(slug)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel"] = get_bot_by_slug(self.kwargs["slug"])
        return context


class HelpMessageReplyDetailView(ModeratorRequiredMixin, generic.DetailView):
    template_name = "subscribers/help_message_detail.html"
    context_object_name = "reply"
    model = HelpReply

    def get_object(self, queryset=None):
        return get_help_message_reply(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel"] = get_bot_by_slug(slug=self.kwargs["slug"])

        return context


class HelpMessageReplyView(ModeratorRequiredMixin, generic.UpdateView):
    template_name = "subscribers/help_message_reply.html"
    model = HelpReply

    def get_form(self, form_class=None):
        return ReplyHelpMessageForm(
            **self.get_form_kwargs(),
            action_qs=get_actions_related_to_bot(slug=self.kwargs["slug"]),
        )

    def get_object(self, queryset=None):
        """
        Automatically saves moderator, who pressed answer and status is now
        is started
        """
        obj = get_help_message_reply(pk=self.kwargs["pk"])

        obj.is_started = True
        if not obj.started_at:
            obj.started_at = timezone.now()
        obj.moderators.add(self.request.user)
        obj.save()

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel"] = get_bot_by_slug(slug=self.kwargs["slug"])

        return context

    def get_success_url(self):
        return reverse_lazy("bots-management:subscribers:help-messages",
                            kwargs={"slug": self.kwargs["slug"]})
