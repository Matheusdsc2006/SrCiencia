from django.shortcuts import render, redirect

def turmas_view(request):
    turmas = [
        {"id": 1, "nome": "Física II", "descricao": "Informática para Internet - 2M", "professor": "Israel França", "cor": "astronomia", "google_drive_url": "#"},
        {"id": 2, "nome": "Química II", "descricao": "Edificações - 2V", "professor": "João Maria Cardoso", "cor": "quimica", "google_drive_url": "#"},
        {"id": 3, "nome": "Biologia I", "descricao": "Controle Ambiental - 3M", "professor": "Gilsilene Ribeiro", "cor": "biologia", "google_drive_url": "#"},
        {"id": 4, "nome": "Física I", "descricao": "Eletrotécnica - 1V", "professor": "José Pedro", "cor": "astronomia", "google_drive_url": "#"},
        {"id": 5, "nome": "Química I", "descricao": "Administração - 1V", "professor": "Flávio das Neves", "cor": "quimica", "google_drive_url": "#"},
        {"id": 6, "nome": "Biologia II", "descricao": "MSI - 4V", "professor": "Marília dos Santos", "cor": "biologia", "google_drive_url": "#"},
    ]

    user = {"nome": "Lucas Albuquerque", "email": "lucas@exemplo.edu"}

    return render(request, "paginas/turmas.html", {"turmas": turmas, "user": user})

def pendentes_view(request, turma_id):
    return render(request, "paginas/pendentes.html", {"turma_id": turma_id})

def cancelar_inscricao(request, turma_id):
    # Simulação de lógica para cancelar inscrição
    return redirect('turmas')
