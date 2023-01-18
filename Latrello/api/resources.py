from types import NoneType

from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from Latrello.api.permissions import IsOwnerOrSuperuser
from Latrello.api.serializers import CardSerializer
from Latrello.models import Card


class CardListAPIView(generics.ListCreateAPIView):
    serializer_class = CardSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Card.objects.all()
        user = self.request.user
        if not user.is_superuser:
            queryset = Card.objects.filter(author=user)
            return queryset
        return queryset


class CardUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]


class CardDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    # permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
#
#
# class StatusCardUpView(generics.RetrieveUpdateAPIView):
#     pass


# class CardViewSet(viewsets.ModelViewSet):
#     queryset = Card.objects.all()
#     serializer_class = CardSerializer


    # @action(methods=['get'], detail=False)
    # def status_new(self, request, pk=None):
    #     aut = Card.objects.filter(status=1)
    #     return Response({'aut': [[a.text, a.author.username, a.date_update] for a in aut]})
    #
    # @action(methods=['get'], detail=False)
    # def status_process(self, request):
    #     aut = Card.objects.filter(status=2)
    #     return Response({'aut': [(a.text, a.author, a.date_create) for a in aut]})
    #
    # @action(methods=['get'], detail=False)
    # def status_in_qa(self, request):
    #     aut = Card.objects.filter(status=3)
    #     return Response({'aut': [[a.text, a.author.username, a.executor.username, a.date_update] for a in aut]})
    #
    # @action(methods=['get'], detail=False)
    # def status_ready(self, request):
    #     aut = Card.objects.filter(status=4)
    #     return Response({'aut': [a.text for a in aut]})
    #
    # @action(methods=['get'], detail=False)
    # def status_done(self, request):
    #     aut = Card.objects.filter(status=5)
    #     return Response({'aut': [a.text for a in aut]})