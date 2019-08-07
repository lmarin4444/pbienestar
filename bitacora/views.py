# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView,TemplateView
from bitacora.models import Lista
from bitacora.forms import BitacoraForm
from dupla.forms import Intervencion_sesionForm,Intervencion_asistencia_sesionForm,Intervencion_anular_sesionForm
from dupla.models import Intervencion_sesion
from plan.models import Planes_externos,Actividades,Plan,Base,Accion,Plancillo
from alumno.models import establecimiento
from django.core.urlresolvers import reverse_lazy,reverse
#Para enviar un mensaje de error al usuario
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
#importaciones para el uso del calendario
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

#Para enviar un mensaje al usuario

from django.contrib import messages
import datetime

# Create your views here.
def show_calendar(request,ano=None,mes=None):
    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    mes = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))

    hoydia = hoy 
    ano_pasado = hoydia.year - 1



    peticiones = Lista.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year) & Q(usuario=request.user)).order_by('horario')  
    return render(
        request,
        "bitacora/calendario.html",
        {
            'hoy':hoy,
            'peticiones':peticiones,
            
            
            
            'sig':hoy.replace(month=hoy.month+1 if hoy.month<12 else 12,day=1),
            'ant':hoy.replace(month=hoy.month-1 if hoy.month>1 else 1,day=1),
        },
        )

    

    

class BitacoraCreate(SuccessMessageMixin,CreateView):
    model = Lista    
    form_class = BitacoraForm
    template_name = 'bitacora/bitacora_form.html'
    success_url = reverse_lazy('bitacora:bitacora_listar')
    success_message = "Error evento ya creado"

    def get_context_data(self, **kwargs):
            # Llamamos ala implementacion primero del  context
            context = super(BitacoraCreate, self).get_context_data(**kwargs)
            
            #pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
            
            colegio=establecimiento.objects.get(id=self.kwargs.get('pk'))
            context['colegio']=colegio
            context['mensaje']="Creación de contingencia"

            return context



    def form_valid(self,form):
        self.object = form.save(commit=False)
        escuela=self.kwargs.get('pk') # El mismo nombre que en tu URL
        colegio=establecimiento.objects.get(pk=escuela)
        usuario=self.request.user # Verificar usuario activo

        try:
            agendado=Lista.objects.get(horario=form.instance.horario,fecha=form.instance.fecha,usuario=usuario)
            
            mensaje= "Contingencia no se puede registrar porque ya existe un evento ese día - a esa hora - regostrado por el susuaio activo"
            messages.success(self.request, self.success_message)
            url = reverse(('bitacora:bitacora_crear'), kwargs={ 'pk': colegio.id })
            print form.instance
            return HttpResponseRedirect(url,mensaje) 
            
                
        except Lista.DoesNotExist:


            form.instance.establecimiento=establecimiento.objects.get(id=escuela)
            form.instance.usuario = self.request.user
            form.instance.numero=2
            print form.instance
            self.object.save()
            return super(BitacoraCreate, self).form_valid(form)

        def get_success_message(self, cleaned_data):
            print (cleaned_data)
            return "Error "

        
class BitacoraList(ListView):
	
	paginate_by = 30
	
	template_name = 'bitacora/bitacora_list.html'
	def get_queryset(self, *args, **kwargs):
		return Lista.objects.filter(usuario=self.request.user).order_by('fecha', 'horario')


#def show_calendar(request,ano=None,mes=None):
#    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    
#    peticiones = Lista.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year)).order_by('horario')  
#    return render(
#        request,
#        "bitacora/calendario.html",
#        {
#            'hoy':hoy,
#            'peticiones':peticiones,
#            'sig':hoy.replace(month=hoy.month+1 if hoy.month<12 else 12,day=1),
#            'ant':hoy.replace(month=hoy.month-1 if hoy.month>1 else 1,day=1),
#        },
#        )
def show_calendar_personal(request,ano=None,mes=None):

    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    
    peticiones = Lista.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year) & Q(usuario=request.user)).order_by('horario')  
    return render(
        request,
        "bitacora/calendario_personal.html",
        {
            'hoy':hoy,
            'peticiones':peticiones,
            'sig':hoy.replace(month=hoy.month+1 if hoy.month<12 else 12,day=1),
            'ant':hoy.replace(month=hoy.month-1 if hoy.month>1 else 1,day=1),
        },
        )

