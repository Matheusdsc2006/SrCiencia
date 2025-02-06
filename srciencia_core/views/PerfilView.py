from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from srciencia_core.models import Turma, Questao, Resolucao
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from srciencia_auth.models import Usuario
from srciencia_core.models.Turma import Turma
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse


@login_required
def aluno_perfil(request):
    if request.user.perfil != 2:
        return render(request, '403.html', status=403)

    user = request.user

    # Total de questões feitas
    total_questoes_feitas = Resolucao.objects.filter(aluno=user).count()

    context = {
        'user_id': user.id,
        'apelido': user.username,
        'nome': user.nome,
        'email': user.email,
        'data_cadastro': user.data_cadastro.strftime('%d/%m/%Y'),
        'total_questoes_feitas': total_questoes_feitas,  # Questões feitas
    }
    return render(request, 'aluno_perfil.html', context)

@login_required
def professor_perfil(request):
    if request.user.perfil != 3: 
        return render(request, '403.html', status=403) 

    user = request.user

    # Contar o número de turmas criadas pelo professor
    numero_turmas = Turma.objects.filter(professor=user).count()

    context = {
        'user_id': user.id,
        'apelido': user.username,
        'nome': user.nome,
        'email': user.email,
        'data_cadastro': user.data_cadastro.strftime('%d/%m/%Y'),
        'numero_turmas': numero_turmas, 
    }
    return render(request, 'professor_perfil.html', context)

@login_required
def editar_apelido(request):
    if request.method == 'POST':
        novo_apelido = request.POST.get('apelido')
        if novo_apelido:
            try:
                request.user.username = novo_apelido
                request.user.save()
                messages.success(request, "Apelido alterado com sucesso.")
            except Exception as e:
                messages.error(request, f"Erro ao salvar o apelido: {str(e)}")
        else:
            messages.error(request, "O apelido não pode ser vazio.")
        
        if request.user.perfil == 2: 
            return redirect('aluno_perfil')
        elif request.user.perfil == 3: 
            return redirect('professor_perfil')

    return redirect('pagina_inicial')

@login_required
def editar_foto(request):
    if request.method == 'POST':
        foto = request.FILES.get('foto')
        if foto:
            try:
                request.user.foto = foto
                request.user.save()
                messages.success(request, "Foto atualizada com sucesso.")

                # Retorna a URL da nova foto para atualização via AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": True, "foto_url": request.user.foto.url})
                    
            except Exception as e:
                messages.error(request, f"Erro ao salvar a foto: {e}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "error": str(e)})
        else:
            messages.error(request, "Nenhuma foto foi enviada.")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": "Nenhuma foto foi enviada."})

    return redirect('professor_perfil' if request.user.perfil == 3 else 'aluno_perfil')






