from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    # URLs existentes
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.entry, name="entry"),
    path("new_page/", views.newPage, name="newPage"),
    path("edit/<str:entry>/", views.edit, name="edit"),
    path("random/", views.randomPage, name="random"),

    # URLs para Usuário
    path("user/create/", views.create_user, name="create_user"),
    path("user/list/", views.list_user, name="list_user"),
    path("user/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("user/update/<int:user_id>/", views.update_user, name="update_user"),

    # URLs para Article
    path("article/create/", views.create_artigo, name="create_artigo"),
    path("article/list/", views.list_artigo, name="list_artigo"),
    path("article/delete/<int:artigo_id>/", views.delete_artigo, name="delete_artigo"),
    path("article/update/<int:artigo_id>/", views.update_artigo, name="update_artigo"),

    # URLs para Comentary
    path("comentary/create/", views.create_comentary, name="create_comentary"),
    path("comentary/list/", views.list_comments, name="list_comments"),
    path("comentary/delete/<int:commentary_id>/", views.delete_comment, name="delete_comment"),
    path("comentary/update/<int:commentary_id>/", views.update_comment, name="update_comment"),
]
