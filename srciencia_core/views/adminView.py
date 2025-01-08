from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from srciencia_core.models import Questao, Alternativa
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
from srciencia_core.forms import QuestaoForm, BancaForm, DisciplinaForm, ConteudoForm, TopicoForm, AlternativaForm, CustomAlternativaFormSet

def questao_list(request):
    questoes = Questao.objects.prefetch_related('alternativas')
    return render(request, "admin/questao_list.html", {"questoes": questoes})

def questao_create(request):
    # Definição correta do modelformset_factory
    AlternativaFormSet = modelformset_factory(
        Alternativa,
        form=AlternativaForm,
        formset=CustomAlternativaFormSet,  # Use o formset personalizado
        extra=5,  # Exibe 5 formulários de alternativas inicialmente
        max_num=5,  # Limita o número máximo de alternativas a 5
        validate_max=True,  # Valida o limite máximo
    )

    anos_disponiveis = list(range(datetime.now().year, 1924, -1))

    if request.method == "POST":
        # Processa os formulários enviados
        questao_form = QuestaoForm(request.POST, request.FILES)
        formset = AlternativaFormSet(request.POST, queryset=Alternativa.objects.none())

        if questao_form.is_valid() and formset.is_valid():
            # Salvar a questão
            questao = questao_form.save()

            # Salvar as alternativas preenchidas
            alternativas = formset.save(commit=False)
            for alternativa in alternativas:
                alternativa.questao = questao
                alternativa.save()

            # Preencher com alternativas vazias, se necessário
            while Alternativa.objects.filter(questao=questao).count() < 5:
                Alternativa.objects.create(questao=questao)

            return redirect(reverse("questao_list"))
    else:
        # Exibe os formulários vazios na criação
        questao_form = QuestaoForm()
        formset = AlternativaFormSet(queryset=Alternativa.objects.none())

    return render(request, "admin/questao_form.html", {
        "questao_form": questao_form,
        "formset": formset,
        "anos": anos_disponiveis,
    })


def questao_update(request, pk):
    # Recuperar a questão pelo ID
    questao = get_object_or_404(Questao, pk=pk)

    # Configurar o modelformset_factory para Alternativas
    AlternativaFormSet = modelformset_factory(
        Alternativa,
        form=AlternativaForm,
        formset=CustomAlternativaFormSet,
        extra=0,
        max_num=5,
        validate_max=True
    )

    if request.method == "POST":
        # Formulários de questão e alternativas
        questao_form = QuestaoForm(request.POST, request.FILES, instance=questao)
        formset = AlternativaFormSet(request.POST, queryset=questao.alternativas.all())

        if questao_form.is_valid() and formset.is_valid():
            # Salvar a questão
            questao = questao_form.save()

            # Salvar as alternativas
            alternativas = formset.save(commit=False)
            for alternativa in alternativas:
                alternativa.questao = questao
                alternativa.save()

            # Remover alternativas extras
            alternativas_atuais = Alternativa.objects.filter(questao=questao)
            if alternativas_atuais.count() > 5:
                alternativas_atuais[5:].delete()

            # Completar com alternativas vazias, se necessário
            while alternativas_atuais.count() < 5:
                Alternativa.objects.create(questao=questao)

            # Redirecionar para a lista de questões
            return redirect(reverse("questao_list"))
    else:
        # Preencher os formulários com os dados atuais
        questao_form = QuestaoForm(instance=questao)
        formset = AlternativaFormSet(queryset=questao.alternativas.all())

    # Recuperar valores selecionados para Conteúdo e Tópico
    conteudo_id = questao.conteudo.id if questao.conteudo else None
    topico_id = questao.topico.id if questao.topico else None
    conteudos = Conteudo.objects.filter(disciplina=questao.disciplina) if questao.disciplina else Conteudo.objects.none()
    topicos = Topico.objects.filter(conteudo=questao.conteudo) if questao.conteudo else Topico.objects.none()

    # Renderizar o template com os formulários
    return render(request, "admin/questao_form.html", {
        "questao_form": questao_form,
        "formset": formset,
        "anos": list(range(datetime.now().year, 1924, -1)),
        "conteudo_id": conteudo_id,
        "topico_id": topico_id,
        "conteudos": conteudos,
        "topicos": topicos,
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
    todas_bancas = Banca.objects.all()
    bancas_iniciais = todas_bancas[:5]
    tem_mais = todas_bancas.count() > 5

    return render(request, "admin/gerenciar_banca.html", {
        "form": form,
        "bancas": bancas_iniciais,
        "todas_bancas": todas_bancas,
        "tem_mais": tem_mais,
    })



def gerenciar_disciplina(request):
    if request.method == "POST":
        if "add" in request.POST:
            form = DisciplinaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Disciplina adicionada com sucesso!")
            else:
                messages.error(request, "Erro ao adicionar disciplina. Verifique os dados e tente novamente.")
        elif "delete" in request.POST:
            disciplina_id = request.POST.get("disciplina_id")
            try:
                disciplina = get_object_or_404(Disciplina, id=disciplina_id)
                disciplina.delete()
                messages.success(request, "Disciplina removida com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao remover disciplina: {str(e)}")

    form = DisciplinaForm()
    todas_disciplinas = Disciplina.objects.all()  # Todas as disciplinas
    disciplinas_iniciais = todas_disciplinas[:5]  # Apenas as 5 primeiras
    tem_mais = todas_disciplinas.count() > 5  # Flag para o botão "Ver mais"

    return render(request, "admin/gerenciar_disciplina.html", {
        "form": form,
        "disciplinas": disciplinas_iniciais,  # Lista inicial de 5 itens
        "todas_disciplinas": todas_disciplinas,  # Todas as disciplinas para o modal
        "tem_mais": tem_mais,
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
    todos_conteudos = Conteudo.objects.select_related("disciplina").all()
    conteudos_iniciais = todos_conteudos[:5]
    tem_mais = todos_conteudos.count() > 5

    return render(request, "admin/gerenciar_conteudo.html", {
        "form": form,
        "conteudos": conteudos_iniciais,
        "todos_conteudos": todos_conteudos,
        "tem_mais": tem_mais,
    })



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
    conteudos = Conteudo.objects.select_related('disciplina').all()
    
    data = [
        {
            'id': conteudo.id,
            'nome': conteudo.nome,
            'disciplina_nome': conteudo.disciplina.nome if conteudo.disciplina else "Sem Disciplina",
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
