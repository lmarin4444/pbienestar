"""centro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from comienza import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404
from comienza.views import mi_error_404
 
handler404 = mi_error_404

urlpatterns = [
	
    url(r'^$', views.index, name='index'),
    #url(r'^$', views.home, name='home')
    #url(r'^admin/', admin.site.urls),
    url(r'^admin/', include(admin.site.urls)),
    # template del modulo empieza
    
    url(r'^informe/', include('informe.urls', namespace='informe')),
    url(r'^comienza/', include('comienza.urls', namespace='comienza')),
    url(r'^secretaria/', include('secretaria.urls', namespace='secretaria')),
    url(r'^derivacion/', include('derivacion.urls', namespace='derivacion')),
    url(r'^alumno/', include('alumno.urls', namespace='alumno')),
    url(r'^usuario/', include('usuario.urls', namespace='usuario')),
    url(r'^adopcion/', include('adopcion.urls', namespace='adopcion')),
    url(r'^sesion/', include('sesion.urls', namespace='sesion')),
    url(r'^calendario/', include('calendario.urls', namespace='calendario')),
    url(r'^profesional/', include('profesional.urls', namespace='profesional')),
    url(r'^historia/', include('historia.urls', namespace='historia')),
    url(r'^bitacora/', include('bitacora.urls', namespace='bitacora')),
    url(r'^dupla/', include('dupla.urls', namespace='dupla')),
    url(r'^plan/', include('plan.urls', namespace='plan')),
    




    #url(r'^login/', include('login.urls', namespace='login')),

    
]
if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Agregar nombre al sistio de administracion
admin.site.site_header = 'Proyecto DEM Centro de Bienestar'
