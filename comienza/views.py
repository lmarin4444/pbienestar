# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect

from derivacion.models import Ficha_derivacion
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden, HttpResponse

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from comienza.forms import RegisterUserForm, LoginForm
from usuario.models import Profile
from plan.models import Planes_externos

# Create your views here.
#def index(request):
    
#    return render (request,"index.html",{})

def index(request):
       
	return render(request,"index.html",{})

#def ver_derivaciones(request):
#    if request.user.is_autheticated():
#    	return HttpResponse (request,"ver_derivaciones.html",{})

def ver_derivaciones(request):
    
    return render (request,"comienza/ver_derivaciones.html",{})

def ver_centro(request):

    return render (request,"comienza/ver_centro.html",{})    

def nosotros(request):
    return render (request,"comienza/nosotros.html",{})

def construye(request):
    return render (request,"comienza/construccion.html",{})
def documentos(request):
    return render (request,"comienza/documentos.html",{})   

def entrar_centro(request):
    try:
        perfil=Profile.objects.get(user=request.user)
        if perfil.area ==1 or perfil.area== 3:

            cantidad = Ficha_derivacion.objects.all()
            espera =Ficha_derivacion.objects.filter(pasada=2,estado=1)
            #derivada=Ficha_derivacion.objects.filter(derivado=2)
            #espera=Ficha_derivacion.objects.filter(Q(pasada=2) |~ Q(derivado=2))
            derivada=Ficha_derivacion.objects.filter(Q(pasada=1) & Q(derivado=2) & Q(estado=1))

            context = {'cantidad': cantidad,'espera':espera,'derivada':derivada}
            return render(request,"comienza/entrar_centro.html",context)
                #return render (request,"entrar_centro.html",{})          
        else:
            return redirect('index') 
            #return render (request,"entrar_centro.html",{})

    except Profile.DoesNotExist:
        return redirect('index')     
           
def entrar_dupla(request):
    try:
        perfil=Profile.objects.get(user=request.user)
        if perfil.area ==1 or perfil.area== 4:
            cantidad = Ficha_derivacion.objects.filter(estado=1)
            retorno=Ficha_derivacion.objects.filter(Q(pasada=5) & Q(derivado=2) &  Q(estado=1) & Q(usuario=request.user))
            inst=Ficha_derivacion.objects.filter((Q(pasada=4) | Q(pasada=7)) & Q(derivado=2) & Q(estado=1) &  Q(usuario=request.user))

            context = {'retorno':retorno,
                    'inst':inst}
            return render (request,"comienza/entrar_dupla.html",context)
        else:
            return redirect('index')
    except Profile.DoesNotExist:
        return redirect('index')

def Planes_externosList(request):
#Listar la planificacion de los programas externos 
    try:
        perfil=Profile.objects.get(user=request.user)
        if perfil.area ==1 or perfil.area== 4:   
            try:
                planes=Planes_externos.objects.all()
                                    
            except Planes_externos.DoesNotExist:
                planes=""
                                                            
            return render(
            request,
            'bitacora/listar_planes_externos.html',
            context={'planes':planes,
                                        }
                            )
        else:
            return redirect('index')
    except Profile.DoesNotExist:
        return redirect('index')             
    

def entrar_secretaria(request):
    try:
        perfil=Profile.objects.get(user=request.user)
        if perfil.area ==1 or perfil.area== 2 or perfil.area == 3:
            return render (request,"comienza/entrar_secretaria.html",{})
        else:
            return redirect('index')
    except Profile.DoesNotExist:
        return redirect('index')
       

def establecimiento(request):
    return render (request,"comienza/establecimiento.html",{})


def dupla_ficha_derivacion(request):
    return render (request,"comienza/dupla_ficha_derivacion.html",{})

def convivencia(request):
    return render (request,"comienza/convivencia.html",{})   

def nosotros_con(request):
    return render (request,"comienza/nosotros_con.html",{})        

def dupla(request):
    return render (request,"comienza/dupla.html",{})

def nosotros(request):
    return render (request,"comienza/nosotros.html",{})
    
def listado(request):
    #return render (request,"comienza/listados.html",{})
    return render (request,"comienza/construccion.html",{})
def equipop(request):
    return render (request,"comienza/equipop.html",{})

def listado_construccion(request):
    return render (request,"comienza/construccion.html",{})    

def encargados(request):
    return render (request,"comienza/encargados_convivencia.html",{})  

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def mi_error_404(request):
    nombre_template = '404.html'
    return render(request, template_name=nombre_template)

def hpv(request):
    return render (request,"comienza/hpv.html",{}) 



