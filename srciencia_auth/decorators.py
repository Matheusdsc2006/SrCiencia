from django.shortcuts import redirect
from functools import wraps

def perfil_required(required_perfis, redirect_urls):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('pagina_login') 

            user_perfil = request.user.perfil
            if user_perfil not in required_perfis:
                return redirect(redirect_urls.get(user_perfil, 'pagina_padrao'))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
