from datetime import timezone, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from Latrello.forms import CreateUserForm
from Latrello.models import Card


# class ProductListView(ListView):
#     model = Product
#     template_name = 'index.html'


def index(request):
    session_count = 0
    if request.user.is_authenticated:
        session_count = request.session.get('session_count', 1)
        request.session['session_count'] = session_count + 1
        if not request.user.is_superuser:
            request.session.set_expiry(60)
    return render(request, 'index.html', context={'count': session_count})


class CreateNewUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'registration/registration.html'
    success_url = '/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid


class CardListView(ListView):
    model = Card
    template_name = 'cards.html'
    extra_context = {'title': 'карточки'}
    #
    # def get(self, request):
    #     session_count = 0
    #     if request.user.is_authenticated:
    #         session_count = request.session.get('session_count', 1)
    #         request.session['session_count'] = session_count + 1
    #         if not request.user.is_superuser:
    #             request.session.set_expiry(60)
    #     return render(request, 'index.html', context={'count': session_count})
