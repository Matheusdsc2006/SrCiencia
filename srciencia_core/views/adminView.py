# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from srciencia_core.models import Questao, Alternativa
from srciencia_core.forms import QuestaoForm, AlternativaForm
from django.forms import modelformset_factory

def questao_list(request):
    questoes = Questao.objects.all()
    return render(request, "admin/questoes/questao_list.html", {"questoes": questoes})

def questao_create(request):
    AlternativaFormSet = modelformset_factory(Alternativa, form=AlternativaForm, extra=4)
    if request.method == "POST":
        questao_form = QuestaoForm(request.POST)
        formset = AlternativaFormSet(request.POST, queryset=Alternativa.objects.none())
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
    return render(request, "admin/questoes/questao_form.html", {"questao_form": questao_form, "formset": formset})

def questao_update(request, pk):
    questao = get_object_or_404(Questao, pk=pk)
    AlternativaFormSet = modelformset_factory(Alternativa, form=AlternativaForm, extra=0)
    if request.method == "POST":
        questao_form = QuestaoForm(request.POST, instance=questao)
        formset = AlternativaFormSet(request.POST, queryset=questao.alternativas.all())
        if questao_form.is_valid() and formset.is_valid():
            questao_form.save()
            formset.save()
            return redirect("questao_list")
    else:
        questao_form = QuestaoForm(instance=questao)
        formset = AlternativaFormSet(queryset=questao.alternativas.all())
    return render(request, "admin/questoes/questao_form.html", {"questao_form": questao_form, "formset": formset})

def questao_delete(request, pk):
    questao = get_object_or_404(Questao, pk=pk)
    if request.method == "POST":
        questao.delete()
        return redirect("questao_list")
    return render(request, "admin/questoes/questao_confirm_delete.html", {"questao": questao})
