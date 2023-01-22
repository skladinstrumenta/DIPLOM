from django.urls import path, include
from rest_framework.authtoken import views

from Latrello.api.resources import *
from rest_framework import routers

# from Latrello.api.resources import CardViewSet
#
# router = routers.DefaultRouter()
# router.register(r'cards', CardViewSet)
# # print(router.urls)

urlpatterns = [
    # path('', include(router.urls)),
    # path('drf-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('cards/', CardListAPIView.as_view()),
    path('cards/<int:pk>/', CardDetailAPIView.as_view()),
    path('cards/<int:pk>/update/', CardUpdateAPIView.as_view()),
    path('cards/<int:pk>/delete/', CardDeleteAPIView.as_view()),
    path('cards/<int:pk>/status-up/', StatusUpdateAPIView.as_view()),
    path('cards/<int:pk>/status-down/', StatusUpdateAPIView.as_view())

]