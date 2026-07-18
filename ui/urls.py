from django.urls import path
from .views import shows

urlpatterns = [path("shows/<int:show_id>", view=shows, name="shows")]
