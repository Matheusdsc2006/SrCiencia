from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from srciencia_core.models import Questao, Alternativa
from srciencia_core.forms import QuestaoForm, AlternativaForm
from django.forms import modelformset_factory
from rest_framework.decorators import api_view
from rest_framework.response import Response
from srciencia_core.models import Conteudo, Topico
from datetime import datetime

def questao_list(request):
    questoes = Questao.objects.prefetch_related('alternativas')
    return render(request, "admin/questao_list.html", {"questoes": questoes})

def questao_create(request):
    AlternativaFormSet = modelformset_factory(Alternativa, form=AlternativaForm, extra=5)
    anos_disponiveis = list(range(datetime.now().year, 1924, -1))  # Lista do ano atual para 1925

    if request.method == "POST":
        questao_form = QuestaoForm(request.POST, request.FILES) 
        formset = AlternativaFormSet(request.POST, request.FILES, queryset=Alternativa.objects.none()) 
        if questao_form.is_valid() and formset.is_valid():
            questao = questao_form.save()
            for form in formset:
                alternativa = form.save(commit=False)
                alternativa.questao = questao
                alternativa.save()
            return redirect("questao_list")
    else:
        questao_form = QuestaoForm()
        formset = AlternativaFormSet(queryset=Alternativa.objects.none())

    return render(request, "admin/questao_form.html", {
        "questao_form": questao_form,
        "formset": formset,
        "anos": anos_disponiveis  # Lista de anos invertida
    })


def questao_update(request, pk):
    questao = get_object_or_404(Questao, pk=pk)
    AlternativaFormSet = modelformset_factory(Alternativa, form=AlternativaForm, extra=0, can_delete=True)
    anos_disponiveis = list(range(datetime.now().year, 1924, -1))  # Lista do ano atual para 1925

    if request.method == "POST":
        questao_form = QuestaoForm(request.POST, request.FILES, instance=questao)
        formset = AlternativaFormSet(request.POST, request.FILES, queryset=questao.alternativas.all())
        if questao_form.is_valid():
            questao = questao_form.save(commit=False)
            questao.ano = request.POST.get("ano")  # Pega o ano diretamente do formulário
            questao.save()
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data.get('DELETE'):
                        form.instance.delete()
                    elif form.cleaned_data:
                        alternativa = form.save(commit=False)
                        alternativa.questao = questao
                        alternativa.save()
                return redirect("questao_list")
    else:
        questao_form = QuestaoForm(instance=questao)
        formset = AlternativaFormSet(queryset=questao.alternativas.all())

    return render(request, "admin/questao_form.html", {
        "questao_form": questao_form,
        "formset": formset,
        "anos": anos_disponiveis,
        # Adicione os valores selecionados para repovoar os campos
        "conteudo_id": questao.conteudo.id if questao.conteudo else None,
        "topico_id": questao.topico.id if questao.topico else None
    })


def questao_delete(request, pk):
    questao = get_object_or_404(Questao, pk=pk)
    if request.method == "POST":
        questao.delete()
        return redirect("questao_list")
    return render(request, "admin/questao_confirm_delete.html", {"questao": questao})


@api_view(['GET'])
def get_conteudos(request, disciplina_id):
    try:
        conteudos = Conteudo.objects.filter(disciplina_id=disciplina_id).values('id', 'nome')
        return Response(list(conteudos))
    except Conteudo.DoesNotExist:
        return Response({'error': 'Conteúdos não encontrados.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_topicos(request, conteudo_id):
    try:
        topicos = Topico.objects.filter(conteudo_id=conteudo_id).values('id', 'nome')
        return Response(list(topicos))
    except Topico.DoesNotExist:
        return Response({'error': 'Tópicos não encontrados.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

