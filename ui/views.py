from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from api.service import api
from api.pydantic_models import Success, Failure, SearchResults


def shows(req: HttpRequest, show_id: int) -> HttpResponse:
    res = api.get_show_details(show_id)
    match res:
        case Success(data=show):
            return render(
                request=req,
                template_name="ui/shows/index.djhtml",
                context={"show": show},
            )
        case Failure(status_code=code, status_message=msg):
            return HttpResponse(msg, status=code)


def season(req: HttpRequest, show_id: int, season_number: int) -> HttpResponse:
    res = api.get_season_details(show_id, season_number)
    match res:
        case Success(data=season):
            return render(
                request=req,
                template_name="ui/shows/season.djhtml",
                context={"season": season},
            )
        case Failure(status_code=code, status_message=msg):
            return HttpResponse(msg, status=code)


def dashboard(req: HttpRequest) -> HttpResponse:
    return render(request=req, template_name="ui/dashboard/index.djhtml")


def search(req: HttpRequest) -> HttpResponse:
    query = req.GET.get("q", "")
    res = api.search_for_show(query)
    match res:
        case Success(data=SearchResults(results=results)):
            if len(results) > 0:
                return render(
                    request=req,
                    template_name="ui/partials/search_results.djhtml",
                    context={"results": results},
                )
            else:
                return render(
                    request=req,
                    template_name="ui/partials/search_results.djhtml",
                    context={"query": query}
                )
        case Failure(status_code=code, status_message=msg):
            return HttpResponse(msg, status=code)
