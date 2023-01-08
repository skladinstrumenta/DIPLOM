from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from Latrello.models import Card


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput)
    email = forms.EmailField(label='E-MAIL', show_hidden_initial='123@gmail.com', widget=forms.EmailInput)
    password1 = forms.CharField(label='Password1', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')
        return email


class CardCreateForm(forms.ModelForm):
    text = forms.TextInput()
    class Meta:
        model = Card
        fields = ['text']


class CardUpdateForm(forms.ModelForm):
    executor = forms.ModelChoiceField(queryset=User.objects.all(), blank=True, required=False, label='Исполнитель') #.all()-->.none() --->>41-42 not#

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CardUpdateForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated and not user.is_superuser:
            self.fields['executor'].queryset = User.objects.filter(id=user.id)
        # else:
        #     self.fields['executor'].queryset = User.objects.all()


    class Meta:
        model = Card
        fields = ['text', 'executor']




