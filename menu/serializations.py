from rest_framework import serializers
from .models import Menu


class MenuSer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['name', 'parent', 'id']

    def create(self, validated_data):
        pass
