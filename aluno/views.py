from pyexpat.errors import messages
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from emprestimo.models import Emprestimo
from .forms import CadastroForm
from .models import User
from django.views.generic import ListView, UpdateView, DeleteView, DetailView

class AlunoslistView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'aluno/alunos_list.html'
    context_object_name = 'alunos'
    
    def get_queryset(self):
        # Filtrar para que apenas alunos (não administradores) sejam listados
        alunos = super().get_queryset().filter(is_staff=False).order_by('first_name')
        search = self.request.GET.get('search')
        if search:
            alunos = alunos.filter(first_name__icontains=search)
        return alunos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar a contagem de alunos ao contexto
        context['total_alunos'] = self.get_queryset().count()
        
        # Adicionar a contagem de alunos com livros emprestados
        context['alunos_com_livros_emprestados'] = Emprestimo.objects.filter(status='emprestado').values('usuario').distinct().count()

        # Encontrar o aluno com o maior número total de empréstimos
        top_aluno = Emprestimo.objects.values('usuario').annotate(total_emprestimos=Count('id')).order_by('-total_emprestimos').first()

        if top_aluno:
            aluno = User.objects.get(id=top_aluno['usuario'])
            context['aluno_mais_emprestimos'] = {
                'aluno': aluno,
                'total_emprestimos': top_aluno['total_emprestimos']
            }
        else:
            context['aluno_mais_emprestimos'] = None

        return context
    

class CadastroView(FormView):
    template_name = 'auth/cadastro.html'
    form_class = CadastroForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class AlunoUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'aluno/form_aluno.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('listar-alunos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Aluno"
        context['botao'] = "Salvar"
        return context
    
    def test_func(self):
        return self.request.user.is_staff  # Apenas admin pode editar

    def handle_no_permission(self):
        return redirect('listar-alunos')
    
class AlunoDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'aluno/aluno_delete.html'
    context_object_name = 'aluno'
    success_url = reverse_lazy('listar-alunos')
    
    def get_queryset(self):
        # Garantir que apenas alunos (não administradores) possam ser deletados
        return super().get_queryset().filter(is_staff=False)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'O aluno foi deletado com sucesso.')
        return super().delete(request, *args, **kwargs)

class AlunoDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'aluno/aluno_detalhe.html'
    context_object_name = 'aluno'
    
    def get_queryset(self):
        aluno = super().get_queryset().filter(pk=self.kwargs['pk'])
        return aluno
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recuperar o histórico de empréstimos do aluno
        context['historico_emprestimos'] = Emprestimo.objects.filter(usuario=self.get_object()).select_related('livro').order_by('-data_emprestimo')
        return context