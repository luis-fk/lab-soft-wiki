from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from encyclopedia.models import Article, User, Comentario, Denuncia, Endereco
from django.contrib.auth.models import User as AuthUser

class EncyclopediaViewsTestCase(APITestCase):

    def setUp(self):
        # Criação de dados para teste
        self.user_admin = AuthUser.objects.create_user(username='admin', password='password123', is_staff=True)
        self.user_normal = AuthUser.objects.create_user(username='normaluser', password='password123')
        self.client.login(username='admin', password='password123')

        # Criar Artigo para testar rota de artigo
        self.article = Article.objects.create(title="Test Article", text="Test Content")

        # Criar Comentário
        self.comentario = Comentario.objects.create(text="Test Comment", article=self.article)

        # Criar Endereço
        self.endereco = Endereco.objects.create(cidade="São Paulo", bairro="Centro", rua="Rua A", numero=123)

        # Criar Denúncia
        self.denuncia = Denuncia.objects.create(title="Test Denuncia", text="Denuncia Text", user=self.user_admin, endereco=self.endereco)

    # Teste para view index
    def test_index_view(self):
        url = reverse('encyclopedia:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para view de entrada (entry)
    def test_entry_view(self):
        url = reverse('encyclopedia:entry', args=[self.article.title])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para criar novo artigo
    def test_create_article_view(self):
        url = reverse('encyclopedia:create_artigo')
        data = {'title': 'New Test Article', 'text': 'Some content for new article'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Teste para listar artigos
    def test_list_article_view(self):
        url = reverse('encyclopedia:list_artigo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para deletar artigo
    def test_delete_article_view(self):
        url = reverse('encyclopedia:delete_artigo', args=[self.article.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para criar usuário
    def test_create_user_view(self):
        url = reverse('encyclopedia:create_user')
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Teste para listar usuários
    def test_list_user_view(self):
        url = reverse('encyclopedia:list_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para deletar usuário
    def test_delete_user_view(self):
        url = reverse('encyclopedia:delete_user', args=[self.user_normal.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para criar comentário
    def test_create_comment_view(self):
        url = reverse('encyclopedia:create_comentary')
        data = {'text': 'New Comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Teste para listar comentários
    def test_list_comments_view(self):
        url = reverse('encyclopedia:list_comments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para deletar comentário
    def test_delete_comment_view(self):
        url = reverse('encyclopedia:delete_comment', args=[self.comentario.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para criar endereço
    def test_create_endereco_view(self):
        url = reverse('encyclopedia:create_endereco')
        data = {'cidade': 'São Paulo', 'bairro': 'Jardins', 'rua': 'Rua B', 'numero': 123}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Teste para listar endereços
    def test_list_enderecos_view(self):
        url = reverse('encyclopedia:list_enderecos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para deletar endereço
    def test_delete_endereco_view(self):
        url = reverse('encyclopedia:delete_endereco', args=[self.endereco.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para criar denúncia
    def test_create_denuncia_view(self):
        url = reverse('encyclopedia:create_denuncia')
        data = {'title': 'Nova Denuncia', 'text': 'Texto de Denuncia', 'user': self.user_admin.id, 'endereco': self.endereco.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Teste para listar denúncias
    def test_list_denuncias_view(self):
        url = reverse('encyclopedia:list_denuncias')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste para deletar denúncia
    def test_delete_denuncia_view(self):
        url = reverse('encyclopedia:delete_denuncia', args=[self.denuncia.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
