from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.index, name="index"),
    path("project/<int:pk>/", views.project_detail, name="project_detail"),
    path("scrape/new/", views.new_scrape, name="new_scrape"),
    path("task/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/", views.task_history, name="task_history"),
]