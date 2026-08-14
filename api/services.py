from . import models
from .tmdb import tmdb_client
from django.db.models import Q


class ServiceException(Exception):
    pass


def get_or_fetch_show(series_id: int) -> tuple[models.Show, list[models.Season]]:
    show = models.Show.objects.filter(Q(id=series_id) | Q(tmdb_id=series_id)).first()
    if show:
        seasons = list(models.Season.objects.filter(show=show))
        return (show, seasons)
    res = tmdb_client.get_show_details(series_id=series_id)
    show = models.Show(
        tmdb_id=res.id,
        name=res.name,
        number_of_episodes=res.number_of_episodes,
        number_of_seasons=res.number_of_seasons,
        origin_country=",".join(res.origin_country),
        original_language=res.original_language,
        original_name=res.original_name,
        overview=res.overview,
        poster_path=res.poster_path or "",
        vote_average=res.vote_average,
        vote_count=res.vote_count,
    )
    show.save()
    seasons = [
        models.Season(
            tmdb_id=s.id,
            episode_count=s.episode_count or 0,
            name=s.name,
            overview=s.overview,
            poster_path=s.poster_path or "",
            season_number=s.season_number,
            vote_average=s.vote_average,
            show=show,
        )
        for s in res.seasons
    ]
    models.Season.objects.bulk_create(seasons)
    return (show, seasons)


def get_or_fetch_season(
    series_id: int, season_number: int
) -> tuple[models.Season, list[models.Episode]]:
    show, seasons = get_or_fetch_show(series_id=series_id)
    season = seasons[season_number] if 0 <= season_number < len(seasons) else None
    if not season:
        raise ServiceException("fuck off, this season isn't even real")
    episodes = list(models.Episode.objects.filter(season=season).filter(show=show))
    if len(episodes) > 0:
        return (season, episodes)
    res = tmdb_client.get_season_details(
        series_id=show.tmdb_id, season_number=season_number
    )
    new_episodes = [
        models.Episode(
            tmdb_id=e.id,
            episode_type=e.episode_type,
            episode_number=e.episode_number,
            name=e.name,
            overview=e.overview,
            season=season,
            show=show,
            still_path=e.still_path or "",
            vote_average=e.vote_average,
            vote_count=e.vote_count,
        )
        for e in res.episodes
    ]
    models.Episode.objects.bulk_create(new_episodes)
    return (season, new_episodes)


def get_show_episodes_ids(series_id: int) -> list[int]:
    return list(
        models.Episode.objects.filter(show_id=series_id).values_list("id", flat=True)
    )
