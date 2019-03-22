from django.views.defaults import page_not_found
 
def mi_error_404(request):
    nombre_template = '404.html'
 
    return page_not_found(request, template_name=nombre_template)