def buscar_fechas (request,dia,mes):
    
    #group_required = 'puede_administrar_encuestas

    age = Lista.objects.filter(Q(fecha__day=dia) & Q(fecha__month=mes) & Q(usuario=request.user)).order_by('horario')  
    # Ademas de buscar el dia del mes se debe setear a todos aquellos
    # que esten fuera de plazo
    
    hoy = datetime.date.today() 
    mes=int(mes)
    mes_actual=int(hoy.month)
    anio=int(hoy.year)
    print("Mes actual :",mes_actual)  # Muestra mes
    print("Mes del parametro:",mes)  # Muestra mes
    print("Mes:",hoy.month)  # Muestra mes

    if mes >= mes_actual:
        valor=1 # Si el mes esta dentro de las opciones de modificacion 
    else:
        valor=2 # Si el mes es anterior a la fecha actual de modo que no se puede modificar 

    context = {
        "agenda":age,
        "valor":valor,
        "mes":mes,
        "dia":dia,
        "anio":anio,

    
    
         }
    return render(request, 'bitacora/calendario_dia.html', context)     

   
       
def buscar_planes_externos (request,dia,mes,plan):
    
    #group_required = 'puede_administrar_encuestas

    age = Lista.objects.filter(Q(fecha__day=dia) & Q(fecha__month=mes) & Q(planes_externos=plan).order_by(horario) ) 
    
    context = {
        "agenda":age,
    
         }
    return render(request, 'bitacora/planes_externos.html', context)

def show_calendar_planes(request,ano=None,mes=None):
    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    
    peticiones = Lista.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year)).order_by(horario) 
    return render(
        request,
        "bitacora/calendario.html",
        {
            'hoy':hoy,
            'peticiones':peticiones,
            'sig':hoy.replace(month=hoy.month+1 if hoy.month<12 else 12,day=1),
            'ant':hoy.replace(month=hoy.month-1 if hoy.month>1 else 1,day=1),
        },
        )
#Accion de ver las actividades planificadas para los planes externos
#ver los planes por area 1: Dupla PsicoSocial
def PlanesExternoListView(request,pk):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico
    try:
        plan_externo=Planes_externos.objects.get(id=pk)
        x= datetime.date.today() 
        annio=str(int(x.year))
        plan=Plan.objects.filter(annio=annio)
        base=Base.objects.filter(plan__annio=annio)
        accion=Accion.objects.filter(base__plan__annio=annio)
        plancillo=Plancillo.objects.filter(accion__base__plan__annio=annio)
        actividades=Actividades.objects.filter(plancillo__accion__base__plan__annio=annio,planes_externos=plan_externo).order_by('fecha')
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
        'bitacora/ver_planes_externos.html',
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

# Listado de planes externos por establecimiento 
def PlanesExternoEscuelaListView(request,pk,colegio):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico


    try:
        plan_externo=Planes_externos.objects.get(id=pk)
        x= datetime.date.today() 
        annio=str(int(x.year))
        escuela=establecimiento.objects.get(id=colegio)
        plan=Plan.objects.filter(annio=annio,establecimiento=escuela)
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
        'bitacora/ver_planes_externos.html',
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
# Listado de planes externos por establecimiento
def Planes_externosEstablecimientoList(request,pk):
#Registrar los logros de cada uno,  para cada diagnostico

    try:
        planes=Planes_externos.objects.all()
        escuela=establecimiento.objects.get(id=pk)
                
    except Planes_externos.DoesNotExist:
        planes=""
        

    
    return render(
        request,
        'bitacora/listar_planes_externos_establecimientos.html',
        context={'planes':planes,
                 'escuela':escuela,

                }
    )


