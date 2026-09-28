from . import views
from django.urls import path

urlpatterns = [
    path("", views.faculty_view, name="faculty_view"),
    path("add_manually", views.add_manually, name="add_manually"),
    path("export_excel", views.export_attendance_excel, name="export_attendance_excel"),
]
