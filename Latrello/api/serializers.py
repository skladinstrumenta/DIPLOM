from rest_framework import serializers

from Latrello.models import Card


class CardSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault(), read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)
    executor = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Card
        fields = ['id', 'status', 'text', 'author', 'author_id', 'executor', 'date_update']


class UpdateStatusCardSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault(), read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    executor = serializers.CharField(read_only=True)
    class Meta:
        model = Card
        fields = ['id', 'status', 'author', 'executor']

