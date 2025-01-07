from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from srciencia_core.models import Questao, Alternativa
from srciencia_core.forms import QuestaoForm, AlternativaForm
from django.forms import modelformset_factory
from rest_framework.decorators import api_view
from rest_framework.response import Response
from srciencia_core.models import Conteudo, Topico
from datetime import datetime
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from django.http import JsonResponse
from unidecode import unidecode
from srciencia_core.models.Questao import Banca, Disciplina, Conteudo, Topico
from srciencia_core.forms import BancaForm, DisciplinaForm, ConteudoForm, TopicoForm

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

    if request.method == "POST":
        questao_form = QuestaoForm(request.POST, request.FILES, instance=questao)
        formset = AlternativaFormSet(request.POST, request.FILES, queryset=questao.alternativas.all())
        
        if questao_form.is_valid() and formset.is_valid():
            questao = questao_form.save(commit=False)
            questao.ano = request.POST.get("ano")
            questao.save()

            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
                elif form.cleaned_data:
                    alternativa = form.save(commit=False)
                    alternativa.questao = questao
                    alternativa.save()

            return redirect("questao_list")
        else:
            print("Erros no formulário principal:", questao_form.errors)
            print("Erros no formset:", formset.errors)
    else:
        questao_form = QuestaoForm(instance=questao)
        formset = AlternativaFormSet(queryset=questao.alternativas.all())

    return render(request, "admin/questao_form.html", {
        "questao_form": questao_form,
        "formset": formset,
        "anos": list(range(datetime.now().year, 1924, -1)),
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

def gerenciar_banca(request):
    if request.method == "POST":
        if "add" in request.POST:
            form = BancaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Banca adicionada com sucesso!")
            else:
                messages.error(request, "Erro ao adicionar banca.")
        elif "delete" in request.POST:
            banca_id = request.POST.get("banca_id")
            try:
                banca = get_object_or_404(Banca, id=banca_id)
                banca.delete()
                messages.success(request, "Banca removida com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao remover banca: {str(e)}")

    form = BancaForm()
    bancas = Banca.objects.all()
    return render(request, "admin/gerenciar_banca.html", {
        "form": form,
        "bancas": bancas,
    })


def gerenciar_disciplina(request):
    if request.method == "POST":
        # Caso seja um POST para adicionar
        if "add" in request.POST:
            form = DisciplinaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Disciplina adicionada com sucesso!")
            else:
                messages.error(request, "Erro ao adicionar disciplina. Verifique os dados e tente novamente.")
        
        # Caso seja um POST para deletar
        elif "delete" in request.POST:
            disciplina_id = request.POST.get("disciplina_id")
            try:
                disciplina = get_object_or_404(Disciplina, id=disciplina_id)
                disciplina.delete()
                messages.success(request, "Disciplina removida com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao remover disciplina: {str(e)}")

    # Instancia um formulário vazio para exibição
    form = DisciplinaForm()
    disciplinas = Disciplina.objects.all()

    # Renderiza a página com o formulário e a lista de disciplinas
    return render(request, "admin/gerenciar_disciplina.html", {
        "form": form,
        "disciplinas": disciplinas,
    })


def gerenciar_conteudo(request):
    if request.method == "POST":
        if "add" in request.POST:
            form = ConteudoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Conteúdo adicionado com sucesso!")
            else:
                messages.error(request, "Erro ao adicionar conteúdo.")
        elif "delete" in request.POST:
            conteudo_id = request.POST.get("conteudo_id")
            try:
                conteudo = get_object_or_404(Conteudo, id=conteudo_id)
                conteudo.delete()
                messages.success(request, "Conteúdo removido com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao remover conteúdo: {str(e)}")

    form = ConteudoForm()
    conteudos = Conteudo.objects.all()
    return render(request, "admin/gerenciar_conteudo.html", {
        "form": form,
        "conteudos": conteudos,
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from srciencia_core.models import Topico, Disciplina
from srciencia_core.forms import TopicoForm

def gerenciar_topico(request):
    if request.method == "POST":
        if "add" in request.POST:
            form = TopicoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Tópico adicionado com sucesso!")
            else:
                messages.error(request, "Erro ao adicionar tópico. Verifique os dados informados.")
        elif "delete" in request.POST:
            topico_id = request.POST.get("topico_id")
            try:
                topico = get_object_or_404(Topico, id=topico_id)
                topico.delete()
                messages.success(request, "Tópico removido com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao remover tópico: {str(e)}")

    form = TopicoForm()

    topicos = Topico.objects.select_related('conteudo__disciplina').all()

    disciplinas = Disciplina.objects.all()

    return render(request, "admin/gerenciar_topico.html", {
        "form": form,
        "topicos": topicos,
        "disciplinas": disciplinas,
    })



def remover_tipo(request, tipo, id):
    if request.method == 'POST':
        if tipo == 'banca':
            item = get_object_or_404(Banca, id=id)
        elif tipo == 'disciplina':
            item = get_object_or_404(Disciplina, id=id)
        elif tipo == 'conteudo':
            item = get_object_or_404(Conteudo, id=id)
        elif tipo == 'topico':
            item = get_object_or_404(Topico, id=id)
        item.delete()
        return redirect(request.META.get('HTTP_REFERER'))  # Retorna para a página anterior
    return HttpResponseNotAllowed(['POST'])


def buscar_bancas(request):
    query = unidecode(request.GET.get('q', '').lower())
    bancas = Banca.objects.all()
    
    data = [
        {
            'id': banca.id,
            'nome': banca.nome,
        }
        for banca in bancas
        if query in unidecode(banca.nome.lower())
    ]
    return JsonResponse(data, safe=False)

def buscar_conteudos(request):
    query = unidecode(request.GET.get('q', '').lower())
    conteudos = Conteudo.objects.all().select_related('disciplina')
    
    data = [
        {
            'id': conteudo.id,
            'nome': conteudo.nome,
            'disciplina_nome': conteudo.disciplina.nome if conteudo.disciplina else "Sem Disciplina"
        }
        for conteudo in conteudos
        if query in unidecode(conteudo.nome.lower()) or
           (conteudo.disciplina and query in unidecode(conteudo.disciplina.nome.lower()))
    ]
    return JsonResponse(data, safe=False)

def buscar_topicos(request):
    query = unidecode(request.GET.get('q', '').lower())
    topicos = Topico.objects.select_related('conteudo__disciplina').distinct()

    topicos_filtrados = [
        {
            'id': topico.id,
            'nome': topico.nome,
            'conteudo_nome': topico.conteudo.nome if topico.conteudo else "Sem Conteúdo",
            'disciplina_nome': topico.conteudo.disciplina.nome if topico.conteudo and topico.conteudo.disciplina else "Sem Disciplina"
        }
        for topico in topicos
        if query in unidecode(topico.nome.lower()) or
           (topico.conteudo and query in unidecode(topico.conteudo.nome.lower())) or
           (topico.conteudo and topico.conteudo.disciplina and query in unidecode(topico.conteudo.disciplina.nome.lower()))
    ]

    response = {
        'total': len(topicos_filtrados),
        'topicos': topicos_filtrados,
    }
    return JsonResponse(response, safe=False)




def buscar_disciplinas(request):
    query = unidecode(request.GET.get('q', '').lower())
    disciplinas = Disciplina.objects.all()
    
    data = [
        {
            'id': disciplina.id,
            'nome': disciplina.nome,
        }
        for disciplina in disciplinas
        if query in unidecode(disciplina.nome.lower())
    ]
    return JsonResponse(data, safe=False)
