from .models import WatchStatus
from profiles.models import Profile, EpisodeWatch
from api.services import get_or_fetch_season, get_show_episodes_ids


class ProfilesServiceException(Exception):
    pass


def update_or_create_watch_status(profile: Profile, show_id: int, status: str) -> None:
    existing = WatchStatus.objects.filter(profile=profile, show_id=show_id).first()
    if existing and existing.status == status:
        existing.delete()
        if status == "completed":
            epispdes_ids = get_show_episodes_ids(series_id=show_id)
            EpisodeWatch.objects.filter(episode_id__in=epispdes_ids).delete()
    else:
        WatchStatus.objects.update_or_create(
            profile=profile, show_id=show_id, defaults={"status": status}
        )
        if status == "completed":
            epispdes_ids = get_show_episodes_ids(series_id=show_id)
            watches = [
                EpisodeWatch(profile=profile, episode_id=id) for id in epispdes_ids
            ]
            EpisodeWatch.objects.bulk_create(watches)


def get_show_watch_status(profile: Profile, show_id: int) -> str | None:
    watch_status = WatchStatus.objects.filter(profile=profile, show_id=show_id).first()
    return watch_status.status if watch_status else None


def is_episode_watched(profile: Profile, episode_id: int) -> bool:
    return (
        EpisodeWatch.objects.filter(profile=profile, episode_id=episode_id).first()
        is not None
    )


def get_season_watch_status(
    profile: Profile, show_id: int, season_number: int
) -> list[int]:
    _, episodes, _ = get_or_fetch_season(series_id=show_id, season_number=season_number)
    episodes_watches = EpisodeWatch.objects.filter(
        episode__in=episodes, profile=profile
    ).select_related("episode")
    return [w.episode.id for w in episodes_watches]


def mark_episodes_watched(profile: Profile, ids: list[int]) -> None:
    EpisodeWatch.objects.bulk_create(
        [EpisodeWatch(profile=profile, episode_id=id) for id in ids]
    )
