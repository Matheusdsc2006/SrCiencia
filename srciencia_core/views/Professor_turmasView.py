from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from srciencia_core.models.Turma import Turma, Arquivo
import random
import string
from django.http import HttpResponseForbidden


@login_required
def professor_turmas(request):
    # Verifica se o usuário é professor
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado para alunos.")

    turmas = Turma.objects.filter(professor=request.user).order_by("-criado_em")

    turmas_com_dados = [
        {
            "id": turma.id,
            "nome": turma.nome,
            "descricao": turma.descricao,
            "codigo": turma.codigo,
        }
        for turma in turmas
    ]

    return render(request, "professor_turmas.html", {"turmas": turmas_com_dados})


@login_required
def listar_turmas_professor(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado para alunos.")

    turmas = Turma.objects.filter(professor=request.user).values(
        "id", "nome", "descricao", "codigo", "professor__username"
    ).order_by("-criado_em")

    return JsonResponse({"success": True, "turmas": list(turmas)})


@login_required
def criar_turma(request):
    if request.method == "POST":
        nome = request.POST.get("class_name")
        descricao = request.POST.get("class_description", "")
        if not nome:
            return JsonResponse({"success": False, "message": "O nome da turma é obrigatório."})

        # Gerar código único para a turma
        codigo = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

        turma = Turma.objects.create(
            nome=nome,
            descricao=descricao,
            codigo=codigo,
            professor=request.user,
        )

        return JsonResponse({
            "success": True,
            "message": "Turma criada com sucesso.",
            "codigo": turma.codigo,
        })

    return JsonResponse({"success": False, "message": "Método inválido."})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

@login_required
def upload_arquivo(request, turma_id):
    if request.method == 'POST':
        turma = get_object_or_404(Turma, id=turma_id, professor=request.user)
        arquivo = request.FILES.get('arquivo')  # Verifica se o arquivo foi enviado
        if not arquivo:
            return JsonResponse({'success': False, 'message': 'Nenhum arquivo enviado.'})

        nome = arquivo.name
        Arquivo.objects.create(turma=turma, arquivo=arquivo, nome=nome)

        return JsonResponse({'success': True, 'message': 'Arquivo enviado com sucesso!'})
    return JsonResponse({'success': False, 'message': 'Método inválido.'})

@login_required
def listar_arquivos(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if not (request.user == turma.professor or turma.alunos.filter(id=request.user.id).exists()):
        return JsonResponse({"success": False, "message": "Acesso negado."}, status=403)

    arquivos = Arquivo.objects.filter(turma=turma)

    arquivos_data = [
        {
            "id": arquivo.id,
            "nome": arquivo.nome,
            "url": arquivo.arquivo.url,
            "size": arquivo.arquivo.size,
        }
        for arquivo in arquivos
    ]

    return JsonResponse({"success": True, "arquivos": arquivos_data})


@login_required
def remover_arquivo(request, arquivo_id):
    if request.method == "POST":
        arquivo = get_object_or_404(Arquivo, id=arquivo_id, turma__professor=request.user)
        arquivo.delete()
        return JsonResponse({"success": True, "message": "Arquivo removido com sucesso!"})
    return JsonResponse({"success": False, "message": "Método inválido."})





