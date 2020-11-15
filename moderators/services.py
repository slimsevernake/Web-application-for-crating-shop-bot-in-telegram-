import string
import random

from smtplib import SMTPException

from django.contrib.auth.models import User
from django.core.mail import send_mail as django_send_mail


def generate_password() -> str:
    """
    Generate new password
    """
    password_characters: str = string.ascii_letters + string.digits
    return ''.join(random.choice(password_characters) for i in range(8))


def send_email(
        email: str, subject: str,
        message: str = None, html_message: str = None) -> None:
    """
    Send new password to email
    """

    try:
        django_send_mail(
            subject,
            message,
            'Administration of site',
            [email],
            fail_silently=False,
            html_message=html_message,
        )
    except SMTPException as e:
        print(e)
        # TODO: Add logging


def change_user_password(user: User, password: str) -> None:
    """
    Change password field in user object
    """
    user.set_password(password)
    user.save()
