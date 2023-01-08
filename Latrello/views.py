from datetime import timezone, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

from Latrello.forms import CreateUserForm, CardCreateForm, CardUpdateForm
from Latrello.models import Card


# def index(request):
#     session_count = 0
#     if request.user.is_authenticated:
#         session_count = request.session.get('session_count', 1)
#         request.session['session_count'] = session_count + 1
#         # if not request.user.is_superuser:
#         #     request.session.set_expiry(60)
#     return render(request, 'index.html', context={'count': session_count})


class HomePageView(TemplateView):
    template_name = 'index.html'


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


class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = 'cards.html'
    extra_context = {'form': CardCreateForm}
    login_url = '/'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Card.objects.filter(author=self.request.user)
            return queryset
        queryset = Card.objects.all()
        return queryset


class CardCreateView(CreateView):
    template_name = 'cards.html'
    http_method_names = ['post']
    form_class = CardCreateForm
    success_url = '/cards'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)


class CardUpdateView(UpdateView):
    model = Card
    form_class = CardUpdateForm
    template_name = 'updatecard.html'
    success_url = '/cards'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class CardDeleteView(DeleteView):
    model = Card
    success_url = '/cards'


class StatusUpView(UpdateView):
    model = Card
    success_url = reverse_lazy('cards')
    fields = ['status']
    template_name = 'cards.html'

    def form_valid(self, form):
        obj = self.get_object()
        obj.update(status=F('status') + 1)
        return super().form_valid(form)


class StatusBackView(UpdateView):
    pass
