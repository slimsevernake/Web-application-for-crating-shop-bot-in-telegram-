import logging

from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from bots_mailings.tasks import send_mailing, delete_mailing
from bots_management.services import get_bot_by_slug
from bots_management.mixins import ModeratorRequiredMixin
from bots_mailings.forms import (
    MailingForm,
    MailingUpdateForm,
)
from bots_mailings.models import Post

logger = logging.getLogger(__name__)


class MailingListView(ModeratorRequiredMixin, ListView):
    template_name = "bots_mailings/mailing_list.html"
    context_object_name = 'mailings'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['channel'] = get_bot_by_slug(self.kwargs['slug'])
        return context


class MailingCreateView(ModeratorRequiredMixin, CreateView):
    template_name = "bots_mailings/mailing_create.html"
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['channel_slug'] = self.kwargs.get('slug')
        return kwargs

    def get_success_url(self):
        # if message is planned send to
        if self.object.send_time:
            send_mailing.apply_async(
                (self.object.id,),
                eta=self.object.send_time,
            )
        else:
            send_mailing.delay(post_id=self.object.id)
        return reverse_lazy(
            "bots-management:mailings:mailing-list",
            kwargs={
                "slug": self.kwargs.get('slug')
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel = get_bot_by_slug(self.kwargs.get('slug'))
        context['channel'] = channel
        return context


class MailingUpdateView(ModeratorRequiredMixin, UpdateView):
    template_name = "bots_mailings/mailing_update.html"
    form_class = MailingUpdateForm
    model = Post
    context_object_name = 'mailing'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['chan    nel_slug'] = self.kwargs.get('slug')
        return kwargs

    def get_object(self, queryset=None):
        # TODO: remove in future, when editing in telegram will be added
        obj = super().get_object(queryset)
        if obj.is_done:
            raise Http404()
        return obj

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:mailings:mailing-list",
            kwargs={
                "slug": self.kwargs.get('slug')
            }
        )


class MailingDetailedView(ModeratorRequiredMixin, DetailView):
    template_name = "bots_mailings/mailing_detailed.html"
    context_object_name = "mailing"
    model = Post


class MailingDeleteView(ModeratorRequiredMixin, DeleteView):
    template_name = "bots_mailings/mailing_delete.html"
    context_object_name = "mailing"
    model = Post

    def delete(self, request, *args, **kwargs):
        # Delete messages in telegram only if mailing is done
        if self.get_object().is_done:
            delete_mailing.delay(post_id=self.get_object().id)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:mailings:mailing-list",
            kwargs={
                "slug": self.kwargs["slug"]
            }
        )
