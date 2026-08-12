from django.urls import path
from .views import shows, season, dashboard, search, status_update

urlpatterns = [
    path("shows/<int:show_id>", view=shows, name="shows"),
    path("shows/<int:show_id>/seasons/<int:season_number>", view=season, name="season"),
    path("search/", view=search, name="search"),
    path(
        "status/update/<int:show_id>/<str:status>",
        view=status_update,
        name="status_update",
    ),
    path("", view=dashboard, name="dashboard"),
]
