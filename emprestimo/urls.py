from django.urls import path
from emprestimo import views

urlpatterns = [
    path('emprestimo/meus', views.MyEmprestimolistview.as_view(), name="meus-emprestimo"),   
    path('livros/<int:pk>/', views.LivrosDetailView.as_view(), name='livros-detail'),
    path('livros/<int:pk>/emprestar/', views.emprestar_livro, name='emprestar_livro'),  
    path('emprestimo/apagar/<int:pk>/', views.DeleteEmprestimo.as_view(), name='deletar-emprestimo'),
    path('emprestimo/devolver/<int:emprestimo_id>/', views.devolver_emprestimo, name='devolver-emprestimo'),
    path('emprestimo/<int:pk>/', views.EmprestimoDetailView.as_view(), name='emprestimo-detail'),
    path('emprestimo/<int:pk>/editar/', views.EmprestimoUpdateView.as_view(), name='emprestimo-update'),
    path('emprestimo/dashboard/', views.DashboardView.as_view(), name='dashboard'), 
]
