from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from aluno.models import User
from .models import Emprestimo, Livro
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.urls import reverse_lazy


class MyEmprestimolistview(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = 'emprestimo/meus.html'
    context_object_name = 'emprestimos'

    def get_queryset(self):
        return Emprestimo.objects.filter(status='emprestado')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contagem de livros emprestados atualmente (status 'emprestado')
        context['livros_emprestados_count'] = Emprestimo.objects.filter(status='emprestado').count()
        
        return context

class LivrosDetailView(LoginRequiredMixin, DetailView):
    model = Livro
    template_name = 'books/detalhe.html'


@login_required
def emprestar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    if livro.status == 'disp':
        if request.method == 'POST':
            aluno_id = request.POST.get('aluno_id')
            aluno = get_object_or_404(User, pk=aluno_id)
            livro.usuario = aluno
            livro.status = 'indisp'
            livro.save()

            Emprestimo.objects.create(
                livro=livro,
                usuario=aluno,
                data_emprestimo=timezone.now(),  
                data_devolucao=timezone.now() + timezone.timedelta(days=10),
                status='emprestado'
            )
            messages.success(request, f'Livro "{livro.nome}" emprestado para {aluno.get_full_name()}.')
            return redirect('meus-emprestimo')
        
        alunos = User.objects.filter(is_staff=False)
        return render(request, 'books/detalhe.html', {'livro': livro, 'alunos': alunos})
    else:
        messages.error(request, 'Este livro não está disponível para empréstimo.')
        return redirect('home')    
            

class DeleteEmprestimo(LoginRequiredMixin, DeleteView):
    model = Emprestimo
    template_name = 'emprestimo/delete.html'
    success_url = reverse_lazy('meus-emprestimo')

    def test_func(self):
       return self.request.user.is_staff  # Apenas o administrador pode deletar

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para excluir este empréstimo.')
        return redirect('meus-emprestimo')


@login_required
def devolver_emprestimo(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)

    # Verifica se o usuário atual é o administrador ou o responsável pelo empréstimo
    if request.user.is_staff or request.user == emprestimo.usuario:
        emprestimo.livro.status = 'disp'
        emprestimo.livro.save()
        
        emprestimo.status = 'devolvido'
        emprestimo.save()

        messages.success(request, 'Livro devolvido com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para devolver este livro.')

    return redirect('meus-emprestimo')

class EmprestimoDetailView(LoginRequiredMixin, DetailView):
    model = Emprestimo
    template_name = 'emprestimo/emprestimo_detail.html'
    context_object_name = 'emprestimo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emprestimo = self.get_object()
        context['is_editable'] = emprestimo.status == 'emprestado'
        return context

class EmprestimoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Emprestimo
    fields = ['data_devolucao', 'status']
    template_name = 'emprestimo/emprestimo_form.html'
    context_object_name = 'emprestimo'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        emprestimo = self.get_object()
        # Permite editar apenas empréstimos que ainda estão emprestados
        return emprestimo.status == 'emprestado'

    def handle_no_permission(self):
        return redirect('emprestimo-detail', pk=self.get_object().pk)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'emprestimo/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Recupera todos os empréstimos
        context['emprestimos'] = Emprestimo.objects.select_related('usuario', 'livro').all()
        
        # Contagem de livros emprestados atualmente (status 'emprestado')
        context['livros_emprestados_count'] = Emprestimo.objects.filter(status='emprestado').count()
        
        # Contagem total de empréstimos realizados (todos os status)
        context['total_emprestimos_count'] = Emprestimo.objects.count()

        # Contagem de empréstimos finalizados (status 'devolvido')
        context['emprestimos_finalizados_count'] = Emprestimo.objects.filter(status='devolvido').count()

        return context