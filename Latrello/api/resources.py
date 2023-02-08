from django.contrib.auth.models import User
from rest_framework import generics, permissions, exceptions

from Latrello.api.permissions import IsOwnerOrSuperuser
from Latrello.api.serializers import CardSerializer, UpdateStatusCardSerializer, CardCreateSerializer
from Latrello.models import Card
from rest_framework.filters import SearchFilter, OrderingFilter


class CardListAPIView(generics.ListAPIView):
    serializer_class = CardSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['=status']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Card.objects.all()
        user = self.request.user
        if not user.is_superuser:
            queryset = Card.objects.filter(author=user)
            return queryset
        return queryset


class CardCreateAPIView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardDetailAPIView(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]


class CardUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    def perform_update(self, serializer):
        obj = self.get_object()
        user = self.request.user

        if 'executor' in serializer.validated_data:
            executor = serializer.validated_data['executor']

            if executor == 'null':
                serializer.save(executor=None)

            else:
                if not user.is_superuser:
                    if user == obj.author == executor:
                        serializer.save(executor=executor)
                    else:
                        msg = f"You are is not SUPERUSER and can't choose anyone but yourself as the executor. " \
                                  f"Please enter name '{user}' or 'null'"
                        raise exceptions.PermissionDenied(msg)
                else:
                    serializer.save(executor=executor)

        else:
            serializer.save()


class CardDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAdminUser]


class StatusUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = UpdateStatusCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        obj = self.get_object()
        status = obj.status
        request_url = str(serializer.context['request'])

        if user and user.is_authenticated:

            if not user.is_superuser and obj.author != obj.executor:
                msg = "you do not have superuser rights, or the executor must be the same as the author!"
                raise exceptions.PermissionDenied(msg)

            if 'status-up' in request_url:
                if not user.is_superuser and obj.status == 4 or user.is_superuser and obj.status == 5:
                    raise exceptions.ValidationError("You're can't status-up!")
                if not user.is_superuser and obj.author == obj.executor and 4 > obj.status >= 1 or \
                        user.is_superuser and obj.status == 4:
                    status += 1

            elif 'status-down' in request_url:
                if not user.is_superuser and obj.status == 1 or user.is_superuser and obj.status == 4:
                    raise exceptions.ValidationError("You're can't status-down!")
                if not user.is_superuser and obj.author == obj.executor and 4 >= obj.status > 1 or \
                        user.is_superuser and obj.status == 5:
                    status -= 1
            serializer.save(status=status)

        else:
            serializer.save()
