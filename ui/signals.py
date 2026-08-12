from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from profiles.models import Profile
from django.http import HttpRequest
from django.contrib.auth.models import User
from typing import Any


@receiver(user_signed_up)
def create_profile_on_signup(
    sender: Any, req: HttpRequest, user: User, **kwargs: Any
) -> None:
    Profile.objects.get_or_create(user=user)
