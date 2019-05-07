# -*- coding: 850 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from django.core.urlresolvers import reverse
from calendar import Calendar
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from secretaria.forms import MascotaRAForm,FormPregunta,Formagenda,FormagendaCalendario,Formconfirma,FormFechas
from secretaria.models import MascotaRA,Pregunta,agenda,Confirma,Registro
from sesion.models import Intervenidos,sesion
from alumno.models import apoderado
from profesional.models import Profesional
from django.http import HttpResponse,HttpResponseRedirect
from alumno.models import Estudiante
from django.contrib.auth.decorators import login_required
from django import template
import datetime
from datetime import date, timedelta
from django.views.generic.dates  import DayArchiveView,MonthArchiveView,WeekArchiveView


register = template.Library()

def consulta(request): 
        form = FormFechas(request.GET or None) 
        if form.is_valid(): 
                fecha_desde = form.cleaned_data['fecha_desde'] 
                fecha_hasta = form.cleaned_data['fecha_hasta'] 

                sesiones = Sesion.objects.filter(fecha__range=(fecha_desde,fecha_hasta)) 
        return render(request, 'secretaria/entradas_mes.html', {'form':form})                

class EntradasMes(MonthArchiveView):
        '''Entradas por mes'''
        queryset=agenda.objects.order_by('fecha')
        
        template_name='secretaria/entradas_mes.html'
        date_field = 'fecha'
        month_format = '%m'
        context_object_name='entradas'

class  EntradasDia( DayArchiveView):
        '''Entradas por día'''
        queryset=agenda.objects.order_by('fecha')
        
        template_name='secretaria/entradas_dias.html'
        date_field = 'fecha'
        context_object_name='Sesion'
        month_format = '%m'
#para realizar el calendario

def EntradasDias(request,year, month ,day):
    event_list = agenda.objects.filter(fecha__year=year, fecha__month=month,fecha__day=day)
    

def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)


def cal_mes(year=date.today().year, month=date.today().month):

    event_list = agenda.objects.filter(fecha__year=year, fecha__month=month)
    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    cal_mes = []
    week = []
    week_headers = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        
        for event in event_list:
            if day >= event.fecha.date() and day <= event.fecha.date():
                cal_day['event'] = True
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False
        week.append(cal_day)
        if day.weekday() == 6:
            cal_mes.append(week)
            week = []
        i += 1
        day += timedelta(1)

    return {'calendar': cal_mes, 'headers': week_headers}

register.inclusion_tag('secretaria/cal_mes.html')(cal_mes)




#fin del calendario
class VistaCrearPregunta(CreateView):
	model = agenda
	form_class = Formagenda
	template_name = 'secretaria/agregar_pregunta.html'
	success_url = reverse_lazy('secretaria:listar_pregunta')
    #group_required = 'puede_administrar_encuestas'
     
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(VistaCrearPregunta, self).dispatch(*args, **kwargs)


class VistaListarPregunta(ListView):
    model = Intervenidos
    template_name = 'secretaria/listar_pregunta.html'
    def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
        context = super(VistaListarPregunta, self).get_context_data(**kwargs)
        return context
 

class VistaUpdatePregunta(UpdateView):
    model = agenda
    form_class = FormPregunta
    template_name = 'secretaria/listar_pregunta.html'
    success_url = reverse_lazy('secretaria:secretaria_listar_pregunta')
    #group_required = 'puede_administrar_encuestas'

class VistaBorrarPregunta(DeleteView):
    model = agenda
    form_class = FormPregunta
    template_name = 'secretaria/secretaria_delete_pregunta.html'
    success_url = reverse_lazy('secretaria:secretaria_listar_pregunta')
    #group_required = 'puede_administrar_encueagenda
def index(request):
	return render(request, 'secretaria/index.html')
	
def mascota_view(request):
	if request.method == 'POST':
		form = MascotaRAForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('secretaria:mascotara_listar')
	else:
		form = MascotaRAForm()
	return render(request, 'secretaria/mascotara_form.html', {'form':form})


