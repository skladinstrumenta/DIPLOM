from django.contrib.auth.models import User
from rest_framework import generics, permissions, exceptions

from Latrello.api.permissions import IsOwnerOrSuperuser
from Latrello.api.serializers import CardSerializer, UpdateStatusCardSerializer
from Latrello.models import Card
from rest_framework.filters import SearchFilter, OrderingFilter


class CardListAPIView(generics.ListCreateAPIView):
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
        input_executor = (serializer.validated_data.get('executor')).title()
        list_of_names = [name.username for name in User.objects.all()]
        if input_executor != 'null'.title():

            try:
                validated_executors = User.objects.get(username=input_executor)
                validated_executors_id = validated_executors.id
            except:
                if user.is_superuser:
                    msg_not_name = f"There is no executor with this name in the database! Please enter another name! " \
                               f"Now the database has such names: {list_of_names}"
                else:
                    msg_not_name = f"You can't choose anyone but yourself as the executor. Please enter name '{user}'"
                raise exceptions.APIException(msg_not_name)

            if user and user.is_authenticated:
                if not user.is_superuser and user == obj.author:
                    if validated_executors_id == user.id:
                        serializer.save(executor=validated_executors)
                    else:
                        msg = f"You are is not SUPERUSER and can't choose anyone but yourself as the executor. " \
                              f"Please enter name '{user}'"
                        raise exceptions.APIException(msg)
                elif user.is_superuser:
                    serializer.save(executor=validated_executors)

        else:
            msg_null = 'There is no executor with this name in the database! Please enter another name!'
            raise exceptions.APIException(msg_null)


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
            if 'status-up' in request_url:
                if not user.is_superuser and obj.author == obj.executor and 4 > obj.status >= 1 or \
                        user.is_superuser and obj.status == 4:
                    status += 1

            elif 'status-down' in request_url:
                if not user.is_superuser and obj.author == obj.executor and 4 >= obj.status > 1 or \
                        user.is_superuser and obj.status == 5:
                    status -= 1
            serializer.save(status=status)
        else:
            serializer.save()
