from . import views
from django.urls import path

urlpatterns = [
    path("add_manually_post/", views.add_manually_post, name="add_manually_post"),
    path("api/mark/", views.api_mark_attendance, name="api_mark_attendance"),
    path("submitted/", views.submitted, name="submitted"),
]
