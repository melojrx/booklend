from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from emprestimo.models import Emprestimo

from .models import Livro


class LivrosListView(LoginRequiredMixin, ListView):
    model = Livro
    template_name = 'home.html'
    context_object_name = 'livros'

    def get_queryset(self):
        return Livro.objects.filter(status='disp')
    
    
class MyLivrosListView(LoginRequiredMixin, ListView):
    model = Livro
    template_name = 'books/mybooks.html'
    context_object_name = 'livros'

    def get_queryset(self):
        return Livro.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total de livros cadastrados
        context['total_livros'] = Livro.objects.count()
        
        # Livros disponíveis
        context['livros_disponiveis'] = Livro.objects.filter(status='disp').count()
        
        # Livros emprestados
        context['livros_emprestados'] = Livro.objects.filter(status='indisp').count()
        
        # Livro mais emprestado
        top_livro = Emprestimo.objects.values('livro').annotate(total_emprestimos=Count('id')).order_by('-total_emprestimos').first()
        if top_livro:
            livro = Livro.objects.get(id=top_livro['livro'])
            context['livro_mais_emprestado'] = {
                'livro': livro,
                'total_emprestimos': top_livro['total_emprestimos']
            }
        else:
            context['livro_mais_emprestado'] = None
        
        return context


class LivrosCreateView(LoginRequiredMixin, CreateView):
    model = Livro
    template_name = 'books/form.html'
    fields = ['nome', 'autor', 'estante']
    success_url = reverse_lazy('my-livros-list')

    def form_valid(self, form):
        form.instance.status = 'disp'  # Novo livro começa como disponível
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Cadastrar Livro"
        context['botao'] = "Cadastrar"
        return context


class LivrosUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Livro
    template_name = 'books/form.html'
    fields = ['nome', 'autor', 'estante']
    success_url = reverse_lazy('my-livros-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Livro"
        context['botao'] = "Salvar"
        return context

    def test_func(self):
        return self.request.user.is_staff  # Apenas admin pode editar

    def handle_no_permission(self):
        return redirect('my-livros-list')
    

class LivrosDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Livro
    template_name = 'books/delete.html'
    success_url = reverse_lazy('my-livros-list')

    def test_func(self):
        return self.request.user.is_staff  # Apenas admin pode excluir

    def handle_no_permission(self):
        return redirect('my-livros-list')

