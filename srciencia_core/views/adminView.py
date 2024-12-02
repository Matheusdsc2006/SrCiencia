from django.shortcuts import render, redirect
from srciencia_core.models import Questao, Caso, Alternativa, DisciplinaQuestao
from srciencia_core.forms import QuestaoForm, CasoFormSet, AlternativaFormSet, DisciplinaQuestaoFormSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

def questao_create(request):
    if request.method == 'POST':
        questao_form = QuestaoForm(request.POST)
        disciplina_formset = DisciplinaQuestaoFormSet(request.POST)

        if questao_form.is_valid() and disciplina_formset.is_valid():
            questao = questao_form.save()
            disciplina_formset.instance = questao  # Associar a questão criada
            disciplina_formset.save()
            return redirect('questao_list')  # Redireciona para a lista de questões
    else:
        questao_form = QuestaoForm()
        disciplina_formset = DisciplinaQuestaoFormSet(queryset=DisciplinaQuestao.objects.none())

    return render(request, 'admin/questoes/questao_form.html', {
        'questao_form': questao_form,
        'disciplina_formset': disciplina_formset,
    })




@api_view(['GET'])
def get_conteudos(request, disciplina_id):
    conteudos = Conteudo.objects.filter(disciplina_id=disciplina_id).values('id', 'nome')
    return Response(list(conteudos))

@api_view(['GET'])
def get_topicos(request, conteudo_id):
    topicos = Topico.objects.filter(conteudo_id=conteudo_id).values('id', 'nome')
    return Response(list(topicos))
