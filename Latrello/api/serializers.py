from django.contrib.auth.models import User
from rest_framework import serializers

from Latrello.models import Card


class CardSerializer(serializers.ModelSerializer):
    # text = serializers.CharField(required=False)
    author = serializers.CharField(default=serializers.CurrentUserDefault(), read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)
    executor = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Card
        fields = ['id', 'status', 'text', 'author', 'author_id', 'executor', 'date_update']

    def validate(self, data):
        if 'executor' in data:
            if data['executor'] == 'null':
                return data
            elif not User.objects.filter(username=data['executor']).exists():
                raise serializers.ValidationError("Нет Юзера с таким именем. Введите пожалуйста другое имя")
            return data
        else:
            return data


class CardCreateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Card
        fields = ['id', 'status', 'text', 'author', 'author_id', 'executor', 'date_create']


class UpdateStatusCardSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault(), read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    executor = serializers.CharField(read_only=True)
    # executor = serializers.IntegerField()

    class Meta:
        model = Card
        fields = ['id', 'status', 'author', 'executor']

