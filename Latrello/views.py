from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

from Latrello.forms import CreateUserForm, CardCreateForm, CardUpdateForm, CardStatusUpForm, CardStatusDownForm, \
    SearchCardForm
from Latrello.models import Card


class SuperUserRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')


class AddUserInFormMixin(UpdateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class HomePageView(TemplateView):
    template_name = 'home.html'


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
    extra_context = {'form': CardCreateForm, 'form2': SearchCardForm}

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Card.objects.filter(author=self.request.user)
            return queryset
        queryset = Card.objects.all()
        return queryset


class CardSearchListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = 'cardssearch.html'
    extra_context = {'form2': SearchCardForm}

    def get_queryset(self):
        status = self.request.GET['status']
        if not self.request.user.is_superuser:
            queryset = Card.objects.filter(author=self.request.user, status=status)
            return queryset
        queryset = Card.objects.filter(status=status)
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


class CardDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('cards')


class CardUpdateView(LoginRequiredMixin, AddUserInFormMixin):
    model = Card
    form_class = CardUpdateForm
    template_name = 'updatecard.html'
    success_url = '/cards'


class StatusUpView(LoginRequiredMixin, AddUserInFormMixin):
    model = Card
    success_url = reverse_lazy('cards')
    form_class = CardStatusUpForm
    template_name = 'cards.html'


class StatusDownView(LoginRequiredMixin, AddUserInFormMixin):
    model = Card
    success_url = reverse_lazy('cards')
    form_class = CardStatusDownForm
    template_name = 'cards.html'
