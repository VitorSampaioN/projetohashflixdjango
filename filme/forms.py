from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)

# Formulário de Criação de Usuário
class CriarContaForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Usuario
        # OBRIGATÓRIO SER DA FORMA ABAIXO
        fields = ('username', 'email', 'password1', 'password2')