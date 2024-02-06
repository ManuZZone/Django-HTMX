def globals(request):
    template = 'app/base.html'
    if(request.htmx):
        template = 'app/p_base.html'
    print(template)
    return {'template': template}