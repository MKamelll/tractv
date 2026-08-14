from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from api.tmdb import tmdb_client
from api.services import get_or_fetch_show, get_or_fetch_season
from django.contrib.auth.decorators import login_required
from profiles.services import (
    update_or_create_watch_status,
    get_show_watch_status,
    get_season_watch_status,
    mark_episodes_watched,
)


@login_required
def shows(req: HttpRequest, show_id: int) -> HttpResponse:
    show, seasons = get_or_fetch_show(series_id=show_id)
    status = get_show_watch_status(profile=req.user.profile, show_id=show.id) or "none"
    return render(
        request=req,
        template_name="ui/shows/index.djhtml",
        context={"show": show, "seasons": seasons, "status": status},
    )


@login_required
def season(req: HttpRequest, show_id: int, season_number: int) -> HttpResponse:
    season, episodes, created_episodes = get_or_fetch_season(
        series_id=show_id, season_number=season_number
    )
    show_watch_status = get_show_watch_status(profile=req.user.profile, show_id=show_id)
    is_show_completed = (
        show_watch_status is not None and show_watch_status == "completed"
    )
    if created_episodes and is_show_completed:
        mark_episodes_watched(profile=req.user.profile, ids=[e.id for e in episodes])
    episodes_watches = get_season_watch_status(
        profile=req.user.profile, show_id=show_id, season_number=season_number
    )
    return render(
        request=req,
        template_name="ui/shows/season.djhtml",
        context={"season": season, "episodes": episodes, "watches": episodes_watches},
    )


@login_required
def dashboard(req: HttpRequest) -> HttpResponse:
    return render(request=req, template_name="ui/dashboard/index.djhtml")


@login_required
def search(req: HttpRequest) -> HttpResponse:
    query = req.GET.get("q", "")
    res = tmdb_client.search_for_show(query)
    if len(res.results) > 0:
        return render(
            request=req,
            template_name="ui/partials/search_results.djhtml",
            context={"results": res.results},
        )
    else:
        return render(
            request=req,
            template_name="ui/partials/search_results.djhtml",
            context={"query": query},
        )


@login_required
def status_update(req: HttpRequest, show_id: int, status: str) -> HttpResponse:
    try:
        update_or_create_watch_status(
            profile=req.user.profile, show_id=show_id, status=status
        )
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)
