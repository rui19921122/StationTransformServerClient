from rest_framework import serializers
from .models import Article, File
from django.contrib.auth.models import User


class FileSer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class ArticleSer(serializers.HyperlinkedModelSerializer):
    create_person = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    menu = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    files = FileSer(many=True,
                    read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'name',
            'create_person',
            'create_time',
            'content',
            'files',
            'menu',
            'url'
        ]

    def create(self, validated_data):
        return Article.objects.create(
            create_person_id=validated_data['create_person_id'],
            content=validated_data['content'],
            menu_id=validated_data['menu_id'],
            name=validated_data['name']
        )

