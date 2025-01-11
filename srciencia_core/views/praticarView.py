from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from srciencia_core.models.Questao import Questao, Disciplina
from srciencia_core.models.Praticar import RespostaAluno, RelatorioQuestao
from django.contrib.auth.decorators import login_required
import json

@login_required
def aluno_praticar(request):
    """
    Renderiza a página de prática para o aluno.
    """
    disciplinas = Disciplina.objects.all()  
    return render(request, 'aluno_praticar.html', {
        'disciplinas': disciplinas,  
        'conteudos': [],   
        'topicos': [],    
    })

@login_required
def buscar_questoes(request):
    if request.method == 'GET':
        try:
            # Obtendo filtros
            disciplina_id = request.GET.get('disciplina')
            conteudo_id = request.GET.get('conteudo')
            dificuldade = request.GET.get('dificuldade')
            quantidade = request.GET.get('quantidade', '10')  # Padrão: 10 questões
            status_filtros = request.GET.getlist('status', [])  # Lista de status
            busca = request.GET.get('busca', '').strip()  # Busca textual

            # Validação de quantidade
            if not quantidade.isdigit() or int(quantidade) <= 0:
                raise ValueError("O parâmetro 'quantidade' deve ser um número inteiro positivo.")
            quantidade = int(quantidade)

            # Base inicial de questões
            questoes = Questao.objects.select_related(
                'banca', 'disciplina', 'conteudo', 'topico'
            ).all()

            # Aplicando filtros
            if disciplina_id:
                questoes = questoes.filter(disciplina_id=disciplina_id)
            if conteudo_id:
                questoes = questoes.filter(conteudo_id=conteudo_id)
            if dificuldade:
                questoes = questoes.filter(dificuldade=dificuldade)

            # Filtrar questões pelo status
            if 'nao_resolvidas' in status_filtros:
                questoes = questoes.exclude(respostas__aluno=request.user)
            if 'com_resolucao' in status_filtros:
                questoes = questoes.filter(resolucao__isnull=False).exclude(resolucao="")
            if 'que_errei' in status_filtros:
                questoes = questoes.filter(
                    respostas__aluno=request.user,
                    respostas__correta=False
                )

            # Filtro de busca
            if busca:
                questoes = questoes.filter(descricao__icontains=busca)

            # Limitar quantidade de questões
            questoes = questoes.distinct()[:quantidade]

            # Verificar se há questões encontradas
            if not questoes.exists():
                return JsonResponse({'questoes': [], 'message': 'Nenhuma questão foi encontrada para o filtro realizado.'})

            # Serializar resultados
            data = [
                {
                    'id': questao.id,
                    'descricao': questao.descricao,
                    'alternativas': list(questao.alternativas.values('id', 'descricao', 'correta')),
                    'resolucao': questao.resolucao,
                    'ano': questao.ano,
                    'banca': questao.banca.nome if questao.banca else None,
                    'disciplina': questao.disciplina.nome if questao.disciplina else None,
                    'conteudo': questao.conteudo.nome if questao.conteudo else None,
                    'topico': questao.topico.nome if questao.topico else None,
                }
                for questao in questoes
            ]
            return JsonResponse({'questoes': data})

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Erro inesperado: ' + str(e)}, status=500)

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
    """
    Permite que o aluno reporte um problema em uma questão.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questao_id = data.get('questao_id')
            descricao = data.get('descricao', '')

            # Verifica se a questão existe
            questao = Questao.objects.get(id=questao_id)

            # Registra o relatório do problema
            RelatorioQuestao.objects.create(
                questao=questao,
                aluno=request.user,
                descricao=descricao
            )

            return JsonResponse({'success': True, 'message': 'Problema reportado com sucesso!'})

        except Questao.DoesNotExist:
            return JsonResponse({'error': 'Questão não encontrada'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
