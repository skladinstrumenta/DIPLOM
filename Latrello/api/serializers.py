from rest_framework import serializers

from Latrello.models import Card


class CardSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default=1)
    class Meta:
        model = Card
        # fields = '__all__'
        fields = ['id', 'status', 'text', 'author']
