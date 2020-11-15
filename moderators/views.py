from typing import Union

from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.http import (
    JsonResponse,
    Http404,
    HttpRequest,
    HttpResponse
)
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    RedirectView)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout

from moderators.forms import (
    ModeratorLoginForm,
    ModeratorRegisterForm,
    ModeratorEditProfileForm,
    ModeratorChangePasswordForm
)
from moderators.services import (
    send_email,
    generate_password,
    change_user_password
)


class ModeratorRegisterView(CreateView):
    """
       Provides moderators the ability to register
    """
    template_name = "moderators/signup.html"
    form_class = ModeratorRegisterForm

    def form_valid(self, form):
        """
            Set password to form field
            and send mail with the new user`s password
        """
        password: str = generate_password()
        form.cleaned_data['password'] = password

        context: dict = {
            "password": password,
            "login_link": self.request.build_absolute_uri(
                reverse('moderators:login')
            ),
        }
        send_email(
            email=form.cleaned_data['email'],
            subject="Реєстрація",
            html_message=render_to_string(
                template_name="moderators/email-register.html",
                context=context
            ),
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('moderators:login')


class ModeratorLoginView(LoginView):
    """
        Provides moderators the ability to login
    """
    template_name = 'moderators/login.html'
    authentication_form = ModeratorLoginForm

    def get_success_url(self) -> str:
        next = self.request.META.get('QUERY_STRING')
        if next and next[:5] == 'next=':
            return next[5:]
        return reverse_lazy('moderators:user-profile')


class ModeratorLogoutView(LoginRequiredMixin, RedirectView):
    """
        Provides moderators the ability to login
    """
    url = '/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ModeratorUpdateView(LoginRequiredMixin, UpdateView):
    """
        Provides moderators the ability to edit profile
    """
    template_name = "moderators/edit-profile.html"
    form_class = ModeratorEditProfileForm
    success_url = reverse_lazy("moderators:user-profile")

    def get_object(self, queryset=None) -> User:
        return self.request.user


class ModeratorChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """
       Provides moderators the ability to change password
    """
    template_name = "moderators/change-password.html"
    form_class = ModeratorChangePasswordForm

    def get_success_url(self) -> str:
        context: dict = {
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "login_link": self.request.build_absolute_uri(
                reverse('moderators:login')
            ),
        }

        send_email(
            email=self.request.user.email,
            subject="Зміна паролю",
            html_message=render_to_string(
                "moderators/email-reset-password.html", context=context
            )
        )
        return reverse_lazy("moderators:user-profile")


class ModeratorProfileView(LoginRequiredMixin, DetailView):
    """
       Provides moderators the ability to see profile
    """
    template_name = "moderators/profile.html"
    context_object_name = 'user'

    def get_object(self, queryset=None) -> User:
        return self.request.user


@csrf_exempt
def reset_password_ajax(
        request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
    """
        Reset password using ajax-request
    """

    if request.is_ajax() and request.method == "POST":
        username = request.POST.get('username')

        user: User = User.objects.filter(username=username).first()
        if user:
            password: str = generate_password()
            change_user_password(user, password)
            context: dict = {
                "password": password,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "login_link": request.build_absolute_uri(
                    reverse('moderators:login')
                ),
            }
            send_email(
                email=user.email,
                subject="Зміна паролю",
                html_message=render_to_string(
                    "moderators/email-reset-password.html", context=context
                )
            )
            response: JsonResponse = JsonResponse({
                'success_msg': "Вам на пошту був відправленний новий пароль."
            })
            return response
        # if invalid username return 404
        else:
            return JsonResponse({'error': "Неправильні дані"}, status=404)

    raise Http404
