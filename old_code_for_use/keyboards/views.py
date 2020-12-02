from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView
)

from bots_management.mixins import (
    ModeratorRequiredMixin
)
from bots_management.services import get_bot_by_slug
from old_code_for_use.keyboards import (
    KeyboardAddForm, KeyboardUpdateForm, ButtonAddForm,
    ButtonUpdateForm, ActionAddForm, ActionUpdateForm
)
from old_code_for_use.keyboards import Button
from old_code_for_use.keyboards import (
    get_keyboards_related_to_bot, get_keyboard_by_pk_related_to_bot,
    get_keyboard_by_pk, get_actions_related_to_bot, get_action_by_pk,
)


class KeyboardListView(ModeratorRequiredMixin, ListView):
    template_name = "keyboards/keyboard_list.html"
    context_object_name = "keyboards"

    def get_queryset(self):
        return get_keyboards_related_to_bot(self.kwargs["slug"])

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context['channel'] = get_bot_by_slug(slug=self.kwargs["slug"])
        return context


class KeyboardDetailView(ModeratorRequiredMixin, DetailView):
    template_name = "keyboards/keyboard_detail.html"
    context_object_name = "keyboard"

    def get_object(self, queryset=None):
        return get_keyboard_by_pk_related_to_bot(
            pk=self.kwargs["pk"],
            slug=self.kwargs["slug"]
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super(KeyboardDetailView, self).get_context_data(**kwargs)

        context["buttons"] = self.object.buttons.all()
        context["button_form"] = ButtonAddForm(
            action_qs=get_actions_related_to_bot(self.kwargs["slug"])
        )
        context["buttons_tg"] = self.object.get_telegram_buttons()
        return context


class KeyboardUpdateView(ModeratorRequiredMixin, UpdateView):
    template_name = "keyboards/keyboard_detail.html"

    def get_object(self, queryset=None):
        return get_keyboard_by_pk_related_to_bot(
            pk=self.kwargs["pk"],
            slug=self.kwargs["slug"]
        )

    def get_form(self, form_class=None):
        channel = self.object.channel
        return KeyboardUpdateForm(**self.get_form_kwargs(), channel=channel)


class KeyboardCreateView(ModeratorRequiredMixin, CreateView):
    template_name = "keyboards/keyboard_create.html"

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:keyboards:keyboard-list",
            kwargs={
                "slug": self.kwargs["slug"]
            }
        )

    def get_form(self, form_class=None):
        channel = get_bot_by_slug(self.kwargs["slug"])
        return KeyboardAddForm(**self.get_form_kwargs(), channel=channel)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel"] = get_bot_by_slug(slug=self.kwargs["slug"])

        return context


class KeyboardDeleteView(ModeratorRequiredMixin, DeleteView):
    template_name = "keyboards/keyboard_delete.html"

    def get_object(self, queryset=None):
        return get_keyboard_by_pk_related_to_bot(
            pk=self.kwargs["pk"],
            slug=self.kwargs["slug"]
        )

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:keyboards:keyboard-list",
            kwargs={
                "slug": self.kwargs["slug"]
            }
        )


def create_button_view(request, slug, pk):
    if request.method == "POST":
        keyboard = get_keyboard_by_pk_related_to_bot(pk=pk, slug=slug)
        form = ButtonAddForm(
            data=request.POST,
            keyboard=keyboard,
            action_qs=get_actions_related_to_bot(slug=slug)
        )

        if form.is_valid():
            form.save()
        else:
            context = {
                "button_form": form,
                "keyboard": keyboard,
                "buttons": keyboard.buttons.all(),
            }
            return render(request, "keyboard_detail.html", context=context)

    return redirect(
        "bots-management:keyboards:keyboard-detail", slug=slug, pk=pk
    )


class ButtonUpdateView(ModeratorRequiredMixin, UpdateView):
    template_name = "keyboards/button_update.html"
    model = Button
    pk_url_kwarg = "pk_button"

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:keyboards:keyboard-detail",
            kwargs={
                "slug": self.kwargs["slug"],
                "pk": self.kwargs["pk"]
            }
        )

    def get_form(self, form_class=None):
        keyboard = get_keyboard_by_pk(self.kwargs["pk"])
        return ButtonUpdateForm(
            **self.get_form_kwargs(),
            keyboard=keyboard,
            action_qs=get_actions_related_to_bot(self.kwargs["slug"])
        )

    def get_context_data(self, **kwargs):
        context = super(ButtonUpdateView, self).get_context_data(**kwargs)
        context["keyboard"] = self.object.keyboard

        return context


class ButtonDeleteView(ModeratorRequiredMixin, DeleteView):
    template_name = "keyboards/button_delete.html"
    model = Button
    pk_url_kwarg = "pk_button"

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:keyboards:keyboard-detail",
            kwargs={
                "slug": self.kwargs["slug"],
                "pk": self.kwargs["pk"]
            }
        )


class ActionListView(ModeratorRequiredMixin, ListView):
    template_name = "keyboards/action_list.html"
    context_object_name = "actions"

    def get_queryset(self):
        return get_actions_related_to_bot(slug=self.kwargs["slug"])

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        context["channel"] = get_bot_by_slug(
            slug=self.kwargs["slug"]
        )

        return context


class ActionDetailView(ModeratorRequiredMixin, DetailView):
    template_name = "keyboards/action_detail.html"
    context_object_name = "action"

    def get_object(self, queryset=None):
        return get_action_by_pk(pk=self.kwargs["pk"])


class ActionCreateView(ModeratorRequiredMixin, CreateView):
    template_name = "keyboards/action_create.html"

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:keyboards:action-list",
            kwargs={
                "slug": self.kwargs["slug"]
            }
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["channel"] = get_bot_by_slug(slug=self.kwargs["slug"])

        return context

    def get_form(self, form_class=None):
        return ActionAddForm(**self.get_form_kwargs(),
                             keyboards_qs=get_keyboards_related_to_bot(
                                 slug=self.kwargs["slug"]
                             ))


class ActionUpdateView(ModeratorRequiredMixin, UpdateView):
    template_name = "keyboards/action_update.html"

    def get_object(self, queryset=None):
        return get_action_by_pk(pk=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:keyboards:action-detail",
            kwargs={
                "slug": self.kwargs["slug"],
                "pk": self.kwargs["pk"]
            }
        )

    def get_form(self, form_class=None):
        return ActionUpdateForm(**self.get_form_kwargs(),
                                keyboards_qs=get_keyboards_related_to_bot(
                                    slug=self.kwargs["slug"]
                                ))


class ActionDeleteView(ModeratorRequiredMixin, DeleteView):
    template_name = "keyboards/action_delete.html"

    def get_object(self, queryset=None):
        return get_action_by_pk(pk=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy(
            "bots-management:keyboards:action-list",
            kwargs={
                "slug": self.kwargs["slug"]
            }
        )