def mascota_list(request):
	mascota = MascotaRA.objects.filter(obs="1")
	#mascota = MascotaRA.objects.all().order_by('id')
	contexto = {'mascotas':mascota}
	return render(request, 'secretaria/mascotara_list.html', contexto)

def mascota_list_obs(request):
	mascota = MascotaRA.objects.filter(obs="1")
	contexto = {'mascotas':mascota}
	return render(request, 'secretaria/mascotara1_list.html', contexto)


def mascota_edit(request, ):
	mascota = MascotaRA.objects.get(id=id_MascotaRA)
	if request.method == 'POST':
		form = MascotaRAForm(instance=mascota)
	else:
		form = MascotaRaForm(request.POST, instance=mascota)
		if form.is_valid():
			form.save()
		return redirect('secretaria:secretaria_listar')
	return render(request, 'secretaria/mascotara_form.html', {'form':form})


def mascota_delete(request, id_MascotaRA):
	mascota = MascotaRA.objects.get(id=id_MascotaRA)
	if request.method == 'POST':
		MascotaRA.delete()
		return redirect('secretaria:secretaria_listar')
	return render(request, 'secretaria/mascotara_delete.html', {'mascota':mascota})

class EstudianteList(ListView):
	model = Estudiante
	template_name = 'secretaria/estud_list.html'
	paginate_by = 6



class MascotaList(ListView):
	model = MascotaRA
	template_name = 'secretaria/mascotara_list.html'

	paginate_by = 6


class MascotaCreate(CreateView):
	model = agenda
	form_class = Formagenda
	template_name = 'secretaria/mascotara_form.html'
	success_url = reverse_lazy('secretaria:secretaria_listar')


class MascotaUpdate(UpdateView):
	model = MascotaRA
	form_class = MascotaRAForm
	template_name = 'secretaria/mascotara_form.html'
	success_url = reverse_lazy('secretaria:secretaria_listar')


class MascotaDelete(DeleteView):
	model = MascotaRA
	template_name = 'secretaria/mascotara_delete.html'
	success_url = reverse_lazy('secretaria:secretaria_listar')	
	

#Listado de acciones para la agenda
class VistaCrearAgenda(CreateView):
    model = agenda
    form = Formagenda
    template_name = 'secretaria/agregar_agenda.html'
    success_url = reverse_lazy('calendario:calendar-ano-mes')
    #group_required = 'puede_administrar_encuestas'
    def get_context_data(self,**kwargs):
        context = super(VistaCrearAgenda, self).get_queryset(**kwargs)
        
        dia= self.kwargs.get('dia', 0)
        
        mes= self.kwargs.get('mes', 0)
        
        anio= self.kwargs.get('anio', 0)
         
        category_list=agenda.objects.filter(Q(fecha__day=dia) & Q(fecha__month=mes) & Q(fecha__year=anio))
        context  =  { 'categories' :  category_list }
        
        return context
        
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        form.instance.usuario = self.request.user
        self.object.save()
        return super(VistaCrearAgenda, self).form_valid(form)

   
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VistaCrearAgenda, self).dispatch(*args, **kwargs)

#crear una cita desde el calendario
class VistaCrearAgendaCalendario(CreateView):
    model = agenda
    form_class = FormagendaCalendario
    template_name = 'secretaria/agregar_agenda_calendario.html'
    success_url = reverse_lazy('calendario:calendar-ano-mes')
    #group_required = 'puede_administrar_encuestas'
    def get_context_data(self, **kwargs):
        context = super(VistaCrearAgendaCalendario,self).get_context_data(**kwargs)
        fecha = self.kwargs.get('fecha') # 
        es=self.kwargs.get('estudiante')
        estudiante = Estudiante.objects.get(Estudiante_id='es')
        return context
    def form_valid(self,form):
        self.object = form.save(commit=False)
        form.instance.usuario = self.request.user
        form.instance.fecha=fecha
        form.instance.Estudiante=estudiante
        self.object.save()
        return super(VistaCrearAgendaCalendario, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VistaCrearAgendaCalendario, self).dispatch(*args, **kwargs)



