from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from api.tmdb import tmdb_client
from api.services import get_or_fetch_show, get_or_fetch_season
from django.contrib.auth.decorators import login_required


@login_required
def shows(req: HttpRequest, show_id: int) -> HttpResponse:
    show, seasons = get_or_fetch_show(series_id=show_id)
    return render(
        request=req,
        template_name="ui/shows/index.djhtml",
        context={"show": show, "seasons": seasons, "status": "none"},
    )


@login_required
def season(req: HttpRequest, show_id: int, season_number: int) -> HttpResponse:
    season, episodes = get_or_fetch_season(
        series_id=show_id, season_number=season_number
    )
    return render(
        request=req,
        template_name="ui/shows/season.djhtml",
        context={"season": season, "episodes": episodes},
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
    return HttpResponse()
