import functools
import atexit
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from encyclopedia.models import Artigo, Comentario, Denuncia, Endereco, User

# Lista global para armazenar os nomes dos testes que falharam
failed_tests = []

def print_test_result(func):
    """
    Decorator para imprimir o resultado do teste e registrar falhas.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            print(f"✅ {func.__name__} passed")
        except AssertionError:
            print(f"❌ {func.__name__} failed")
            failed_tests.append(func.__name__)
            raise
    return wrapper

@atexit.register
def print_failed_tests():
    """
    Função registrada para ser executada ao final da execução dos testes.
    Imprime um resumo dos testes que falharam ou apresentaram erros.
    """
    if failed_tests:
        print("\n❌ Testes que falharam ou apresentaram erros:")
        for test in failed_tests:
            print(f"❌ {test}")
    else:
        print("\n✅ Todos os testes passaram com sucesso!")

class ApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        User = get_user_model()
        # Criação de usuários
        cls.user = User.objects.create_user(username='user', password='password', email='user@example.com')
        cls.staff_user = User.objects.create_user(username='admin', password='password', is_staff=True, email='admin@example.com')

        # Criação de um artigo e outros objetos relacionados
        cls.artigo = Artigo.objects.create(title='Test Article', text='This is a test article.', user=cls.user)
        cls.comentario = Comentario.objects.create(text='Test comment', article=cls.artigo, user=cls.user)
        cls.endereco = Endereco.objects.create(cidade='São Paulo', bairro='Centro', rua='Rua A', numero='123')

        # URLs
        cls.create_comment_url = reverse('encyclopedia:create_comentary')
        cls.list_comments_url = reverse('encyclopedia:list_comments')
        cls.delete_comment_url = reverse('encyclopedia:delete_comment', args=[cls.comentario.id])
        cls.create_denuncia_url = reverse('encyclopedia:create_denuncia')

    @print_test_result
    def test_create_comment_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {'text': 'A new comment', 'article': self.artigo.id}
        response = self.client.post(self.create_comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'A new comment')

    @print_test_result
    def test_create_comment_as_unauthenticated_user(self):
        data = {'text': 'A new comment', 'article': self.artigo.id}
        response = self.client.post(self.create_comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_list_comments(self):
        response = self.client.get(self.list_comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], 'Test comment')

    @print_test_result
    def test_delete_comment_as_admin(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.delete_comment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Comment deleted successfully.')

    @print_test_result
    def test_delete_comment_as_non_admin(self):
        self.client.force_authenticate(user=self.user)  # Usuário não admin
        response = self.client.delete(self.delete_comment_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_create_denuncia_with_address(self):
        self.client.force_authenticate(user=self.user)
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

    @print_test_result
    def test_create_denuncia_with_invalid_address(self):
        self.client.force_authenticate(user=self.user)
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

    @print_test_result
    def test_create_denuncia_as_unauthenticated_user(self):
        data = {
            'title': 'Denúncia Teste',
            'text': 'Texto da denúncia.',
            'endereco': {
                'cidade': 'São Paulo',
                'bairro': 'Centro',
                'rua': 'Rua B',
                'numero': '456'
            }
        }
        response = self.client.post(self.create_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ArtigoApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        User = get_user_model()
        cls.user = User.objects.create_user(username='user', password='password', email='user@example.com')
        cls.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True, email='admin@example.com')
        cls.artigo = Artigo.objects.create(title='Test Artigo', text='This is a test artigo.', user=cls.user)
        
        # URLs
        cls.create_artigo_url = reverse('encyclopedia:create_artigo')
        cls.list_artigos_url = reverse('encyclopedia:list_artigo')
        cls.update_artigo_url = reverse('encyclopedia:update_artigo', args=[cls.artigo.id])
        cls.delete_artigo_url = reverse('encyclopedia:delete_artigo', args=[cls.artigo.id])

    @print_test_result
    def test_create_artigo_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'New Artigo', 'text': 'This is a new artigo.'}
        response = self.client.post(self.create_artigo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Artigo')

    @print_test_result
    def test_create_artigo_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Unauthorized Artigo', 'text': 'This should not be created.'}
        response = self.client.post(self.create_artigo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_list_artigos(self):
        response = self.client.get(self.list_artigos_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Artigo')

    @print_test_result
    def test_update_artigo_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'Updated Artigo'}
        response = self.client.put(self.update_artigo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Artigo')

    @print_test_result
    def test_update_artigo_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Invalid Update'}
        response = self.client.put(self.update_artigo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_delete_artigo_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.delete_artigo_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Artigo deletado com sucesso.')

    @print_test_result
    def test_delete_artigo_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_artigo_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EnderecoApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.endereco = Endereco.objects.create(cidade='São Paulo', bairro='Centro', rua='Rua A', numero='123')
        
        # URLs
        cls.create_endereco_url = reverse('encyclopedia:create_endereco')
        cls.list_enderecos_url = reverse('encyclopedia:list_enderecos')
        cls.update_endereco_url = reverse('encyclopedia:update_endereco', args=[cls.endereco.id])
        cls.delete_endereco_url = reverse('encyclopedia:delete_endereco', args=[cls.endereco.id])

    @print_test_result
    def test_create_endereco(self):
        data = {'cidade': 'Rio de Janeiro', 'bairro': 'Copacabana', 'rua': 'Rua B', 'numero': '456'}
        response = self.client.post(self.create_endereco_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cidade'], 'Rio de Janeiro')

    @print_test_result
    def test_create_endereco_with_invalid_data(self):
        data = {'cidade': '', 'bairro': 'Copacabana', 'rua': 'Rua B', 'numero': '456'}
        response = self.client.post(self.create_endereco_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @print_test_result
    def test_list_enderecos(self):
        response = self.client.get(self.list_enderecos_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cidade'], 'São Paulo')

    @print_test_result
    def test_update_endereco_as_admin(self):
        User = get_user_model()
        admin_user = User.objects.create_user(username='admin_update_endereco', password='password', is_staff=True, email='admin_update_endereco@example.com')
        self.client.force_authenticate(user=admin_user)
        data = {'cidade': 'São Paulo', 'bairro': 'Vila Mariana'}
        response = self.client.put(self.update_endereco_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bairro'], 'Vila Mariana')

    @print_test_result
    def test_update_endereco_as_non_admin(self):
        User = get_user_model()
        user = User.objects.create_user(username='user_update_endereco', password='password', email='user_update_endereco@example.com')
        self.client.force_authenticate(user=user)
        data = {'cidade': 'São Paulo', 'bairro': 'Vila Mariana'}
        response = self.client.put(self.update_endereco_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_delete_endereco_as_admin(self):
        User = get_user_model()
        admin_user = User.objects.create_user(username='admin_delete_endereco', password='password', is_staff=True, email='admin_delete_endereco@example.com')
        self.client.force_authenticate(user=admin_user)
        response = self.client.delete(self.delete_endereco_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Endereço deletado com sucesso.')

    @print_test_result
    def test_delete_endereco_as_non_admin(self):
        User = get_user_model()
        user = User.objects.create_user(username='user_delete_endereco', password='password', email='user_delete_endereco@example.com')
        self.client.force_authenticate(user=user)
        response = self.client.delete(self.delete_endereco_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        User = get_user_model()
        cls.user = User.objects.create_user(username='user', password='password', email='user@example.com')
        cls.admin_user = User.objects.create_user(username='admin', password='password', email='admin@example.com', is_staff=True)
        
        # URLs
        cls.create_user_url = reverse('encyclopedia:create_user')
        cls.list_users_url = reverse('encyclopedia:list_user')
        cls.delete_user_url = reverse('encyclopedia:delete_user', args=[cls.user.id])
        cls.update_user_url = reverse('encyclopedia:update_user', args=[cls.user.id])

    @print_test_result
    def test_create_user_with_valid_data(self):
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}
        response = self.client.post(self.create_user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')

    @print_test_result
    def test_create_user_with_invalid_data(self):
        data = {'username': '', 'email': 'invalidemail', 'password': 'short'}
        response = self.client.post(self.create_user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @print_test_result
    def test_list_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Deve listar 2 usuários

    @print_test_result
    def test_list_users_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_delete_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Usuário deletado com sucesso.')

    @print_test_result
    def test_delete_user_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_update_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'username': 'updateduser'}
        response = self.client.put(self.update_user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')

    @print_test_result
    def test_update_user_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {'username': 'invalidupdate'}
        response = self.client.put(self.update_user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DenunciaApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        User = get_user_model()
        cls.user = User.objects.create_user(username='user', password='password', email='user@example.com')
        cls.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True, email='admin@example.com')

        cls.endereco = Endereco.objects.create(cidade='São Paulo', bairro='Centro', rua='Rua A', numero='123')
        cls.denuncia = Denuncia.objects.create(title='Test Denuncia', text='This is a test denuncia.', user=cls.user, endereco=cls.endereco)

        # URLs
        cls.create_denuncia_url = reverse('encyclopedia:create_denuncia')
        cls.list_denuncias_url = reverse('encyclopedia:list_denuncias')
        cls.update_denuncia_url = reverse('encyclopedia:update_denuncia', args=[cls.denuncia.id])
        cls.delete_denuncia_url = reverse('encyclopedia:delete_denuncia', args=[cls.denuncia.id])

    @print_test_result
    def test_create_denuncia_as_authenticated_user(self):
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
        self.assertEqual(response.data['title'], 'New Denuncia')

    @print_test_result
    def test_create_denuncia_as_unauthenticated_user(self):
        data = {
            'title': 'Denúncia Teste',
            'text': 'Texto da denúncia.',
            'endereco': {
                'cidade': 'São Paulo',
                'bairro': 'Centro',
                'rua': 'Rua B',
                'numero': '456'
            }
        }
        response = self.client.post(self.create_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_list_denuncias(self):
        response = self.client.get(self.list_denuncias_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Denuncia')

    @print_test_result
    def test_update_denuncia_by_author(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Denuncia'}
        response = self.client.put(self.update_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Denuncia')

    @print_test_result
    def test_update_denuncia_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'Admin Updated Denuncia'}
        response = self.client.put(self.update_denuncia_url, data, format='json')
        # Ajuste conforme a lógica de permissões da sua aplicação
        # Se administradores podem atualizar, espere 200 OK
        # Caso contrário, ajuste para 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Admin Updated Denuncia')

    @print_test_result
    def test_delete_denuncia_by_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_denuncia_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Denúncia deletada com sucesso.')

    @print_test_result
    def test_delete_denuncia_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.delete_denuncia_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Denúncia deletada com sucesso.')

    @print_test_result
    def test_delete_denuncia_by_non_author(self):
        User = get_user_model()
        non_author = User.objects.create_user(username='non_author', password='password', email='non_author@example.com')
        self.client.force_authenticate(user=non_author)
        response = self.client.delete(self.delete_denuncia_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @print_test_result
    def test_update_denuncia_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': ''}  # Título inválido
        response = self.client.put(self.update_denuncia_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
