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
    """
    Busca as questões com base nos filtros aplicados pelo aluno.
    """
    if request.method == 'GET':
        # Obtém os parâmetros enviados na requisição
        disciplina_id = request.GET.get('disciplina')
        conteudo_id = request.GET.get('conteudo')
        topico_id = request.GET.get('topico')
        dificuldade = request.GET.get('dificuldade')  # 1, 2, 3 para Fácil, Médio, Difícil
        quantidade = int(request.GET.get('quantidade', 10))  # Padrão: 10 questões

        # Filtra as questões
        questoes = Questao.objects.all()

        if disciplina_id:
            questoes = questoes.filter(disciplina_id=disciplina_id)
        if conteudo_id:
            questoes = questoes.filter(conteudo_id=conteudo_id)
        if topico_id:
            questoes = questoes.filter(topico_id=topico_id)
        if dificuldade:
            questoes = questoes.filter(dificuldade=dificuldade)

        # Limita a quantidade
        questoes = questoes[:quantidade]

        # Serializa as questões
        data = [
            {
                'id': questao.id,
                'descricao': questao.descricao,
                'alternativas': list(questao.alternativas.values('id', 'descricao', 'correta')),
                'dificuldade': questao.get_dificuldade_display(),
                'taxa_acertos': questao.taxa_acertos,
            }
            for questao in questoes
        ]
        return JsonResponse({'questoes': data})

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
