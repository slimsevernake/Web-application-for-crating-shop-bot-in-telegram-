from django.contrib.auth.mixins import AccessMixin

from bots_management.services import get_bot_by_slug


class ModeratorRequiredMixin(AccessMixin):
    """
    Raises 403 if user not in bots's moderators list and
    is not a superuser.
    """

    def dispatch(self, request, *args, **kwargs):
        bot = get_bot_by_slug(kwargs.get("slug"))

        if bot:
            if all([not request.user.is_superuser,
                    request.user not in bot.moderators.all()]):
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(AccessMixin):
    """
    Raises 403 if user is not a bot owner.
    """

    def dispatch(self, request, *args, **kwargs):
        bot = get_bot_by_slug(kwargs.get("slug"))

        if bot and request.user != bot.owner:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