# Proceso de actualizacion de las acciones de cada una de las opciones de la bitacora 
# Modificar una contingencia 
def modificar_contingencia(request,pk):
# modificar un indicador el cual depende de una base de un plan para un establceimiento
    
    contingencia= get_object_or_404(Lista, pk=pk)
 
    escuela=contingencia.establecimiento
    mensaje="Proceso para modificar Contingencia"
    
    if request.method=='POST':
        formulario = BitacoraForm(request.POST or None, instance=contingencia)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            contingencia= get_object_or_404(Lista, pk=pk)
            # Ver si la modificacion es cambio de datos no de fecha y hora 
 
            
            if instance.horario == contingencia.horario and instance.fecha == contingencia.fecha:

                #agendado=Lista.objects.get(horario=instance.horario,fecha=instance.fecha,usuario=request.user)
                instance.establecimiento=escuela
                instance.usuario =request.user
                instance.save() 
                mensaje="Contingencia modificada"                   
            else:                

                try:
            # Valida si el nuevo horario esta escogido     
                

                    agendado=Lista.objects.get(horario=instance.horario,fecha=instance.fecha,usuario=request.user)
                
                    mensaje= "Contingencia no se puede registrar porque ya existe un evento ese día - a esa hora - registrado por el usuario activo"
                    
                    context = {
                        "form": formulario,
                        
                        
                        "colegio":escuela,
                        "mensaje":mensaje,

                         }
                    return render(request, 'bitacora/bitacora_form.html', context) 

            
                
                except Lista.DoesNotExist:
                    instance.usuario = request.user
                        
                    instance.save()
                
                    
                    mensaje= "Contingencia modificada "    
                    context = {
                        "form": formulario,
                        
                        
                        "colegio":escuela,
                        "mensaje":mensaje,

                         }
                    return render(request, 'bitacora/bitacora_form.html', context) 
                    
            
                
        formulario = BitacoraForm(request.POST or None, instance=contingencia)
    else:

           
        formulario = BitacoraForm(request.POST or None, instance=contingencia)
    context = {
        "form": formulario,
        
        
        "colegio":escuela,
        "mensaje":mensaje,

         }
    return render(request, 'bitacora/bitacora_form.html', context) 

# Eliminar una contingencia 
class eliminar_contingencia(DeleteView):
    model = Lista
    template_name = 'bitacora/eliminar_contingencia.html'

            
    def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
        context = super(eliminar_contingencia, self).get_context_data(**kwargs)
        
        #pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
        
        b=self.kwargs.get('pk') # El mismo nombre que en tu URL
        lista=Lista.objects.get(id=b)
        
        context['lista']=lista


        return context

    def post(self,request,*args,**kwargs):          
        self.object=self.get_object

        object = super(eliminar_contingencia, self).get_object()
        pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
        
        lista=Lista.objects.get(pk=pk)
        
        
        object.delete()
        
        # Retornamos el objeto
        url = reverse(('bitacora:fechas'), kwargs={ 'dia': lista.fecha.day,'mes':lista.fecha.month})
        return HttpResponseRedirect(url)

# Registrar la asistencia a una sesion
# Ingresar la asistencia a una cita

# Registar una sesion de dupla

