from django.shortcuts import render, redirect

def crud_questoes(request):
    return render(request, './admin/questoes.html')