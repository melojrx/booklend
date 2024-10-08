# Generated by Django 5.1 on 2024-08-17 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("livro", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="livro",
            name="status",
            field=models.CharField(
                choices=[("disp", "Disponível"), ("indisp", "Emprestado")],
                default="disp",
                max_length=20,
            ),
        ),
    ]
