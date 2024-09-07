from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.entry, name="entry"),
    path("new_page/", views.newPage, name="newPage"),
    path("edit/<str:entry>/", views.edit, name="edit"),
    path("random/", views.randomPage, name="random"),
]
