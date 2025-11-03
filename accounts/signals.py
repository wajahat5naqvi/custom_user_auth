from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from .models import LoggedInUser

@receiver(user_logged_in)
def on_user_logged_in(sender, user, request, **kwargs):
    session_key = request.session.session_key or ''
    obj, created = LoggedInUser.objects.get_or_create(user=user)
    obj.is_active = True
    obj.last_login_at = timezone.now()
    obj.session_key = session_key
    obj.save()

@receiver(user_logged_out)
def on_user_logged_out(sender, user, request, **kwargs):
    try:
        obj = LoggedInUser.objects.get(user=user)
        obj.is_active = False
        obj.session_key = None
        obj.save()
    except LoggedInUser.DoesNotExist:
        pass
