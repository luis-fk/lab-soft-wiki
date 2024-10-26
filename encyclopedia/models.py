from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.name

class Endereco(models.Model):
    cidade = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    rua = models.CharField(max_length=255)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.rua}, {self.numero}, {self.cidade}"

class Denuncia(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    validacao = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Historico(models.Model):
    num_changes = models.IntegerField()
    text_changes = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('Artigo', on_delete=models.CASCADE)

    def __str__(self):
        return f"History of Article {self.article.title}"

class Artigo(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    views = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)  # Armazenando apenas o ID do usuário

    def __str__(self):
        return self.title

class Comentario(models.Model):
    text = models.TextField()
    likes = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    user_id = models.IntegerField(default=0)
    article_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by User {self.user_id} on Article {self.article_id}"
