from django.db import models
from django.utils import timezone
from aluno.models import User
from livro.models import Livro
from datetime import timedelta

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('emprestado', 'Emprestado'),
        ('devolvido', 'Devolvido'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='emprestado')

    def save(self, *args, **kwargs):
        if self.status == 'devolvido' and not self.data_devolucao:
            self.data_devolucao = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.livro.nome} emprestado para {self.usuario.get_full_name()}"
    
    def dias_restantes(self):
        if self.status == 'emprestado':
            data_emprestimo = self.data_emprestimo.date() if isinstance(self.data_emprestimo, timezone.datetime) else self.data_emprestimo
            dias = (data_emprestimo + timedelta(days=10) - timezone.now().date()).days
            return dias if dias >= 0 else 0
        return None
    
    def dias_atraso(self):
        if self.status == 'devolvido':
            data_emprestimo = self.data_emprestimo.date() if isinstance(self.data_emprestimo, timezone.datetime) else self.data_emprestimo
            dias = (self.data_devolucao - data_emprestimo).days - 10
            return dias if dias > 0 else 0
        return None