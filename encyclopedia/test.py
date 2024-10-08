from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from encyclopedia.models import Artigo, Comentario, Denuncia, Endereco

class ApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        # Criação de usuários
        self.user = User.objects.create_user(username='user', password='password', email='user@example.com')
        self.staff_user = User.objects.create_user(username='admin', password='password', is_staff=True, email='admin@example.com')

        # Criação de um artigo e outros objetos relacionados
        self.artigo = Artigo.objects.create(title='Test Article', text='This is a test article.', user=self.user)
        self.comentario = Comentario.objects.create(text='Test comment', article=self.artigo, user=self.user)
        self.endereco = Endereco.objects.create(cidade='São Paulo', bairro='Centro', rua='Rua A', numero='123')

        # URLs
        self.create_comment_url = reverse('encyclopedia:create_comentary')
        self.list_comments_url = reverse('encyclopedia:list_comments')
        self.delete_comment_url = reverse('encyclopedia:delete_comment', args=[self.comentario.id])
        self.create_denuncia_url = reverse('encyclopedia:create_denuncia')

    def test_create_comment_as_authenticated_user(self):
        self.client.login(username='user', password='password')
        data = {'text': 'A new comment', 'article': self.artigo.id}
        response = self.client.post(self.create_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'A new comment')
        print("✅ test_create_comment_as_authenticated_user passed")

    def test_create_comment_as_unauthenticated_user(self):
        data = {'text': 'A new comment', 'article': self.artigo.id}
        response = self.client.post(self.create_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Corrigido para 403
        print("✅ test_create_comment_as_unauthenticated_user passed")

    def test_list_comments(self):
        response = self.client.get(self.list_comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], 'Test comment')
        print("✅ test_list_comments passed")

    def test_delete_comment_as_admin(self):
        self.client.login(username='admin', password='password')
        response = self.client.delete(self.delete_comment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Comment deleted successfully.')
        print("✅ test_delete_comment_as_admin passed")

    def test_delete_comment_as_non_admin(self):
        self.client.force_login(self.user)  # Usando force_login
        response = self.client.delete(self.delete_comment_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("✅ test_delete_comment_as_non_admin passed")

    def test_create_denuncia_with_address(self):
        self.client.login(username='user', password='password')
        data = {
            'title': 'Denúncia Teste',
            'text': 'Texto da denúncia.',
            'endereco': {
                'cidade': 'São Paulo',
                'bairro': 'Centro',
                'rua': 'Rua B',
                'numero': '456',
                'complemento': 'Apto 101'
            }
        }
        response = self.client.post(self.create_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Denúncia Teste')
        self.assertEqual(response.data['endereco']['cidade'], 'São Paulo')
        print("✅ test_create_denuncia_with_address passed")

    def test_create_denuncia_with_invalid_address(self):
        self.client.login(username='user', password='password')
        data = {
            'title': 'Denúncia Teste',
            'text': 'Texto da denúncia.',
            'endereco': {
                'cidade': '',  # Campo inválido
                'bairro': 'Centro',
                'rua': 'Rua B',
                'numero': '456'
            }
        }
        response = self.client.post(self.create_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("✅ test_create_denuncia_with_invalid_address passed")
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from encyclopedia.models import Artigo, User


class ArtigoApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='password', email='user@example.com')
        self.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.artigo = Artigo.objects.create(title='Test Artigo', text='This is a test artigo.', user=self.user)
        
        # URLs
        self.create_artigo_url = reverse('encyclopedia:create_artigo')
        self.list_artigos_url = reverse('encyclopedia:list_artigo')
        self.update_artigo_url = reverse('encyclopedia:update_artigo', args=[self.artigo.id])
        self.delete_artigo_url = reverse('encyclopedia:delete_artigo', args=[self.artigo.id])

    def test_create_artigo(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'New Artigo', 'text': 'This is a new artigo.'}
        response = self.client.post(self.create_artigo_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("✅ test_create_artigo passed")

    def test_list_artigos(self):
        response = self.client.get(self.list_artigos_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print("✅ test_list_artigos passed")

    def test_update_artigo(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'Updated Artigo'}
        response = self.client.put(self.update_artigo_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ test_update_artigo passed")

    def test_delete_artigo(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.delete_artigo_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ test_delete_artigo passed")


from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from encyclopedia.models import Endereco


class EnderecoApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.endereco = Endereco.objects.create(cidade='São Paulo', bairro='Centro', rua='Rua A', numero='123')
        
        # URLs
        self.create_endereco_url = reverse('encyclopedia:create_endereco')
        self.list_enderecos_url = reverse('encyclopedia:list_enderecos')
        self.update_endereco_url = reverse('encyclopedia:update_endereco', args=[self.endereco.id])
        self.delete_endereco_url = reverse('encyclopedia:delete_endereco', args=[self.endereco.id])

    def test_create_endereco(self):
        data = {'cidade': 'Rio de Janeiro', 'bairro': 'Copacabana', 'rua': 'Rua B', 'numero': '456'}
        response = self.client.post(self.create_endereco_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("✅ test_create_endereco passed")

    def test_list_enderecos(self):
        response = self.client.get(self.list_enderecos_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print("✅ test_list_enderecos passed")

    def test_update_endereco(self):
        data = {'cidade': 'São Paulo', 'bairro': 'Vila Mariana'}
        response = self.client.put(self.update_endereco_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ test_update_endereco passed")

    def test_delete_endereco(self):
        response = self.client.delete(self.delete_endereco_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ test_delete_endereco passed")


from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from encyclopedia.models import User


class UserApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='user', password='password', email='user@example.com')
        self.admin_user = get_user_model().objects.create_user(username='admin', password='password', email='admin@example.com', is_staff=True)

        # URLs
        self.create_user_url = reverse('encyclopedia:create_user')
        self.list_users_url = reverse('encyclopedia:list_user')
        self.delete_user_url = reverse('encyclopedia:delete_user', args=[self.user.id])
        self.update_user_url = reverse('encyclopedia:update_user', args=[self.user.id])

    def test_create_user(self):
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("✅ test_create_user passed")

    def test_list_users(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Deve listar 2 usuários
        print("✅ test_list_users passed")

    def test_delete_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ test_delete_user_as_admin passed")

    def test_update_user(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'username': 'updateduser'}
        response = self.client.put(self.update_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ test_update_user passed")



from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from encyclopedia.models import Denuncia, User, Endereco


class DenunciaApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='password', email='user@example.com')
        self.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True)

        self.endereco = Endereco.objects.create(cidade='São Paulo', bairro='Centro', rua='Rua A', numero='123')
        self.denuncia = Denuncia.objects.create(title='Test Denuncia', text='This is a test denuncia.', user=self.user, endereco=self.endereco)

        # URLs
        self.create_denuncia_url = reverse('encyclopedia:create_denuncia')
        self.list_denuncias_url = reverse('encyclopedia:list_denuncias')
        self.update_denuncia_url = reverse('encyclopedia:update_denuncia', args=[self.denuncia.id])
        self.delete_denuncia_url = reverse('encyclopedia:delete_denuncia', args=[self.denuncia.id])

    def test_create_denuncia(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Denuncia',
            'text': 'This is a new denuncia.',
            'endereco': {
                'cidade': 'Rio de Janeiro',
                'bairro': 'Copacabana',
                'rua': 'Rua B',
                'numero': '456'
            }
        }
        response = self.client.post(self.create_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("✅ test_create_denuncia passed")

    def test_list_denuncias(self):
        response = self.client.get(self.list_denuncias_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Denuncia')
        print("✅ test_list_denuncias passed")

    def test_update_denuncia_by_author(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Denuncia'}
        response = self.client.put(self.update_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Denuncia')
        print("✅ test_update_denuncia_by_author passed")

    def test_update_denuncia_by_non_author(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'Invalid Update'}
        response = self.client.put(self.update_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("✅ test_update_denuncia_by_non_author passed")

    def test_delete_denuncia_by_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_denuncia_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ test_delete_denuncia_by_author passed")

    def test_delete_denuncia_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.delete_denuncia_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ test_delete_denuncia_by_admin passed")

    def test_delete_denuncia_by_non_author(self):
        non_author = User.objects.create_user(username='non_author', password='password')
        self.client.force_authenticate(user=non_author)
        response = self.client.delete(self.delete_denuncia_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("✅ test_delete_denuncia_by_non_author passed")
