from django.db import models
from aluno.models import User


class Livro(models.Model):
    STATUS_OPTIONS = [
        ('disp', 'Disponível'),
        ('indisp', 'Emprestado'),
    ]
    
    ESTANTE_OPTIONS = [
        ('1', 'Estante 1'),
        ('2', 'Estante 2'),
        ('3', 'Estante 3'),
        ('4', 'Estante 4'),
        ('5', 'Estante 5'),
        ('6', 'Estante 6'),
        ('7', 'Estante 7'),
        ('8', 'Estante 8'),
        ('9', 'Estante 9'),
    ]
    
    nome = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='disp')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Emprestado para')
    estante = models.CharField(max_length=10, choices=ESTANTE_OPTIONS, default='1', verbose_name='Estante')

    def __str__(self):
        return f"{self.nome} ({self.get_status_display()})"

