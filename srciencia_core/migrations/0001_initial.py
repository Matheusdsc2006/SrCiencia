from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Conteudo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Topico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('conteudo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicos', to='srciencia_core.conteudo')),
            ],
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', django_ckeditor_5.fields.CKEditor5Field(verbose_name='descricao')),
                ('alteravel', models.BooleanField(default=False)),
                ('resolucao', django_ckeditor_5.fields.CKEditor5Field(verbose_name='resolucao')),
                ('dificuldade', models.IntegerField(choices=[(2, 'Médio'), (3, 'Difícil'), (1, 'Fácil')], default=1)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('banca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='srciencia_core.banca')),
                ('conteudo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='srciencia_core.conteudo')),
                ('disciplina', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='srciencia_core.disciplina')),
                ('topico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='srciencia_core.topico')),
            ],
        ),
        migrations.AddField(
            model_name='conteudo',
            name='disciplina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conteudos', to='srciencia_core.disciplina'),
        ),
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='alternativas/')),
                ('correta', models.BooleanField(default=False)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alternativas', to='srciencia_core.questao')),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('codigo', models.CharField(max_length=8, unique=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turmas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