# Registar una sesion
class RegistrarSesion(CreateView):
    model = Intervencion_sesion
    form_class = Intervencion_asistencia_sesionForm
    #template_name = 'sesion/sesion_form.html'
    template_name = 'bitacora/registrar_sesion.html'
    success_url = reverse_lazy('sesion:sesion_listar')

    def get_context_data(self, **kwargs):
        context = super(RegistrarSesion, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        sesion_lista = Lista.objects.get(pk=pk)
        print sesion_lista
        sesion=sesion_lista.sesion
        print sesion
        caso=sesion.intervencion_casos
        dato=caso.estudiante

        
        context['dato'] = dato
        context['agenda'] = sesion_lista

        return context

    def post(self,request,*args,**kwargs):          
        self.object=self.get_object
        form = self.form_class(request.POST)

        if form.is_valid():
            solicitud = form.save(commit=False)
            mensaje=""
            pk = self.kwargs.get('pk')
            sesion_lista = Lista.objects.get(pk=pk)
            sesion=sesion_lista.sesion
            caso=sesion.intervencion_casos
            estudiante=caso.estudiante



            solicitud.fecha=sesion_lista.fecha
            solicitud.horario=sesion_lista.horario
            solicitud.numero = 1
            solicitud.intervencion_casos=caso
            solicitud.usuario=request.user

            

            

            
            solicitud.save()
        
        
        sesion_lista.numero=2
        sesion_lista.save()
    
     
        # Retornamos el objeto
        url = reverse(('bitacora:fechas'), kwargs={ 'dia': sesion_lista.fecha.day,'mes':sesion_lista.fecha.month})
        return HttpResponseRedirect(url)     

        
        
            
            
            #url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante.id })
            #return HttpResponseRedirect(url)
        #else:
        #    return self.render_to_response(self.get_context_data(form=form))
    
            





#Modificar una sesion de dupla
class RegistrarSesionUpdate(UpdateView):
    model = Intervencion_sesion
    form_class = Intervencion_asistencia_sesionForm
    #template_name = 'sesion/sesion_form.html'
    template_name = 'bitacora/registrar_sesion.html'
    success_url = reverse_lazy('sesion:sesion_listar')

    def get_context_data(self, **kwargs):
        context = super(RegistrarSesionUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        Sesion=Intervencion_sesion.objects.get(pk=pk)

        dato=Sesion.intervencion_casos.estudiante
        context['dato'] = dato
        context['agenda'] = Sesion

        return context

    def post(self,request,*args,**kwargs):          
        self.object=self.get_object
        object = super(RegistrarSesionUpdate, self).get_object()

        # Grabamos el valor 3 porque sale de la lista de eppera 
        object.numero = 1 #significa que ya no esta en lista de espera
        lista=Lista.objects.get(sesion=object)
        lista.numero=2
        lista.save()
    
        object.save()
        # Retornamos el objeto
        url = reverse(('bitacora:fechas'), kwargs={ 'dia': lista.fecha.day,'mes':lista.fecha.month})
        return HttpResponseRedirect(url)                
def anular_sesion(request,pk):

    #group_required = 'puede_administrar_encuestas
    mensaje=""
   
    sesion_lista = get_object_or_404(Lista, pk=pk)
    
    sesion=sesion_lista.sesion
    
    #plan_caso=sesion.intervencion_casos
    #estudiante=plan_caso.estudiante
    
    if request.method=='POST':
        formulario = Intervencion_anular_sesionForm(request.POST)
        lista=Lista.objects.get(id=pk)
        sesion=lista.sesion
        if formulario.is_valid():
            instance = formulario.save(commit=False)
                          
            
            instance.intervencion_casos=sesion.intervencion_casos
            instance.objetivo_especifico="No asiste y/o anulada la sesión "
            instance.tematicas="No asiste y/o anulada la sesión "
            instance.numero=2
            instance.usuario = request.user
            instance.fecha=sesion.fecha
            instance.horario=sesion.horario
            sesion_lista.numero=3
            mensaje="Actualización realizada "
            instance.save()
            sesion_lista.save()
            url = reverse(('bitacora:fechas'), kwargs={ 'dia': sesion_lista.fecha.day,'mes':sesion_lista.fecha.month})
            return HttpResponseRedirect(url)
        else:
            
            formulario = Intervencion_anular_sesionForm(request.POST or None, instance=sesion)
    else:
        
        formulario = Intervencion_anular_sesionForm(request.POST or None, instance=sesion)
        mensaje=""
    
    
    context = {
        "form": formulario,
        "sesion_lista": sesion_lista,
        "mensaje":mensaje,
        
         }
    return render(request, 'bitacora/anular_sesion.html', context)


# Ver un evento de contingencia un suceso
def ver_sucesos(request,pk):
#Registrar los logros de cada uno,  para cada diagnostico

    try:
        agendado=Lista.objects.get(pk=pk)
        
                
    except Lista.DoesNotExist:
        agendado=""
        

    
    return render(
        request,
        'bitacora/ver_sucesos.html',
        context={'agendado':agendado,
                 

                }
    )


