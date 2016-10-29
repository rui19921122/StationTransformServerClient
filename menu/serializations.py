from rest_framework import serializers
from .models import Menu
from django.contrib.auth.models import User


class MenuSer(serializers.ModelSerializer):
    own_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset='own_id', required=False)
    url = serializers.HyperlinkedIdentityField(view_name='menu-articles')

    class Meta:
        model = Menu
        fields = ['name', 'parent', 'id', 'own_id', 'url']

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)


class AddChildSer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True)


class MenuAdministratorSer(serializers.Serializer):
    pk = serializers.IntegerField(required=True)
    username = serializers.StringRelatedField(read_only=True,
                                              )

    def validate_pk(self, value):
        if User.objects.filter(pk=value).exists():
            return value
        else:
            raise serializers.ValidationError("{}用户不存在".format(value))
