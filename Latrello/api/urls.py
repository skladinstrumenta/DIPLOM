from django.urls import path
from rest_framework.authtoken import views

from Latrello.api.resources import *

urlpatterns = [

    path('api-token-auth/', views.obtain_auth_token),
    path('cards/', CardListAPIView.as_view()),
    path('cards/create/', CardCreateAPIView.as_view()),
    path('cards/<int:pk>/', CardDetailAPIView.as_view()),
    path('cards/<int:pk>/update/', CardUpdateAPIView.as_view()),
    path('cards/<int:pk>/delete/', CardDeleteAPIView.as_view()),
    path('cards/<int:pk>/status-up/', StatusUpdateAPIView.as_view()),
    path('cards/<int:pk>/status-down/', StatusUpdateAPIView.as_view())

]