class VistaCrearAgendaEspera(CreateView):
    model = agenda
    form_class = Formagenda
    template_name = 'secretaria/agregar_agenda.html'
    success_url = reverse_lazy('calendario:calendario2')
    #group_required = 'puede_administrar_encuestas'
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        form.instance.usuario = self.request.user
        self.object.save()
        return super(VistaCrearAgenda, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VistaCrearAgenda, self).dispatch(*args, **kwargs)


class VistaListarAgenda(ListView):
    model = agenda
    template_name = 'secretaria/listar_agenda.html'
 

class VistaUpdateAgenda(UpdateView):
    model = agenda
    form_class = Formagenda
    template_name = 'secretaria/listar_agenda.html'
    success_url = reverse_lazy('secretaria:secretaria_listar_agenda')
    #group_required = 'puede_administrar_encuestas'

class VistaBorrarAgenda(DeleteView):
    model = agenda
    form_class = Formagenda
    template_name = 'secretaria/secretaria_delete_agenda.html'
    success_url = reverse_lazy('secretaria:secretaria_listar_agenda')
    #group_required = 'puede_administrar_encuestas'

#solicitar cita de un estudiante despues de elegirlo
class MascotaCreate(CreateView):
    model = MascotaRA
    form_class = MascotaRAForm
    template_name = 'secretaria/mascotara_form.html'
    success_url = reverse_lazy('secretaria:secretaria_listar')


# fechas por dia
class ArticleWeekArchiveView(WeekArchiveView):
    queryset = agenda.objects.all()
    date_field = "fecha"
    week_format = "%W"
    allow_future = True    
    


#Listar a todos los estudiantes intervenidos
class IntervenidossecreList(ListView):
    model = Intervenidos 
    template_name = 'sesion/secre_intervenidos_listar.html'
