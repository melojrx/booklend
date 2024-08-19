from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    SERIE_TURMA_CHOICES = [
        ('Admin', 'Admin'),
        ('6A', '6A'), ('6B', '6B'), ('6C', '6C'),
        ('7A', '7A'), ('7B', '7B'), ('7C', '7C'),
        ('8A', '8A'), ('8B', '8B'), ('8C', '8C'),
        ('9A', '9A'), ('9B', '9B'), ('9C', '9C'),
    ]
    
    TURNO_CHOICES = [
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
    ]
    
    serie_turma = models.CharField(
        max_length=10,
        choices=SERIE_TURMA_CHOICES,
        verbose_name='Série/Turma',
        default='6A'
    )
    turno = models.CharField(
        max_length=10,
        choices=TURNO_CHOICES,
        verbose_name='Turno',
        default='Manhã'
    )
    
    def __str__(self):
        return f"{self.username} - {self.serie_turma} - {self.turno}"
