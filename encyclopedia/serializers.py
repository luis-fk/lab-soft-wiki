from rest_framework import serializers
from .models import User, Endereco, Denuncia, Historico, Artigo, Comentario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'cidade', 'role')

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id', 'cidade', 'bairro', 'rua', 'numero', 'complemento')

class ArtigoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Artigo
        fields = ('id', 'title', 'text', 'views', 'user')

class DenunciaSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    endereco = EnderecoSerializer()

    class Meta:
        model = Denuncia
        fields = ('id', 'title', 'text', 'user', 'endereco')

class HistoricoSerializer(serializers.ModelSerializer):
    edited_by = UserSerializer(read_only=True)
    article = ArtigoSerializer(read_only=True)

    class Meta:
        model = Historico
        fields = ('id', 'num_changes', 'text_changes', 'edited_by', 'article')

class ComentarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article = ArtigoSerializer(read_only=True)

    class Meta:
        model = Comentario
        fields = ('id', 'text', 'likes', 'edited', 'user', 'article')
