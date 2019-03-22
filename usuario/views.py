# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
from django.contrib import auth
#Importamos la vista genérica FormView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
#Importamos el formulario de autenticación de django
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from usuario.forms import RegistroForm
# Create your views here.
from plan.models import Planes_externos,Actividades,Plan,Base,Accion,Plancillo
from alumno.models import establecimiento
import datetime
class RegistroUsuario(CreateView):
    model = User
    template_name = "usuario/registrar.html"
    form_class = RegistroForm
    success_url = reverse_lazy('usuario:usuario_listar')
    

class ListarUsuario(ListView):
    model = User 
    template_name = 'usuario/usuario_listar.html'
    paginate_by = 25

        

def loginView(request):
    if request.user.is_authenticated():
        return redirect('indexDashboard')
    else:
        if 'login_form' in request.POST:
            login_form = LoginForm(request.POST)
            
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
                if user is not None:
                    try:
                        if user.is_active:
                            login(request, user)
                            return redirect('indexDashboard')
                    except:
                        login_form = LoginForm()
                        dataErrorLogin = "Lo sentimos, su usuario no esta habilitado para ingresar al sistema"
                        return render(request, 'loginUser.html', {'login_form': login_form, 'dataErrorLogin': dataErrorLogin})
                else:
                    login_form = LoginForm()
                    dataErrorLogin = "Usuario y/o contraseña no son válidos"
                    return render(request, 'loginUser.html', {'login_form': login_form, 'dataErrorLogin': dataErrorLogin})
            else:
                raise ('Error Login : Form Invalid')
        else:
            login_form = LoginForm()
            return render(request, 'loginUser.html', {'login_form': login_form})

@login_required()
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/usuario/privado/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/usuario/privado/')
                else:
                    return render(request, 'usuario/noactivo.html')
                    
            else:
                return render(request, 'usuario/nousuario.html')
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request, 'usuario/ingresar.html', context)

def entrar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/index/')
    if request.method == 'POST':
        formulario = LoginForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/usuario/privado/')
                else:
                    return render(request, 'usuario/noactivo.html')
                    
            else:
                return render(request, 'usuario/nousuario.html')
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request, 'usuario/ingresar.html', context)



@login_required(login_url='usuario:ingresar')
def privado(request):
    usuario = request.user
    context = {'usuario': usuario}
    return render(request, 'privado.html', context)

class UserView(DetailView):
    model = User    


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            if not request.user.is_anonymous():
                logout(request)
                return HttpResponseRedirect('/')
            else:
                return redirect('usuario:change_password')
             
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usuario/change_password.html', {
        'form': form
    })




 # listar casos por tematicas
 # Codigo descargado para realizar busquedas 
#class TematicasduplasListView(ListView):
#    model = Lista
#    template_name = 'identificadores/lista.html'
 #   context_object_name = 'lista_identificador'

#def get_context_data(self, **kwargs):
#    ctx = super(TematicasduplasListView, self).get_context_data(**kwargs)
#    ctx['search_url'] = 'listar_identificador'
#    return ctx

#def get_queryset(self):
#    queryset = super(TematicasduplasListView, self).get_queryset()
    # En el admin_base.jade tenemos un input#search(name='q', type='search')
    # usamos la sig linea para obtener la consulta solicitada.
#    q = self.request.GET.getlist('q')
#    terms = [term for term in q]
#    if q:  # Si el campo no esta vacio, construimos el filtro
#        queryset = reduce(operator.or_,
#                          (Identificador.objects.filter(Q(clave__contains=t) \
#                                                        | Q(nombre__contains=t))
#                            for t in terms
#                            )
#                          )
#    return queryset
# Ver los planes externos de todos los establecimientos
def Planes_externosEstablecimientoList(request):
#Registrar los logros de cada uno,  para cada diagnostico

    try:
        planes=Planes_externos.objects.all()
        
    except Planes_externos.DoesNotExist:
        planes=""
        
    return render(
        request,
        'usuario/listar_planes_externos_establecimientos.html',
        context={'planes':planes,
                 

                }
    )
# Listar los planes externos de todos los establecimientos
# Listado de planes externos por establecimiento 
def PlanesExternoEscuelaListView(request,pk):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico


    try:
        plan_externo=Planes_externos.objects.get(id=pk)
        x= datetime.date.today() 
        annio=str(int(x.year))
        
        plan=Plan.objects.filter(annio=annio)
        base=Base.objects.filter(plan=plan)
        accion=Accion.objects.filter(base__plan=plan)
        plancillo=Plancillo.objects.filter(accion__base__plan=plan)
        actividades=Actividades.objects.filter(plancillo__accion__base__plan=plan,planes_externos=plan_externo).order_by('fecha')
        mensaje="Plan presente en la planificación de los establecimientos"
        
    except Actividades.DoesNotExist:
        plan =None
        base=None
        accion=None
        plancillo=None
        actividades=None
        mensaje="Plan externo sin planificación"
    
    return render(
        request,
        'usuario/ver_planes_externos.html',
        context={
                 'plan_externo':plan_externo,
                 'plan':plan,
                 'base':base,
                 'accion':accion,
                 'plancillo':plancillo,
                 'actividades':actividades,
                 'mensaje':mensaje,

                 }
    )    

