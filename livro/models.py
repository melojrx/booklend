from django.db import models
from aluno.models import User


class Livro(models.Model):
    STATUS_OPTIONS = [
        ('disp', 'Disponível'),
        ('indisp', 'Emprestado'),
    ]
    nome = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='disp')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Emprestado para')

    def __str__(self):
        return f"{self.nome} ({self.get_status_display()})"

