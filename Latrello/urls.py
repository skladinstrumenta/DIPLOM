from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from Latrello.views import CardListView, CreateNewUserView, CardCreateView, CardUpdateView, CardDeleteView, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreateNewUserView.as_view(), name='register'),
    path('cards/', CardListView.as_view(), name='cards'),
    path('cards/new/', CardCreateView.as_view(), name='createcard'),
    path('cards/update/<int:pk>', CardUpdateView.as_view(), name='updatecard'),
    path('cards/delete/<int:pk>', CardDeleteView.as_view(), name='deletecard')


]
