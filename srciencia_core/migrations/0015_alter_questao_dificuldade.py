# Generated by Django 4.2.7 on 2025-01-07 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srciencia_core', '0014_alter_questao_dificuldade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questao',
            name='dificuldade',
            field=models.IntegerField(choices=[(1, 'Fácil'), (2, 'Médio'), (3, 'Difícil')], default=1),
        ),
    ]
