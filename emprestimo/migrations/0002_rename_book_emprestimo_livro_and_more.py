# Generated by Django 5.1 on 2024-08-17 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emprestimo", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="emprestimo",
            old_name="book",
            new_name="livro",
        ),
        migrations.AlterField(
            model_name="emprestimo",
            name="data_devolucao",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="emprestimo",
            name="status",
            field=models.CharField(
                choices=[
                    ("emprestado", "Emprestado"),
                    ("devolvido", "Devolvido"),
                    ("atrasado", "Atrasado"),
                ],
                default="emprestado",
                max_length=10,
            ),
        ),
    ]
