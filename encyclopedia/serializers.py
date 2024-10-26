from rest_framework import serializers
from .models import User, Endereco, Denuncia, Historico, Artigo, Comentario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'city', 'role', 'password', 'date_joined')
        read_only_fields = ['password']  # Tornar 'password' somente de leitura

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

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        denuncia = Denuncia.objects.create(endereco=endereco, **validated_data)
        return denuncia

class HistoricoSerializer(serializers.ModelSerializer):
    edited_by = UserSerializer(read_only=True)
    article = ArtigoSerializer(read_only=True)

    class Meta:
        model = Historico
        fields = ('id', 'num_changes', 'text_changes', 'edited_by', 'article')

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'text', 'likes', 'edited', 'user_name', 'article_id', 'created_at']
        read_only_fields = ['id', 'created_at']
