from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHomepage

# Create your views here.

class HomePage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs) # redireciona para homepage

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse("filme:login")
        else:
            return reverse("filme:criarconta")

# Página com todos os filmes (ListView pois mostrará uma listagem de filmes)
class HomeFilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme

# Detalhe único de cada filme (DetailView pois mostrará o Detalhe de um único filme)
class DetalhesFilmes(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilmes.html"
    model = Filme

    def get(self, request, *args, **kwargs):
        # Somar 1 na visualização daquele filme
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super(DetalhesFilmes, self).get(request, *args, **kwargs) # Redireciona o Usuário para Url final

    def get_context_data(self, **kwargs):
        context = super(DetalhesFilmes, self).get_context_data(**kwargs)
        # filtrar a tabela de filmes com categorias iguais
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context

# Barra de pesquisa (ListView pois puxará uma lista com episodios filtrados)
class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    # Editando o Object List
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class PaginaPerfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

# Criar conta (FormView para criação de um formulário
class CriarConta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    # Salvar o formulário que cria um item no banco de dados
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        reverse(): Espera o retorno de um LINK do site.
        redirect(): Espera o retorno de uma PÁGINA INTEIRA (arquivo) do site.
        """
        return reverse('filme:login')