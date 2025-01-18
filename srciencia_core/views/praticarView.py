from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from srciencia_core.models.Questao import Questao, Disciplina, Alternativa
from srciencia_core.models.Praticar import RespostaAluno, RelatorioQuestao
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField
from django.db.models import OuterRef, Subquery
from difflib import SequenceMatcher
from random import sample
from random import shuffle
from django.views.decorators.http import require_POST
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter 
from django.http import HttpResponse
import random
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import requests
from django.db.models.functions import Lower
from django.db.models import Value
from django.db.models.expressions import Func
import matplotlib.pyplot as plt
from matplotlib import mathtext
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.shortcuts import get_object_or_404
from django.db.models import Q
from bs4 import BeautifulSoup
import json

@login_required
def aluno_praticar(request):
    """
    Renderiza a página de prática para o aluno ou professor.
    """
    disciplinas = Disciplina.objects.all()  
    return render(request, 'aluno_praticar.html', {
        'disciplinas': disciplinas,
        'conteudos': [],
        'topicos': [],
        'exibir_resumo': False, 
        'user_perfil': request.user.perfil,  
    })


@login_required
def buscar_questoes(request):
    """
    Endpoint para buscar questões com base em filtros aplicados.
    """
    if request.method == 'GET':
        try:
            # Obtendo parâmetros de busca e filtros
            disciplina_id = request.GET.get('disciplina')
            conteudo_id = request.GET.get('conteudo')
            dificuldade = request.GET.get('dificuldade')
            quantidade = request.GET.get('quantidade', '10')  # Padrão: 10 questões
            status_filtros = request.GET.getlist('status', [])  # Lista de status
            busca = request.GET.get('busca', '').strip()  # Texto de busca

            print(f"Filtros recebidos: disciplina={disciplina_id}, conteudo={conteudo_id}, "
                  f"dificuldade={dificuldade}, quantidade={quantidade}, status={status_filtros}, busca={busca}")

            # Validar quantidade
            if not quantidade.isdigit() or int(quantidade) <= 0:
                raise ValueError("O parâmetro 'quantidade' deve ser um número inteiro positivo.")
            quantidade = int(quantidade)

            # Base inicial de questões
            questoes = Questao.objects.select_related(
                'banca', 'disciplina', 'conteudo', 'topico'
            ).all()
            print(f"Total de questões no banco: {questoes.count()}")

            # Aplicar filtros básicos
            if disciplina_id:
                questoes = questoes.filter(disciplina_id=disciplina_id)
                print(f"Após filtro disciplina: {questoes.count()}")

            if conteudo_id:
                questoes = questoes.filter(conteudo_id=conteudo_id)
                print(f"Após filtro conteúdo: {questoes.count()}")

            if dificuldade:
                questoes = questoes.filter(dificuldade=dificuldade)
                print(f"Após filtro dificuldade: {questoes.count()}")

            # Filtrar por status
            usuario = request.user

            if 'nao_resolvidas' in status_filtros:
                # Excluir questões já respondidas
                questoes = questoes.exclude(respostas__aluno=usuario)
                print(f"Filtro 'não resolvidas' aplicado. Total após filtro: {questoes.count()}")
            else:
                print("Filtro 'não resolvidas' não aplicado. Exibindo todas as questões.")

            if 'que_errei' in status_filtros:
                questoes = questoes.filter(
                    respostas__aluno=usuario,
                    respostas__correta=False
                )
                print(f"Filtro 'que errei' aplicado. Total após filtro: {questoes.count()}")

            if 'favoritadas' in status_filtros:
                questoes = questoes.filter(favoritada_por=request.user) 
                print(f"Filtro 'favoritadas' aplicado. Total após filtro: {questoes.count()}")


            # Filtro de busca textual
            if busca:
                # Filtrar questões contendo o texto buscado no campo 'descricao'
                questoes = questoes.filter(descricao__icontains=busca)
                print(f"Questões encontradas por busca direta: {questoes.count()}")
            else:
                print("Nenhuma busca aplicada. Exibindo todas as questões.")

            # Embaralhar e limitar quantidade
            questoes = list(questoes)
            shuffle(questoes)
            questoes = questoes[:quantidade]
            print(f"Questões finais após embaralhar e limitar: {len(questoes)}")
            print(f"Parâmetros recebidos no backend: {request.GET}")

            # Serializar as questões para envio
            data = [
                {
                    'id': q.id,
                    'descricao': q.descricao,
                    'alternativas': list(q.alternativas.values('id', 'descricao', 'correta')),
                    'resolucao': q.resolucao,
                    'ano': q.ano,
                    'banca': q.banca.nome if q.banca else None,
                    'disciplina': q.disciplina.nome if q.disciplina else None,
                    'conteudo': q.conteudo.nome if q.conteudo else None,
                    'topico': q.topico.nome if q.topico else None,
                    'favoritada': usuario in q.favoritada_por.all(), 
                }
                for q in questoes
            ]

            return JsonResponse({'questoes': data})

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            return JsonResponse({'error': f'Erro inesperado: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
@login_required
def registrar_resposta(request):
    """
    Registra a resposta do aluno a uma questão.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questao_id = data.get('questao_id')
            alternativa_id = data.get('alternativa_id')
            aluno = request.user

            # Verifica se a questão existe
            questao = Questao.objects.get(id=questao_id)

            # Verifica se a alternativa é correta
            alternativa_correta = questao.alternativas.filter(id=alternativa_id, correta=True).exists()

            # Registra a resposta do aluno
            RespostaAluno.objects.create(
                aluno=aluno,
                questao=questao,
                alternativa_id=alternativa_id,
                correta=alternativa_correta
            )

            return JsonResponse({'success': True, 'correta': alternativa_correta})

        except Questao.DoesNotExist:
            return JsonResponse({'error': 'Questão não encontrada'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


@csrf_exempt
@login_required
def reportar_questao(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questao_id = data.get('questao_id')
            descricao = data.get('descricao')

            if not questao_id or not descricao:
                return JsonResponse({'error': 'Dados insuficientes para o relatório.'}, status=400)

            questao = Questao.objects.get(id=questao_id)

            # Criar o relatório
            RelatorioQuestao.objects.create(
                questao=questao,
                aluno=request.user,
                descricao_problema=descricao
            )

            return JsonResponse({'message': 'Relatório enviado com sucesso!'})

        except Questao.DoesNotExist:
            return JsonResponse({'error': 'Questão não encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erro inesperado: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_exempt
@login_required
def finalizar_atividade(request):
    if request.method == 'POST':
        try:
            # Carregar dados do corpo da requisição
            respostas = json.loads(request.body)

            # Validar as respostas
            if not isinstance(respostas, list):
                return JsonResponse({'error': 'Formato inválido de dados enviados.'}, status=400)

            aluno = request.user
            questoes_resolvidas = []

            for resposta in respostas:
                questao_id = resposta.get('questao_id')
                alternativa_id = resposta.get('alternativa_id')

                # Verificar se os IDs foram enviados
                if not questao_id or not alternativa_id:
                    continue

                try:
                    questao = Questao.objects.get(id=questao_id)
                    alternativa = questao.alternativas.get(id=alternativa_id)
                except Questao.DoesNotExist:
                    return JsonResponse({'error': f'Questão {questao_id} não encontrada.'}, status=404)
                except Alternativa.DoesNotExist:
                    return JsonResponse({'error': f'Alternativa {alternativa_id} não encontrada.'}, status=404)

                correta = alternativa.correta
                RespostaAluno.objects.update_or_create(
                    aluno=aluno,
                    questao=questao,
                    defaults={
                        'alternativa_selecionada': alternativa,
                        'correta': correta,
                    },
                )

                questoes_resolvidas.append({
                    'id': questao.id,
                    'descricao': questao.descricao,
                    'alternativas': list(questao.alternativas.values('id', 'descricao', 'correta')),
                    'alternativa_selecionada': alternativa.id,
                    'resolucao': questao.resolucao or "Nenhuma resolução disponível."
                })

            return JsonResponse({'message': 'Atividade finalizada com sucesso!', 'questoes_resolvidas': questoes_resolvidas})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Erro ao decodificar os dados JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)


@csrf_exempt
@login_required
def registrar_resposta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questao_id = data.get('questao_id')
            alternativa_id = data.get('alternativa_id')

            if not questao_id or not alternativa_id:
                return JsonResponse({'error': 'Questão ou alternativa inválida.'}, status=400)

            questao = Questao.objects.get(id=questao_id)
            alternativa = questao.alternativas.get(id=alternativa_id)
            correta = alternativa.correta

            # Salvar a resposta
            RespostaAluno.objects.update_or_create(
                aluno=request.user,
                questao=questao,
                defaults={'alternativa_selecionada': alternativa, 'correta': correta},
            )

            return JsonResponse({'message': 'Resposta registrada com sucesso!', 'correta': correta})

        except Questao.DoesNotExist:
            return JsonResponse({'error': 'Questão não encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erro inesperado: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405) 

def clean_latex(text):
    """
    Remove LaTeX notations and replace them with human-readable text.
    """
    # Lista de substituições
    replacements = [
        (r"\\times", "×"),
        (r"\\cdot", "·"),
        (r"\\text\{(.*?)\}", r"\1"),
        (r"\\frac\{(.*?)\}\{(.*?)\}", r"\1/\2"),
        (r"\\sqrt\{(.*?)\}", r"√\1"),
        (r"\\left\(|\\right\)", ""),
        (r"\^circ", "°"),  # Transforma qualquer ocorrência de ^circ em °
        (r"\\\^circ", "°"),  # Transforma \^circ em °
        (r"^circ", "°"),  # Transforma circ isolado em °
        (r"\\degree", "°"),  # Outras variantes para °
        (r"\\sin", "sen"),
        (r"\\cos", "cos"),
        (r"\\tan", "tan"),
        (r"\\log", "log"),
        (r"\\ln", "ln"),
        (r"\\", ""),  # Remove qualquer barra invertida restante
        (r"\s+", " "),  # Remove múltiplos espaços
    ]

    # Aplicando substituições em ordem
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    return text

def exportar_atividade(request):
    # Obter IDs das questões
    questoes_ids = request.GET.get("questoes", "").split(",")
    questoes = Questao.objects.filter(id__in=questoes_ids)

    # Configuração do PDF
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    for i, questao in enumerate(questoes, 1):
        # Extrair texto puro da descrição usando BeautifulSoup
        soup = BeautifulSoup(questao.descricao, "html.parser")
        descricao_texto = soup.get_text()

        # Limpar LaTeX na descrição
        descricao_formatada = clean_latex(descricao_texto)

        # Adicionar título e descrição da questão
        elements.append(Paragraph(f"<b>Questão {i}:</b> {descricao_formatada}", styles["Normal"]))

        # Adicionar imagem, se disponível
        for img_tag in soup.find_all("img"):
            img_url = img_tag.get("src")
            if img_url:
                try:
                    response = requests.get(img_url, stream=True)
                    if response.status_code == 200 and "image" in response.headers["Content-Type"]:
                        img = Image(BytesIO(response.content))
                        img.drawHeight = 150  # Ajustar altura
                        img.drawWidth = 300  # Ajustar largura
                        elements.append(img)
                except Exception as e:
                    elements.append(Paragraph(f"Erro ao carregar imagem: {e}", styles["Normal"]))

        # Adicionar alternativas
        elements.append(Paragraph("<b>Alternativas:</b>", styles["Normal"]))
        for alternativa in questao.alternativas.all():
            alternativa_texto = clean_latex(alternativa.descricao)
            elements.append(Paragraph(f"- {alternativa_texto}", styles["Normal"]))

        elements.append(Spacer(1, 12))  # Espaçamento entre questões

    # Construir o PDF
    pdf.build(elements)
    buffer.seek(0)

    # Retornar o PDF como resposta
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="atividade.pdf"'
    return response

@login_required
def favoritar_questao(request, questao_id):
    try:
        questao = Questao.objects.get(id=questao_id)
        if questao.favoritada_por.filter(id=request.user.id).exists():
            questao.favoritada_por.remove(request.user) 
            return JsonResponse({'success': True, 'favoritada': False})
        else:
            questao.favoritada_por.add(request.user) 
            return JsonResponse({'success': True, 'favoritada': True})
    except Questao.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Questão não encontrada'})




