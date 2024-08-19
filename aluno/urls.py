from django.contrib.auth import views as auth_views
from django.urls import path
from aluno import views
from .forms import CustomLoginForm

urlpatterns = [
    path('aluno/listar_alunos/', views.AlunoslistView.as_view(), name='listar-alunos'),
    path('aluno/editar/<int:pk>/', views.AlunoUpdateView.as_view(), name='aluno-update'),
    path('aluno/apagar/<int:pk>/', views.AlunoDeleteView.as_view(), name='aluno-delete'),
    path('aluno/detalhes/<int:pk>/', views.AlunoDetailView.as_view(), name='aluno-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html', authentication_form=CustomLoginForm), name="login"),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]
