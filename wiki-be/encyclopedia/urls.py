from django.urls import path

# Importe as views específicas dos arquivos em `views`
from .views import (
    article_view,
    comentary_view,
    denuncia_view,
    endereco_view,
    user_view,
    siteinfo_view,
    mapa_view,
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
    path("user/list/", user_view.list_users, name="list_users"),  # Lista os usuários mais recentes (20 por padrão)
    path("user/list/<int:quantity>/", user_view.list_users, name="list_users_quantity"),  # Especifica a quantidade de usuários a listar
    path("user/detail/<int:id>/", user_view.get_user_by_id, name="get_user_by_id"),  # Obtém usuário pelo ID
    path("user/detail/email/<str:email>/", user_view.get_user_by_email, name="get_user_by_email"),  # Obtém usuário pelo email
    path("user/delete/<int:user_id>/", user_view.delete_user, name="delete_user"),
    path("user/update/<int:user_id>/", user_view.update_user, name="update_user"),
    path("user/update_password/<int:user_id>/", user_view.update_user_password, name="update_user_password"),
    path("user/check_login_user/", user_view.check_login_user, name='check_login_user'),
    
    # URLs para Article (article_view.py)
    path("article/create/", article_view.create_artigo, name="create_artigo"),
    path("article/list/", article_view.list_articles, name="list_articles"),
    path("article/list/<int:quantity>/", article_view.list_articles, name="list_articles_quantity"),
    path("article/detail/<int:id>/", article_view.get_article_by_id, name="get_article_by_id"),
    path("article/delete/<int:article_id>/", article_view.delete_artigo, name="delete_artigo"),
    path("article/update/<int:article_id>/", article_view.update_artigo, name="update_artigo"),

    # URLs para Commentary (comentary_view.py)
    path("commentary/create/", comentary_view.create_comentary, name="create_comentary"),
    path("commentary/list/<int:article_id>/", comentary_view.list_comments_by_article, name='list_comments_by_article'),  # Com ID, mostra um usuário específico
    path("commentary/delete/<int:commentary_id>/", comentary_view.delete_comment, name="delete_comment"),
    path("commentary/update/<int:commentary_id>/", comentary_view.update_comment, name="update_comment"),
    

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
    
    #URLs para SiteInfo (siteinfo_view.py)
    path("siteinfo/", siteinfo_view.list_siteinfos, name="list_siteinfos"),
    path("siteinfo/create/", siteinfo_view.create_siteinfo, name="create_siteinfo"),
    path("siteinfo/update/<int:siteinfo_id>/", siteinfo_view.update_siteinfo, name="update_siteinfo"),
    path("siteinfo/delete/<int:siteinfo_id>/", siteinfo_view.delete_siteinfo, name="delete_siteinfo"),
    
    #URLs para envio de mapas (mapa_view.py)
    
    path("mapa/nao-trabalhados/", mapa_view.mapa_nao_trabalhados, name="mapa_nao_trabalhados"),
    path("mapa/incidencia-aedes/", mapa_view.mapa_incidencia_aedes, name="mapa_incidencia_aedes"),
    path("mapa/tratamento-imoveis/", mapa_view.mapa_tratamento_imoveis, name="mapa_tratamento_imoveis"),
]
