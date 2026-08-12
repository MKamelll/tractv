from .models import WatchStatus
from profiles.models import Profile
from django.http import HttpRequest
from django.contrib.auth.models import User


class ProfilesServiceException(Exception):
    pass


def update_or_create_watch_status(
    request: HttpRequest, show_id: int, status: str
) -> None:
    if not isinstance(request.user, User):
        raise ProfilesServiceException("fuck off with this user")
    profile = Profile.objects.get(user=request.user)
    existing = WatchStatus.objects.filter(profile=profile, show_id=show_id).first()
    if existing and existing.status == status:
        existing.delete()
    else:
        WatchStatus.objects.update_or_create(
            profile=profile, show_id=show_id, defaults={"status": status}
        )


def get_watch_status(request: HttpRequest, show_id: int) -> str | None:
    if not isinstance(request.user, User):
        raise ProfilesServiceException("fuck off with this user")
    profile = Profile.objects.get(user=request.user)
    watch_status = WatchStatus.objects.filter(profile=profile, show_id=show_id).first()
    return watch_status.status if watch_status else None
