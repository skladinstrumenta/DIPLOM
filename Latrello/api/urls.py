from django.urls import path, include

from Latrello.api.resources import CardListAPIView, CardUpdateAPIView, CardDeleteAPIView
from rest_framework import routers

# from Latrello.api.resources import CardViewSet

# router = routers.DefaultRouter()
# router.register(r'cards', CardViewSet)
# print(router.urls)

urlpatterns = [
    # path('', include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
    path('cards/', CardListAPIView.as_view()),
    path('cards/update/<int:pk>/', CardUpdateAPIView.as_view()),
    path('cards/delete/<int:pk>/', CardDeleteAPIView.as_view()),

]