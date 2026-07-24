from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from api.service import api
from api.pydantic_models import Success, Failure, Show


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
