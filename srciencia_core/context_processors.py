def active_menu(request):
    """
    Define qual item do menu lateral está ativo com base na URL.
    """
    menu_map = {
        "pagina_inicial": "pagina_inicial",
        "professor_turmas": "turmas",
        "turmas": "turmas",
        "pendentes": "praticar",
        "ajuda": "ajuda",
        "meu_perfil": "meu_perfil",
    }

    active_menu = None
    if request.resolver_match:
        active_menu = menu_map.get(request.resolver_match.url_name)

    return {"active_menu": active_menu}
