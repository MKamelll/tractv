from django.urls import path
from .views import shows, season

urlpatterns = [
    path("shows/<int:show_id>", view=shows, name="shows"),
    path("shows/<int:show_id>/seasons/<int:season_number>", view=season, name="season"),
]