#crear el formulario para realizar una confirmacion de asistencia
def Confirmacion(request,pk):

    dato = get_object_or_404(Estudiante, pk=pk)
    
    atencion= agenda.objects.filter(Estudiante__id=pk)
    
    if request.method=='POST':
        formulario = Formconfirma(request.POST, request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            instance.agenda=atencion
            
            instance.usuario = request.user
            instance.Estudiante=dato
            
            instance.save()
            return HttpResponseRedirect('/secretaria/Agendalistar/')
    else:
        formulario = Formconfirma()

    context = {
        "formulario": formulario,
        "dato": dato,
        "agenda":atencion,
         }
    return render(request, 'secretaria/formconfirmacion.html', context)  

#Eliminar una confirmaacion

def Confirmacion_Delete(request,pk,age):

    dato = get_object_or_404(Estudiante, pk=pk)

    agendo=agenda.objects.get(id=age)

    try:
        confirma=Confirma.objects.get(agenda=agendo)
    except Confirma.DoesNotExist:
        confirma=None

    template = 'secretaria/eliminar_confirmacion.html'
    
    
    context = {
        "confirma": confirma,
        "agendo":agendo,
        "dato": dato,

        }
    return render(request, template, context)



#buscar las proximas vitas de ese estudiante para el centro
def buscar_agenda(request,pk):
    
    #group_required = 'puede_administrar_encuestas
    dato = get_object_or_404(Estudiante, pk=pk)
    print dato
    atencion= agenda.objects.filter(Estudiante__id=pk).order_by('fecha')
    print atencion

    context = {
        "dato": dato,
        "agenda":atencion,
       
         }
    return render(request, 'secretaria/buscar_agenda.html', context)  

def salvacion(request):
    
    #group_required = 'puede_administrar_encuestas    
    if request.method=='POST':
        formulario = FormFechas(request.POST, request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            instance.agenda=atencion
            
            instance.usuario = request.user
            instance.Estudiante=dato
            fecha_inicio=instance.fecha_desde
            fecha_termino=instance.fecha_desde
            
                
            return HttpResponseRedirect('/secretaria/Agendalistar')
    else:
        formulario = FormFechas()

    context = {
        "formulario": formulario,
        "dato": dato,
        "agenda":atencion,

         }
    return render(request, 'secretaria/fechas_salvadoras.html', context)  


def ConfirmacionCreate(request,pk,age):

    dato = get_object_or_404(Estudiante, pk=pk)
    agendo=agenda.objects.get(id=age)
    date = datetime.date.today()      
    
        
    if request.method=='POST':
        formulario = Formconfirma(request.POST,request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            instance.usuario = request.user
            instance.Estudiante=dato
            instance.agenda=agendo
            instance.fecha_confirma=date
            if instance.estado2 == None:
                instance.estado2 = 11
            if instance.estado3 == None:
                 instance.estado3 = 11
                
            instance.save()
            agendo=agenda.objects.get(id=age)
            agendo.estado=2
            agendo.save()
                #formulario.save_m2m() para grabar datos de muchos amuchos 
            
            
            url = reverse(('secretaria:buscar_agenda'), kwargs={ 'pk': dato.id })
            return HttpResponseRedirect(url)
    else:
            formulario = Formconfirma()

    context = {
            "formulario": formulario,
            "dato": dato,
            "agendo":agendo,
            
             }
    return render(request, 'secretaria/crearconfirmacion.html', context)   
    
def ConfirmacionModificar(request,pk,age):

    dato = get_object_or_404(Estudiante, pk=pk)
    
    agendo=agenda.objects.get(id=age)
    
    confirma=Confirma.objects.get(agenda=agendo)
    
    x = datetime.date.today()
    
    form = Formconfirma(request.POST or None, instance=confirma)
    template = "secretaria/crearconfirmacion.html"         
    if form.is_valid():
        instance = form.save(commit=False)
        instance.usuario = request.user
        instance.Estudiante=dato
        instance.fecha_creacion=x
        instance.save()
        
        if request.method == 'POST':
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.Estudiante=dato
            instance.save()
            return HttpResponseRedirect("/secretaria/Agendalistar/")
    else:
        
        context={
        "dato": dato,
        "formulario": form,
        "agendo":agendo,
        }
        return render(request, template, context) 
    
    
                   
def ver_escuela(request):
    
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    
    start_week=end_week
    end_week = start_week + datetime.timedelta(4)
   
    fechas = agenda.objects.filter(fecha__range=[start_week, end_week]).order_by('fecha')
    
    
    #fechas=agenda.objects.filter(fecha=current_week)
    
    
    return render(
        request,
        'secretaria/escuela.html',
         context={
         'fechas':fechas,
         'fecha_inicio':start_week,
         'fecha_termino':end_week,
       
          
                 
                 
    })  







def ver_semana(request):
    
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    print start_week
    end_week = start_week + datetime.timedelta(7)
    
    #start_week=end_week
    end_week = start_week + datetime.timedelta(4)
    print end_week
    #fechas = agenda.objects.filter(Q(fecha__gte=start_week), Q(fecha__lte=end_week)) 
    fechas = agenda.objects.filter(fecha__range=[start_week, end_week]).order_by('horario_i')
    
    
    dias = timedelta(days=1)
    
    martes=start_week+dias

    dias = timedelta(days=2)
    
    miercoles=start_week+dias

    dias = timedelta(days=3)
    
    jueves=start_week+dias
    print fechas
    #BUSCAR LOS PSICOLOGOS DE LA PROXIMA SEMANA 

    return render(
        request,
        'secretaria/ver_semana.html',
         context={
         'fechas':fechas,
         'fecha_inicio':start_week,
         'fecha_termino':end_week,
         'martes':martes,
         'miercoles':miercoles,
         'jueves':jueves,
       
          
                 
                 
    })

def ver_impresa(request):
    
    # Obtener todos los usuarios que son profesionales centro de bienestar

    profesionales=Profesional.objects.filter(tipo_profesional =0)
    print profesionales
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    print start_week
    end_week = start_week + datetime.timedelta(7)
    #start_week=end_week
    end_week = start_week + datetime.timedelta(4)
    print end_week
    #fechas = agenda.objects.filter(Q(fecha__gte=start_week), Q(fecha__lte=end_week)) 
    fechas = agenda.objects.filter(fecha__range=[start_week, end_week]).order_by('horario_i')
    
    
    dias = timedelta(days=1)
    
    martes=start_week+dias

    dias = timedelta(days=2)
    miercoles=start_week+dias
    dias = timedelta(days=3)
    jueves=start_week+dias
    print fechas
    #BUSCAR LOS PSICOLOGOS DE LA PROXIMA SEMANA 

    return render(
        request,
        'secretaria/ver_impresa.html',
         context={
         'fechas':fechas,
         'fecha_inicio':start_week,
         'fecha_termino':end_week,
         'martes':martes,
         'miercoles':miercoles,
         'jueves':jueves,
         'profesionales':profesionales
                    
    })

def ver_dia(request,fecha=None):

    date = datetime.datetime.now()
    fechas = agenda.objects.filter(fecha=date).order_by('horario_i')
    print fechas            
        #fechas=agenda.objects.filter(fecha=current_week)  
    return render(
        request,
        'secretaria/ver_dia.html',
         context={
         'fechas':fechas,
         
         'date':date,
        
                 
    })  

#Para ver a los apoderado de cada uno de los estudiante
def ver_apoderado(request,pk,fami):
    print pk
    estudiante = Estudiante.objects.get(id=pk)
    
    print estudiante
    familia=apoderado.objects.filter(Familia__id=fami)
    print familia

    contexto = {
    'estudiante':estudiante,
    'familia':familia,
    
    }

    return render(request, 'secretaria/ver_apoderado.html', contexto)



#Visualizacion de las citas por medio de calendario por mes y año

def ver_calandario_mes(request):
    
    hoy = datetime.date.today() 
    anio=hoy.year
    contexto = {
    'anio':anio,
    
    
    }

    return render(request, 'secretaria/ver_calendario_mes.html',contexto)

#Mostrar las sesiones en las que va un estudiante
def Intervenidos_sesiones(request,pk):

    dato = get_object_or_404(Estudiante, pk=pk)
    
    try:
        listado = sesion.objects.filter(Estudiante__id=pk).order_by('fecha')
    except sesion.DoesNotExist:
        listado=None
    
    # ir a buscar la informacion de la agenda
    try:
        agendado=agenda.objects.filter(Estudiante=dato).order_by('fecha')
    except agenda.DoesNotExist:
        agendado=None
    
    try:
        registrado=Registro.objects.get(agenda=agendado)
    except Registro.DoesNotExist:
        registrado=None
    

    #dalumnos={}
    #for agendadar in agendado:
#       bandera=0
    #   for i in range (agendado):
    #       print i
    #       for x in range (listado):
    #           if i.fecha == x.fecha and i.horario_i==x.horario_i:
    #               dalumnos=({i:[x.numero,x.fecha,x.horario_i,x.observacion,x.privado]})
    #               bandera=1
    #       if bandera == 0:
    #               porque=Registro.objects.get(agenda=i,Estudiante=dato)
    #               dalumnos.append({i:['NN',i.fecha,i.horario_i,'Sesion no reliazada',i.porque]})          
    #   print dalumnos

    contexto = {'sesion':listado,
                'dato':dato,
                'registrado':registrado,
                'agendado':agendado,
                            }

    return render(request, 'secretaria/sesion_list.html', contexto)
