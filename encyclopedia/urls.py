from django.urls import path

# Importe as views específicas dos arquivos em `views`
from .views import (
    article_view,
    comentary_view,
    denuncia_view,
    endereco_view,
    user_view,
    view  # Certifique-se de que `view.py` está corretamente importado
)

app_name = "encyclopedia"

urlpatterns = [
    # URLs existentes
    path("", view.index, name="index"),  # Certifique-se de que `view.py` tem uma função chamada `index`
    path("wiki/<str:entry>/", view.entry, name="entry"),
    path("new_page/", view.newPage, name="newPage"),
    path("edit/<str:entry>/", view.edit, name="edit"),
    path("random/", view.randomPage, name="random"),

    # URLs para Usuário (user_view.py)
    path("user/create/", user_view.create_user, name="create_user"),
    path("user/list/", user_view.list_user, name="list_user"),
    path("user/delete/<int:user_id>/", user_view.delete_user, name="delete_user"),
    path("user/update/<int:user_id>/", user_view.update_user, name="update_user"),

    # URLs para Article (article_view.py)
    path("article/create/", article_view.create_artigo, name="create_artigo"),
    path("article/list/", article_view.list_artigo, name="list_artigo"),
    path("article/delete/<int:artigo_id>/", article_view.delete_artigo, name="delete_artigo"),
    path("article/update/<int:artigo_id>/", article_view.update_artigo, name="update_artigo"),

    # URLs para Comentary (comentary_view.py)
    path("comentary/create/", comentary_view.create_comentary, name="create_comentary"),
    path("comentary/list/", comentary_view.list_comments, name="list_comments"),
    path("comentary/delete/<int:commentary_id>/", comentary_view.delete_comment, name="delete_comment"),
    path("comentary/update/<int:commentary_id>/", comentary_view.update_comment, name="update_comment"),

    # URLs para Endereco (endereco_view.py)
    path("endereco/create/", endereco_view.create_endereco, name="create_endereco"),
    path("endereco/list/", endereco_view.list_enderecos, name="list_enderecos"),
    path("endereco/update/<int:endereco_id>/", endereco_view.update_endereco, name="update_endereco"),
    path("endereco/delete/<int:endereco_id>/", endereco_view.delete_endereco, name="delete_endereco"),

    # URLs para Denuncia (denuncia_view.py)
    path("denuncia/create/", denuncia_view.create_denuncia, name="create_denuncia"),
    path("denuncia/list/", denuncia_view.list_denuncias, name="list_denuncias"),
    path("denuncia/update/<int:denuncia_id>/", denuncia_view.update_denuncia, name="update_denuncia"),
    path("denuncia/delete/<int:denuncia_id>/", denuncia_view.delete_denuncia, name="delete_denuncia"),
]
