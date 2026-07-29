from django.urls import path
from .views import shows, season, dashboard, search

urlpatterns = [
    path("shows/<int:show_id>", view=shows, name="shows"),
    path("shows/<int:show_id>/seasons/<int:season_number>", view=season, name="season"),
    path("dashboard/", view=dashboard, name="dashboard"),
    path("search/", view=search, name="search"),
]
