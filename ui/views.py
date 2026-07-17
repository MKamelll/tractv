from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def index(req: HttpRequest) -> HttpResponse:
    return render(request=req, template_name="ui/shows/index.djhtml")
