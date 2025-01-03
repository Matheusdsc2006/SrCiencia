from django.shortcuts import render

def pagina_inicial(request):
    username = request.user.username 
    return render(request, 'pagina_inicial.html', {'username': username})
