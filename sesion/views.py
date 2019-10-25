# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

import datetime

import time
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from sesion.forms import SesionForm,DiagnosticoForm,SesionIniciaForm,Tipo_sesionForm,FormCita, \
TematicaForm,Objetivo_intervencionForm,SesionFormCalendar,CrearRegistroForm,ContinuidadForm,FichaEgresoForm, \
motivo_egresoForm,SeguimientoForm,ModificarRegistroForm,SesionModificarForm,SeguimientocentroForm

from sesion.models import tipo_sesion,pruebas,sesion,Diagnostico,Intervenidos,Tematicas,objetivo_intervencion, \
objetivo_intervencionhistoria,Motivo_egreso,Pasos_intervencion,Estado,Seguimiento,Reporte_continuidad,Ficha_de_egreso
from alumno.models import Estudiante
from derivacion.models import Ficha_derivacion,Motivo_Retorno_Ficha_derivacion
from secretaria.models import agenda,Registro,Confirma
from secretaria.forms import FormagendaCalendario,Formconfirma
from profesional.models import Profesional

# sesion 
#Agendar una nueva cita desde el incio

#Listado de acciones para la agenda

def CrearCita(request,id_Estudiante):
	
    #group_required = 'puede_administrar_encuestas
	mensaje=""

	dato = get_object_or_404(Estudiante, pk=id_Estudiante)
	
	if request.method=='POST':
		formulario = FormCita(request.POST, request.FILES)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			try:
 			 # try something
	 			hoy=agenda.objects.get(Q(fecha=instance.fecha) & Q(horario_i=instance.horario_i)& Q(usuario=request.user))
	 			
			except agenda.DoesNotExist:
			  # do something
				hoy=None
				
			if hoy==None:	
				instance.Estudiante=dato
				instance.usuario = request.user
				instance.numero=1# significa hora pedida ( 2: hora realizada 3: hora no asistida)
				instance.save()
				return HttpResponseRedirect('/calendario/show/calendar')
			else:
				mensaje='Horario ocupado por '+hoy.Estudiante.nombres+" "+hoy.Estudiante.firs_name+" "+hoy.Estudiante.last_name
				formulario = FormCita(request.POST or None, instance=hoy)
	else:
		formulario = FormCita()
	
	context = {
		"formulario": formulario,
		"dato": dato,
		"mensaje":mensaje,
		 }
	return render(request, 'sesion/formcita_nueva.html', context)

# Proceso por el cual la secretaria podra solicitar hora para un estudiante asignandole a un profesional
def CrearCitaSecretaria(request,id_Estudiante,profesional):

    #group_required = 'puede_administrar_encuestas
	mensaje=""

	dato = get_object_or_404(Estudiante, pk=id_Estudiante)
	psico= get_object_or_404(Profesional, pk=profesional)
	usuario=psico.usuario
	if request.method=='POST':
		formulario = FormCita(request.POST, request.FILES)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			try:
 			 # try something
	 			hoy=agenda.objects.get(Q(fecha=instance.fecha) & Q(horario_i=instance.horario_i)& Q(usuario=request.user))
	 			
			except agenda.DoesNotExist:
			  # do something
				hoy=None
				
			if hoy==None:	
				instance.Estudiante=dato
				instance.usuario = usuario
				instance.numero=1# significa hora pedida ( 2: hora realizada 3: hora no asistida)
				instance.save()
				#return HttpResponseRedirect('/calendario/show/calendar')
				#return HttpResponseRedirect('secretaria/ver_impresa')
				return redirect('secretaria:ver_impresa')
			else:
				mensaje='Horario ocupado por '+hoy.Estudiante.nombres+" "+hoy.Estudiante.firs_name+" "+hoy.Estudiante.last_name
				formulario = FormCita(request.POST or None, instance=hoy)
	else:
		formulario = FormCita()
	
	context = {
		"formulario": formulario,
		"dato": dato,
		"mensaje":mensaje,
		 }
	return render(request, 'sesion/formcita_nueva_secretaria.html', context)


# Crear asignacion de actividad individual de cada profesional

def CrearCitaProfesional(request):
	
    #group_required = 'puede_administrar_encuestas

	
	if request.method=='POST':
		formulario = FormagendaProfesional(request.POST, request.FILES)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)

			# Verificar si el bloque que quiero bloquear no tienen ninguna asignación 
			for i in range(instance.horario_i, instance.horario_t):
				
				try:

		 			hoy=agenda.objects.get(Q(fecha=instance.fecha) & Q(horario_i=i)& Q(usuario=request.user))
		 			
				except agenda.DoesNotExist:
				  # do something
					hoy=None
				try:

		 			hoy=agenda_profesional.objects.get(Q(fecha=instance.fecha) & Q(horario_i=i)& Q(usuario=request.user))
		 			
				except agenda.DoesNotExist:
				  # do something
					hoy=None
				
			if hoy==None:	
				instance.Estudiante=dato
				instance.usuario = request.user
				instance.numero=1# significa hora pedida ( 2: hora realizada 3: hora no asistida)
				instance.save()
				return HttpResponseRedirect('/calendario/show/calendar')
			else:
				mensaje='Horario ocupado por '+hoy.Estudiante.nombres+" "+hoy.Estudiante.firs_name+" "+hoy.Estudiante.last_name
				formulario = FormagendaProfesional(request.POST or None, instance=hoy)
	else:
		formulario = FormagendaProfesional()
	
	context = {
		"formulario": formulario,
		"dato": dato,
		"mensaje":mensaje,
		 }
	return render(request, 'sesion/formcita_nueva.html', context)





#Modificar una cita
def ModificarCita(request,pk,age):
	

    #group_required = 'puede_administrar_encuestas
	mensaje=""

	dato = get_object_or_404(Estudiante, pk=pk)
	cita = get_object_or_404(agenda, pk=age)
	
	if request.method=='POST':
		
		formulario = FormCita(request.POST or None, instance=cita)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			try:
 			 
				hoy=agenda.objects.get(Q(fecha=instance.fecha) & Q(horario_i=instance.horario_i) & Q(usuario=request.user))
				instance.usuario=request.user
	 			
				instance.save()
	 			
	
			except agenda.DoesNotExist:
				instance.Estudiante=dato
				instance.usuario = request.user
				instance.numero=1# significa hora pedida ( 2: hora realizada 3: hora no asistida)
				instance.save()
				mensaje="Cita modificada exitosamente"
				try:
					confirmacion=Confirma.objects.get(agenda=cita)
					#confirmacion.delete()
				except Confirma.DoesNotExist:
					confirmacion=None
				#cita.delete()
				return HttpResponseRedirect('/calendario/show/calendar')
			
				
			mensaje='Horario con información previa, y/o ocupado por '+hoy.Estudiante.nombres+" "+hoy.Estudiante.firs_name+" "+hoy.Estudiante.last_name
				
			formulario = FormCita(request.POST or None, instance=cita)
	else:
		formulario = FormCita(request.POST or None, instance=cita)

	
	context = {
		"formulario": formulario,
		"dato": dato,
		"cita":cita,
		"mensaje":mensaje,

		 }
	return render(request, 'sesion/formcitamodificar.html', context)


#Eliminar cita
class AgendaDelete(DeleteView):
	model = agenda
	template_name = 'sesion/eliminar_cita.html'
	success_url = reverse_lazy('sesion:intervenido')	

	def get_context_data(self, **kwargs):
		context=super(AgendaDelete,self).get_context_data(**kwargs)
		return context



# Para modificar una cita se va a buscar las citas de un estudiante en particular
def buscar_citas(request,pk):
    
    
	dato = get_object_or_404(Estudiante, pk=pk)
	atencion= agenda.objects.filter(Estudiante__id=pk,numero=1).order_by('fecha')
	
	try:
		confirma=Confirma.objects.filter(Estudiante__id=pk,agenda__numero=1)
		
		 			
	except Confirma.DoesNotExist:
			  # do something
		confirma=""
	
	context = {
        "dato": dato,
        "agenda":atencion,
        "confirma":confirma,
         }
	return render(request, 'sesion/buscar_agenda.html', context)  


class SesionIncicalCreate(CreateView):
	model = sesion
	template_name = 'sesion/sesion_incio_form.html'
	form_class = SesionIniciaForm
	success_url = reverse_lazy('adopcion:solicitud_listar')

	def get_context_data(self, **kwargs):
		context = super(SolicitudCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			solicitud = form.save(commit=False)
			solicitud.persona = form2.save()
			solicitud.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))
# comenzar con la intevencion de un estudiante
def ingresat(request):
    template = "ingresa_centro.html"
    querysetEstudiante = Estudiante.objects.get(Estudiante_id='pk')
    querysetSesion = sesion.objects.get(Estudiante_id=sesion.Estudiante)
    data = {
        "queryset": querysetEstudiante

    }
    return render(request, template, data)

#ver las sesiones de un estudiante en particular
# ver familia de un estudiante


# listar la asistencia al centro
class CasoDetailView(ListView):
	model = sesion
	template_name = 'sesion/ver_caso.html'
	

	def get_queryset(self):
	    qs = super(CasoDetailView, self).get_queryset()
	    return qs.filter(Estudiante=self.kwargs['pk'])


def index(request):
	return render(request, 'sesion/index.html')

def listadousuarios(request):
	lista = serializers.serialize('json', User.objects.all(), fields=['username', 'first_name'])
	return HttpResponse(lista, content_type='application/json')

def index(request):
	return render(request, 'sesion/index.html')
	
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
	mascota = MascotaRA.objects.all().order_by('id')
	contexto = {'mascotas':mascota}
	return render(request, 'secretaria/mascotara_list.html', contexto)


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

class SesionList(ListView):
	model = sesion
	template_name = 'sesion/sesion_listar_todas.html'
	paginate_by = 6


# Listado de sesiones por estudiante 		
#def SesionList_e(request, pk):
	
#	estudiante = get_object_or_404(Estudiante, Estudiante__id=pk)
#	print estudiante
#	a_list = sesion.objects.filter(Estudiante__id=pk)
#	print a_list
#	1/0
	
#	context = {'pk': pk, 'list': a_list}
#	return render(request, 'sesion/sesion_listar.html', context)


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
		registrado=Registro.objects.filter(agenda=agendado).order_by('fecha')
	except Registro.DoesNotExist:
		registrado=None
	

	#dalumnos={}
	#for agendadar in agendado:
#		bandera=0
	#	for i in range (agendado):
	#		print i
	#		for x in range (listado):
	#			if i.fecha == x.fecha and i.horario_i==x.horario_i:
	#				dalumnos=({i:[x.numero,x.fecha,x.horario_i,x.observacion,x.privado]})
	#				bandera=1
	#		if bandera == 0:
	#				porque=Registro.objects.get(agenda=i,Estudiante=dato)
	#				dalumnos.append({i:['NN',i.fecha,i.horario_i,'Sesion no reliazada',i.porque]})			
	#	print dalumnos

	contexto = {'sesion':listado,
				'dato':dato,
				'registrado':registrado,
				'agendado':agendado,
							}

	return render(request, 'sesion/sesion_list.html', contexto)



class SesionList2(ListView):
	model = sesion
	template_name = 'sesion/sesion_list.html'
	paginate_by = 6
	
	def get_queryset(self, *args, **kwargs):
		queryset = super(SesionList, self).get_queryset(**kwargs)
		name=request.GET['pk']
		return queryset.filter(Estudiante__id='pk')

#listar informacion de un estudiante

def crear_Sesion(request,age,pk):	
#group_required = 'puede_administrar_encuestas
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	inter= get_object_or_404(agenda, pk=age)
	

	try:
 			 # Verificar si hay objetivo definido
		objetivo=objetivo_intervencion.objects.get(Estudiante=dato,activo=1)
	 			
	except objetivo_intervencion.DoesNotExist:
			  # do something
		objetivo=None

	try:
 		# Obtener el numero de la ultima sesion en donde se atiende al estudiante
		#ultima=sesion.objects.latest(Estudiante__id=dato.id)
		#ultima = sesion.objects.filter(Estudiante=dato)
		#longitud = ultima
		users = sesion.objects.filter(Estudiante__id=dato.id)	 			
	except sesion.DoesNotExist:
			  # do something
		last=None


	if users.exists():	
	
		lusers = list(users)
		first = lusers[0]
		last = lusers[-1]	
		numero=last.numero +1
	else:
		numero=1		


	date = datetime.date.today()

	if request.method=='POST':
		formulario = SesionFormCalendar(request.POST, request.FILES)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			#listado de los participantes en donde esta el estudiante, si el esta cuenta 1 sino no 
			
			if instance.participantes==0 or instance.participantes==2 or instance.participantes==3 or instance.participantes==4 or instance.participantes==5 or instance.participantes==6 or instance.participantes==7 or instance.participantes==8:			
				instance.numero=numero
				
			else:
				instance.numero=numero-1
			intervenido=Intervenidos.objects.get(Estudiante=dato)
			intervenido.estado='Sesión Numero'+str(instance.numero)	
			intervenido.save()
			instance.fecha=inter.fecha
			instance.usuario = request.user
			instance.Estudiante=dato	
			instance.horario_i=inter.horario_i
			instance.save()
			inter.numero=2 #porque el estudiante asistio a la sesion
			inter.save()
			Registro.objects.create(fecha=date,agenda=inter,Estudiante=dato,situacion=3,obs="El estudiante asiste a la sesión", usuario=request.user)
			url = reverse(('calendario:fechas'), kwargs={ 'dia': inter.fecha.day,'mes': inter.fecha.month})
			return HttpResponseRedirect(url)
			
			mensaje='Sesion almacenada de '+hoy.Estudiante.nombres+" "+hoy.Estudiante.firs_name+" "+hoy.Estudiante.last_name
				
	else:
		formulario = SesionFormCalendar(request.POST or None, instance=inter)
		
	
	context = {
		"form": formulario,
		"dato": dato,
		"mensaje":mensaje,
		"agenda":inter,
		"objetivo":objetivo,
		 }
	return render(request, 'sesion/sesion_crear_form.html', context)

# Crear una sesion desde el buscador 
def crear_Sesion_buscador(request,age,pk):	
#group_required = 'puede_administrar_encuestas
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	inter= get_object_or_404(agenda, pk=age)
	

	try:
 			 # Verificar si hay objetivo definido
		objetivo=objetivo_intervencion.objects.get(Estudiante=dato,activo=1)
	 			
	except objetivo_intervencion.DoesNotExist:
			  # do something
		objetivo=None

	try:
 		# Obtener el numero de la ultima sesion en donde se atiende al estudiante
		#ultima=sesion.objects.latest(Estudiante__id=dato.id)
		#ultima = sesion.objects.filter(Estudiante=dato)
		#longitud = ultima
		users = sesion.objects.filter(Estudiante__id=dato.id)	 			
	except sesion.DoesNotExist:
			  # do something
		last=None


	if users.exists():	
	
		lusers = list(users)
		first = lusers[0]
		last = lusers[-1]	
		numero=last.numero +1
	else:
		numero=1		


	date = datetime.date.today()

	if request.method=='POST':
		formulario = SesionFormCalendar(request.POST, request.FILES)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			#listado de los participantes en donde esta el estudiante, si el esta cuenta 1 sino no 
			
			if instance.participantes==0 or instance.participantes==2 or instance.participantes==3 or instance.participantes==4 or instance.participantes==5 or instance.participantes==6 or instance.participantes==7 or instance.participantes==8:			
				instance.numero=numero
				
			else:
				instance.numero=numero-1
			intervenido=Intervenidos.objects.get(Estudiante=dato)
			intervenido.estado='Sesión Numero'+str(instance.numero)	
			intervenido.save()
			instance.fecha=inter.fecha
			instance.usuario = request.user
			instance.Estudiante=dato	
			instance.horario_i=inter.horario_i
			instance.save()
			inter.numero=2 #porque el estudiante asistio a la sesion
			inter.save()
			Registro.objects.create(fecha=date,agenda=inter,Estudiante=dato,situacion=3,obs="El estudiante asiste a la sesión", usuario=request.user)
			url = reverse(('alumno:ingresar_estudiantes_establecimiento_listado_retorno'), kwargs={'pk':dato.id})
			return HttpResponseRedirect(url)
			
			mensaje='Sesion almacenada de '+hoy.Estudiante.nombres+" "+hoy.Estudiante.firs_name+" "+hoy.Estudiante.last_name
				
	else:
		formulario = SesionFormCalendar(request.POST or None, instance=inter)
		
	
	context = {
		"form": formulario,
		"dato": dato,
		"mensaje":mensaje,
		"agenda":inter,
		"objetivo":objetivo,
		 }
	return render(request, 'sesion/sesion_crear_form.html', context)




def Crear_Registro(request,age,pk):	

	mensaje=""	
	dato = get_object_or_404(Estudiante, pk=pk)	
	inter= get_object_or_404(agenda, pk=age)
	date = datetime.date.today()

	try:
 			 # try something
		hoy=Registro.objects.get(Q(agenda=inter) & Q(Estudiante=dato))
	 			
	except Registro.DoesNotExist:
			  # do something
		hoy=None
	
	if hoy==None:
		if request.method=='POST':
			formulario = CrearRegistroForm(request.POST, request.FILES)
	 		if formulario.is_valid():
				instance = formulario.save(commit=False)			
				instance.agenda=inter
				instance.usuario = request.user
				instance.Estudiante=dato
				instance.fecha=date
				instance.save()
				inter.numero=3
				inter.save()

				url = reverse(('calendario:fechas'), kwargs={ 'dia': inter.fecha.day,'mes': inter.fecha.month})
				return HttpResponseRedirect(url)	
						
		else:
			formulario = CrearRegistroForm()
	
	else:
		mensaje='Ya se a realizado el registro para esta sesión  de: '+hoy.Estudiante.nombres+" "+hoy.Estudiante.firs_name+" "+hoy.Estudiante.last_name
		formulario = CrearRegistroForm(request.POST or None, instance=hoy)

	
		
	
	context = {
		"form": formulario,
		"dato": dato,
		"agenda":inter,
		"mensaje":mensaje,
		 }
	return render(request, 'sesion/sesion_crear_registro.html', context)


def ver_registro(request,age,pk):	

	mensaje=""	
	dato = get_object_or_404(Estudiante, pk=pk)	
	
	inter= agenda.objects.get(id=age)
	date = datetime.date.today()

	try:
 			 # try something
		hoy=Registro.objects.get(Q(agenda=inter) & Q(Estudiante=dato))
	 			
	except Registro.DoesNotExist:
			  # do something
		hoy=None
		
	if hoy==None:
			
		mensaje=' No existe registro de asistencia para esta sesión'	
		url = reverse(('sesion:intervencion_listar'), kwargs={ 'pk': dato.id })
		return HttpResponseRedirect(url)	
							
	else:
		mensaje='Estudiante con registro de asistencia '	
			
	
	context = {
		"hoy":hoy,
		"dato": dato,
		"agenda":inter,
		
		"mensaje":mensaje,
		 }
	return render(request, 'sesion/ver_registro.html', context)



def ModificarRegistro(request,pk):
	
    #group_required = 'puede_administrar_encuestas
	mensaje=""

	hoy = Registro.objects.get(id=pk)
	dato=hoy.Estudiante

	if request.method=='POST':
		formulario = ModificarRegistroForm(request.POST or None, instance=hoy)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			instance.fecha=hoy.fecha
			instance.agenda=hoy.agenda
			instance.Estudiante=dato
			instance.usuario = request.user
			instance.save()
			
			url = reverse(('sesion:ver_registro'), kwargs={ 'age': hoy.agenda.id, 'pk': dato.id})
			return HttpResponseRedirect(url)
			
		else:
			
			formulario = ModificarRegistroForm(request.POST or None, instance=hoy)
	else:
		formulario = ModificarRegistroForm(request.POST or None, instance=hoy)

	
	context = {
		"formulario": formulario,
		"dato": dato,
		"mensaje":mensaje,
		"hoy":hoy,

		 }
	return render(request, 'sesion/modificar_registro.html', context)	

class SesionCreate(CreateView):
	model = sesion
	form_class = SesionForm
	template_name = 'sesion/sesion_form.html'
	success_url = reverse_lazy('sesion:sesion_listar')
	
	def get_context_data(self,**kwargs):
		context=super(SesionCreate,self).get_context_data(**kwargs)
		
		return context

	def form_valid(self,form):
	    self.object = form.save(commit=False)
	    form.instance.usuario = self.request.user
	    self.object.save()
	    return super(SesionCreate, self).form_valid(form)

#crear un objetivo para un estudiante en particular
def ObjetivoIntervencionCreate(request,pk):

	dato = get_object_or_404(Estudiante, pk=pk)
	tema=Tematicas.objects.all()
	date = datetime.date.today()

	
	if objetivo_intervencion.objects.filter(Estudiante__id=pk,activo=1).exists():
	
		url = reverse(('sesion:VerObjetivo'), kwargs={ 'pk': dato.id})
		return HttpResponseRedirect(url)
		
		
	else:
		
		if request.method=='POST':
			formulario = Objetivo_intervencionForm(request.POST,request.FILES)
	 		if formulario.is_valid():
	 			instance = formulario.save(commit=False)
	 			instance.usuario = request.user
				instance.Estudiante=dato
				instance.fecha_creacion=date				
				instance.save()
				formulario.save_m2m()
			

				return HttpResponseRedirect('/sesion/intervenido')
		else:
			formulario = Objetivo_intervencionForm()

		context = {
			"formulario": formulario,
			"dato": dato,
			"tema":tema,
			
			 }
		return render(request, 'sesion/objetivo_intervencion_form.html', context)	
	
		
#modificar un objetivo
def ObjetivoIntervencionUpdate(request,pk):

	dato = get_object_or_404(Estudiante, pk=pk)
	date = datetime.date.today()
	
	if request.method=='POST':
		formulario = Objetivo_intervencionForm(request.POST,request.FILES)
 		if formulario.is_valid():
 			instance = formulario.save(commit=False)
 			instance.usuario = request.user
			instance.Estudiante=dato
			instance.fecha_creacion=date
		
			instance.save()
		

			return HttpResponseRedirect('/sesion/intervenido')
	else:
		formulario = Objetivo_intervencionForm()

	context = {
		"formulario": formulario,
		"dato": dato,
		
		 }
	return render(request, 'sesion/objetivo_intervencion_form.html', context)	



class CambioObjetivoListview(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = objetivo_intervencion
	template_name = 'sesion/listado_cambio_objetivo.html'
	paginate_by = 6
 
 	def get_queryset(self):
		queryset = super(CambioObjetivoListview, self).get_queryset()
		
		return queryset.filter(usuario=self.request.user,activo=1)


#Listar un objetivo ya definido para un solo estudiante 

def VerObjetivo(request,pk):
        '''listar el objetivo del estudiante en particular'''
	
	obje= objetivo_intervencion.objects.filter(Estudiante__id=pk,activo=1)
	template = "sesion/verobjetivo.html"

	context = {
		
		"objetivo": obje,
		
		
		}
	return render(request, template, context)
#Lista la hostoria de los objetivos de ese estudiante	
def VerObjetivohistorico(request,pk):
        '''listar la historia de los  objetivo del estudiante en particular'''
	
	obje= objetivo_intervencionhistoria.objects.filter(Estudiante__id=pk)
	template = "sesion/verobjetivohistoria.html"

	context = {
		
		"objetivo": obje,
		
		
		}
	return render(request, template, context)



#modificar un objetivo ya definido
def cambio_objetivo(request,pk,objetivo):
	dato = get_object_or_404(Estudiante, pk=pk)
	
	#fecha = datetime.datetime.now()
	fecha = datetime.date.today()
	impresionf = fecha.strftime("%A %B %d %Y")
	date = datetime.date.today()
	

	x = datetime.datetime.today()

	d="%s/%s/%s" % (x.year,x.day, x.month )
	

	obje= objetivo_intervencion.objects.get(pk=objetivo,activo=1)
	objetivo_pasado=obje.objetivo_particular
	
	tem=obje.Tematicas.all()
	valor=""
	
		
	for temas in tem:
		valor=valor+'-'+temas.nombre
	 	tematicas=valor
	 	

	 #para mostra las tematicas en el cuadro	
	

	form = Objetivo_intervencionForm(request.POST or None, instance=obje)
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.usuario = request.user
			instance.Estudiante=dato
			instance.fecha_creacion=x
			instance.save()

	template = "sesion/objetivo_intervencion_form.html"
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.usuario = request.user
			instance.Estudiante=dato
			instance.fecha_creacion=x
			instance.save()
			form.save_m2m()
			usuario=form.instance.usuario


		#grabar el registro en el archivo de hostoria de cada uno de los estudiantes
		objetivo_intervencionhistoria.objects.create(fecha_creacion=x,objetivo_particular=objetivo_pasado,Tematicas=tematicas,Estudiante=dato, usuario=request.user)

		return HttpResponseRedirect("/sesion/intervenido/")
	context = {
		"dato": dato,
		"objetivo": obje,
		"formulario": form,
		"tema":temas,
		}
	return render(request, template, context)
			
#procedimiento para la visualizacion de las intervenciones
#Ver a todos los intervenidos 
class intervencionesList(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion
	template_name = 'sesion/intervecion_listar.html'
	paginate_by = 5
#muestra a todas las derivaciones realizadas   
	
	
	def get_queryset(self):
		queryset = super(intervencionesList, self).get_queryset()
		return queryset.filter(derivado=2,pasada=3,estado=1)


def  SesionUpdate(request,pk):

	Sesion = get_object_or_404(sesion, pk=pk)
	dato=Sesion.Estudiante
	template = 'sesion/sesion_crear_form.html'        
	

	try:
		Sesion=sesion.objects.get(pk=pk)
		x = datetime.date.today()
		form = SesionModificarForm(request.POST or None, instance=Sesion)
		template = 'sesion/sesion_crear_form.html'
	
		if request.method=='POST':
			form = SesionModificarForm(request.POST or None, instance=Sesion)
 			if form.is_valid():

				form.instance= form.save(commit=False)
				form.instance.numero=Sesion.numero
				form.instance.horario_i=Sesion.horario_i
				form.instance.fecha=Sesion.fecha
				form.instance.usuario=request.user
				form.instance.Estudiante=Sesion.Estudiante

				form.instance.save()
			
			
				
				
			url = reverse(('sesion:intervencion_listar'), kwargs={ 'pk': Sesion.Estudiante.id })
			return HttpResponseRedirect(url)

	except sesion.DoesNotExist:
		Sesion=None
		form = SesionModificarForm(request.POST or None, instance=Sesion)
		
		template= 'sesion/sesion_crear_form.html'
		context={
	        "dato": dato,
	        "form": form,
	        "agenda": Sesion,



	        }


		return render(request, template, context) 
	
	
	
	context={
	        "dato": dato,
	        "form": form,
	        "agenda": Sesion,
	        
	        }


	return render(request, template, context) 







class SesionDelete(DeleteView):
	model = sesion
	template_name = 'sesion/sesion_delete.html'
	

	def get_context_data(self, **kwargs):
		context=super(SesionDelete,self).get_context_data(**kwargs)
		return context
	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(SesionDelete, self).get_object()
		
		agendado=agenda.objects.get(Estudiante=object.Estudiante,fecha=object.fecha,horario_i=object.horario_i)
		

        # Borramos las acciones realizadas en la agenda 
		agendado.numero=1
		agendado.save()
		#Ir a borrar el registro de asistencia para esa sesion
		try:
			registrado=Registro.objects.get(agenda=agendado)
			registrado.delete()
		except Registro.DoesNotExist:
			registrado=""
		
		dato=object.Estudiante
		try:
 			 # Obtener el numero de la ultima sesion en donde se atiende al estudiante
		#ultima=sesion.objects.latest(Estudiante__id=dato.id)
		#ultima = sesion.objects.filter(Estudiante=dato)
		#longitud = ultima

			users = sesion.objects.filter(Estudiante__id=dato.id)
			if users.exists():	
		
				lusers = list(users)
				first = lusers[0]
				last = lusers[-1]	
				numero=last.numero -1
			else:
				numero=0	 			
		except sesion.DoesNotExist:
				  # do something
			last=None


		
		intervenido=Intervenidos.objects.get(Estudiante=dato)
		if numero == 0:
			intervenido.estado= 'Intervenido, borradas las sesiones'
			intervenido.save()
		else:
			intervenido.estado= 'Sesión Nº ' +str(numero)
			intervenido.save()						
		object.delete()
        # Retornamos el objeto
		
		url = reverse(('sesion:intervencion_listar'), kwargs={ 'pk': dato.id })
		return HttpResponseRedirect(url)	




#Area de manejo de tematicas 
class tematicaList(ListView):
	model = Tematicas 
	template_name = 'sesion/tematica_list.html'
	paginate_by = 6

	def get_queryset(self):
		queryset = super(tematicaList, self).get_queryset()
		return queryset.order_by('id')

	
   
class tematicaCreate(CreateView):
	model = Tematicas
	form_class = TematicaForm
	template_name = 'sesion/tematica_form.html'
	success_url = reverse_lazy('sesion:tematica_listar')


class tematicaUpdate(UpdateView):
	model = Tematicas
	form_class = TematicaForm
	template_name = 'sesion/tematica_form.html'
	success_url = reverse_lazy('sesion:tematica_listar')


class tematicaDelete(DeleteView):
	model = Tematicas
	template_name = 'sesion/tematica_delete.html'
	success_url = reverse_lazy('sesion:tematica_listar')

#Area de manejo de tipo de sesion
class tipo_sesionList(ListView):
	model = tipo_sesion 
	template_name = 'sesion/tipo_sesion_list.html'
	paginate_by = 6
   
class tipo_sesionCreate(CreateView):
	model = tipo_sesion
	form_class = Tipo_sesionForm
	template_name = 'sesion/tipo_sesion_form.html'
	success_url = reverse_lazy('sesion:tipo_sesion_listar')


class tipo_sesionUpdate(UpdateView):
	model = tipo_sesion
	form_class = Tipo_sesionForm
	template_name = 'sesion/tipo_sesion_form.html'
	success_url = reverse_lazy('sesion:tipo_sesion_listar')


class tipo_sesionDelete(DeleteView):
	model = tipo_sesion
	template_name = 'sesion/tipo_sesion_delete.html'
	success_url = reverse_lazy('sesion:tipo_sesion_listar')	



#Area de manejo de Diagostico
class DiagnosticoList(ListView):
	model = Diagnostico 
	template_name = 'sesion/diagnostico_listar'
	paginate_by = 6
   

class DiagnosticoCreate(CreateView):
	model = Diagnostico
	form_class = DiagnosticoForm
	template_name = 'sesion/Diagnostico_form.html'
	success_url = reverse_lazy('sesion:diagnostico_listar')


class DiagnosticoUpdate(UpdateView):
	model = Diagnostico
	form_class = DiagnosticoForm
	template_name = 'sesion/Diagnostico_form.html'
	success_url = reverse_lazy('sesion:Diagnostico_listar')


class DiagnosticoDelete(DeleteView):
	model = Diagnostico
	template_name = 'sesion/Diagnostico_delete.html'
	success_url = reverse_lazy('sesion:Diagnostico_listar')	


#Area de manejo de Intervenidos

class IntervenidosList(ListView):
	model = Intervenidos 
	template_name = 'sesion/intervenidos_listar.html'

 
 	def get_queryset(self):
		queryset = super(IntervenidosList, self).get_queryset()
		return queryset.filter(usuario=self.request.user,activo=1)

# Listar intervenidos por profesional para pedir hora
class IntervenidosListSecretaria(ListView):
	model = Intervenidos 
	template_name = 'sesion/intervenidos_listar_secretaria.html'

	def get_context_data(self, *args, **kwargs):
		context = super(IntervenidosListSecretaria, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		upro=User.objects.get(id=pk)
		intervenido=Intervenidos.objects.filter(usuario=upro,activo=1)
		context['intervenido']=intervenido
		context['usuario']=upro

		return context


#Para pedir hora 		

class IntervenidosListAgenda(ListView):
	model = Intervenidos 
	second_model=Estudiante
	form=FormagendaCalendario
	template_name = 'sesion/intervenidos_listar_calendario.html'
	paginate_by = 6
 
 	def get_queryset(self):
		queryset = super(IntervenidosList, self).get_queryset()

		return queryset.filter(usuario=self.request.user)

def Reportecontinuidad(request,pk):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	
	
		#obje= get_object_or_404(objetivo_intervencion, Estudiante__id=pk)
        #evaluacion=Diagnostico.objects.get(Estudiante__id=pk)
        #obj_id=objetivo_intervencion.objects.filter(Estudiante__id=pk)
	form = ContinuidadForm()
	if request.method == 'POST':
		form = ContinuidadForm(request.POST)
	        #codigo
		if form.is_valid():
			instance = form.save(commit=False)
			x = datetime.date.today()
			instance.Estudiante=estudiante_id
			instance.fecha=x
			instance.activo=1
			instance.usuario=request.user
			instance.save()
			return redirect('derivacion:intervencion_listar')
        	


    #Enviar un valor pasa saber si la persona que esta activa es la misma que hiso el informe
    # si valor es 0 el usuario que hiso el informe es el mismo que esta actualmente si el 1 no es el mismo
    
	return render(
        request,
        'sesion/reporte_continuidad.html',
        context={'form':form,
        		'dato':estudiante_id,
        	        		 

	})
	
def Reportecontinuidad_solo(request,pk):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	
	
		#obje= get_object_or_404(objetivo_intervencion, Estudiante__id=pk)
        #evaluacion=Diagnostico.objects.get(Estudiante__id=pk)
        #obj_id=objetivo_intervencion.objects.filter(Estudiante__id=pk)
	form = ContinuidadForm()
	if request.method == 'POST':
		form = ContinuidadForm(request.POST)
	        #codigo
		if form.is_valid():
			instance = form.save(commit=False)
			x = datetime.date.today()
			instance.Estudiante=estudiante_id
			instance.fecha=x
			instance.usuario=request.user
			instance.save()
			return redirect('derivacion:intervencion_listar')
        	
    #Enviar un valor pasa saber si la persona que esta activa es la misma que hiso el informe
    # si valor es 0 el usuario que hiso el informe es el mismo que esta actualmente si el 1 no es el mismo
    
	return render(
        request,
        'sesion/reporte_continuidad_solo.html',
        context={'form':form,
        		'dato':estudiante_id,
        	        		 

	})

def VerReportecontinuidad(request,pk):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	try:
		informes=Reporte_continuidad.objects.filter(Estudiante__id=pk)
	except Reporte_continuidad.DoesNotExist:
		informes=None
	
    
	return render(
        request,
        'sesion/listado_continuidad.html',
        context={'informes':informes,
        		'dato':estudiante_id
        	        		 

	})	

	#Para listar los diferentes onformes de continuidad entregados 
def ReportecontinuidadModificar(request,pk):
	mensaje=""
	
	continuidad=Reporte_continuidad.objects.get(pk=pk)
	dato=continuidad.Estudiante
	
	try:
		obje= objetivo_intervencion.objects.get(Estudiante=dato,activo=1)
	except objetivo_intervencion.DoesNotExist:
		obje=None	
	x = datetime.date.today()
	if request.method == 'POST':
		form = ContinuidadForm(request.POST)	
		if form.is_valid():
			
			instance = form.save(commit=False)
			instance.Estudiante=continuidad.Estudiante
			instance.fecha=x
			instance.usuario=request.user
	        #codigo
			instance.save()
			continuidad.delete()
			return redirect('derivacion:intervencion_listar')
       
		if obje==None:
			obje=""
	valor=""
	form = ContinuidadForm( instance=continuidad)	
	#form = ContinuidadForm( instance=continuidad)
	return render(
		        request,
		        'sesion/reporte_continuidad.html',
		        context={'formulario':form,
	        	'dato':dato,
	       		 'objetivo':obje,
        		 'mensaje':mensaje,
        		 'valor':valor,
        		 'certificado':pk,
        		 
        		 
	})



def Ficha_egreso(request,pk):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	ficha_id=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
	mensaje=""

	try:
		ultimo = sesion.objects.latest('Estudiante')
	

		try:
			intervencion=Intervenidos.objects.get(Estudiante__id=pk)
			yo=intervencion.usuario
		except Intervenidos.DoesNotExist:
			intervencion=""
			yo=""
		try:
			evaluar=Ficha_de_egreso.objects.get(Estudiante__id=pk)
			mensaje="Estudiante ya cuenta con un reporte de continuidad"
			
				
		except Ficha_de_egreso.DoesNotExist:
			evaluar=""
			form = FichaEgresoForm()

		try:
			#obje= get_object_or_404(objetivo_intervencion, Estudiante__id=pk)

			obje= objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
	        #evaluacion=Diagnostico.objects.get(Estudiante__id=pk)
	        #obj_id=objetivo_intervencion.objects.filter(Estudiante__id=pk)
		
			
			form = FichaEgresoForm(instance=evaluar or None)
			if request.method == 'POST':
				form = FichaEgresoForm(request.POST)
		        #codigo
		        if form.is_valid():
					instance = form.save(commit=False)
					x = datetime.date.today()
					instance.fecha_informe=x
					instance.fecha_egreso=ultimo.fecha
					instance.Estudiante=estudiante_id
					instance.usuario=request.user
					instance.save()
					infoarchivo2 = Ficha_derivacion.objects.get(id = ficha_id.id)
					infoarchivo2.pasada= 7 #porque sera visto en la lista de proximos egresados
					infoarchivo2.derivado = 2 # porque ya fue vista por el centro
					infoarchivo2.save()
					

					return redirect('derivacion:intervencion_listar')
	        	
		
		except objetivo_intervencion.DoesNotExist:
			mensaje="Estudiante sin asignación de objetivo"
			form = FichaEgresoForm(request.POST or None)
			obje=""


    #Enviar un valor pasa saber si la persona que esta activa es la misma que hiso el informe
    # si valor es 0 el usuario que hiso el informe es el mismo que esta actualmente si el 1 no es el mismo
    
		if evaluar:
			valor=1
			mensaje ="No se puede ingresar ya existe"

		else:	
		
				if intervencion:
					if yo:
						if yo == request.user:
							valor=0
						else:
							valor=1
							mensaje="El informe ya fue creado o el estudiante esta intervendio por otro profesional,  por lo cual no puede modificarlo o crearlo."
					else:
						valor=1
						mensale="Error en los permisos no pude guardar el informe"
				else:
					valor=1
					mensaje="Estudiante en bandaja de entrada aun no registra intervención"
	except sesion.DoesNotExist:
		mensaje='Debe existir a lo menos una sesión'
		form = FichaEgresoForm(request.POST or None)
		ultimo=""
		obje=""
		valor=1
		yo=""	
					
	return render(
        request,
        'sesion/ficha_egreso.html',
        context={'formulario':form,
        		'estudiante':estudiante_id,
        		 'ficha':ficha_id,
        		 'objetivo':obje,
        		 'mensaje':mensaje,
        		 'ultimo':ultimo,
        		 'valor':valor,
        		 'yo':yo,

	})



def Ficha_egresoModificar(request,pk):
	
	mensaje=""
	estudiante_id= get_object_or_404(Estudiante, pk=pk)	
	estudiante=estudiante_id.id
	ficha_id=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
	try:
		Egreso=Ficha_de_egreso.objects.get(Estudiante__id=pk)
		form = FichaEgresoForm(request.POST or None, instance=Egreso)
		valor=""
		try:
			ultimo = sesion.objects.latest('Estudiante')
	
	
			try:
				#obje= get_object_or_404(objetivo_intervencion, Estudiante__id=pk)
				obje= objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
				tem=obje.Tematicas.all()

		        #obj_id=objetivo_intervencion.objects.filter(Estudiante__id=pk)
			except objetivo_intervencion.DoesNotExist:
				obje=""
				mensaje='Debe existir definición de objetivos para realizar el informe de egreso'
				tem=""

			
			
				# if request is not post, initialize an empty form
			#form = form_class(request.POST or None) # Maybe Not 
			if request.method == 'POST':
				form = FichaEgresoForm(request.POST or None)
				instance = form.save(commit=False)
				instance.Estudiante=estudiante_id
				instance.fecha_egreso=ultimo.fecha
				instance.fecha_informe=datetime.datetime.now()	
				instance.usuario=request.user
				Egreso.delete()
				instance.save()
				return redirect('derivacion:intervencion_listar')
			
		except sesion.DoesNotExist:
				valor=1
			
	except Ficha_de_egreso.DoesNotExist:
		Egreso=None
		mensaje="No cuenta con  informe de egreso"
		obje=""
		ultimo=""
		valor=1
		form = FichaEgresoForm()

		
	
	return render(
			        request,
			        'sesion/ficha_egreso.html',
			        context={'formulario':form,
		        	'estudiante':estudiante_id,
		        	 'ficha':ficha_id,
	        		 'objetivo':obje,
	        		 'mensaje':mensaje,
	        		 'ultimo':ultimo,
	        		 'valor':valor,

	        		 
	        		 
		})


# MAnejo de infromacion de motivos de egreso
class Motivo_egresoCreate(CreateView):
	model = Motivo_egreso
	form_class = motivo_egresoForm
	template_name = 'sesion/motivo_egreso_form.html'
	success_url = reverse_lazy('sesion:Motivo_egreso_list')


class Motivo_egresoUpdate(UpdateView):
	model = Motivo_egreso
	form_class = motivo_egresoForm
	template_name = 'sesion/motivo_egreso_form.html'
	success_url = reverse_lazy('sesion:Motivo_egreso_listar')


class Motivo_egresoDelete(DeleteView):
	model = Motivo_egreso
	template_name = 'sesion/motivo_egreso_delete.html'
	success_url = reverse_lazy('sesion:Motivo_egreso_list')		
	
class Motivo_egresoList(ListView):
	model = Motivo_egreso
	template_name = 'sesion/motivo_egreso_list.html'
	paginate_by = 10


def historia(request,ficha,pk):
	
	mensaje=""
	ultimo=""
	
	dato = get_object_or_404(Estudiante, pk=pk)
	
	ficha_id=Ficha_derivacion.objects.get(pk=ficha,estado=1)
	try:
		sesiones = sesion.objects.filter(Estudiante__id=pk).order_by('fecha')
	except sesion.DoesNotExist:
		sesiones=None

	# Ultimo numero registrado en las sesiones	
	try:
		#ultimo = sesion.objects.latest('dato')
		ultimo=sesion.objects.filter(Estudiante__id=pk).latest('numero')
		
	except sesion.DoesNotExist:
		ultimo=None
	try:
		hoy= objetivo_intervencion.objects.get(Estudiante=dato,activo=1)
	except objetivo_intervencion.DoesNotExist:
		hoy=None
 
	try:
 		viejos=	objetivo_intervencionhistoria.objects.filter(Estudiante__id=pk)	
 	except viejos.DoesNotExist:
		viejos=None				
	

	try:
 		retorno=Motivo_Retorno_Ficha_derivacion.objects.get(Ficha_derivacion=ficha_id)
 		
	except Motivo_Retorno_Ficha_derivacion.DoesNotExist:
		retorno=None				
	try:
		intervenido=Intervenidos.objects.get(Estudiante__id=pk)
	except Intervenidos.DoesNotExist:
		intervenido=None
	
	try:
 		pasos=Pasos_intervencion.objects.filter(Intervenidos=intervenido)
	except Pasos_intervencion.DoesNotExist:
		pasos=None				
	try:
		estado=Estado.objects.filter(Estudiante__id=pk)
	except Estado.DoesNotExist:
		estado=None
		
	try:
		modelito= objetivo_intervencion.objects.filter(Estudiante=dato,activo=1)		
	except objetivo_intervencion.DoesNotExist:
		modelito=None
	try:
		confirma=Confirma.objects.filter(Estudiante=dato)
	except Confirma.DoesNotExist:
		confirma=None
	try:
		asiste=Registro.objects.filter(Estudiante=dato)
	except Registro.DoesNotExist:
		asiste=None
		
	
	return render(
		request,
		'sesion/historia.html',
		 context={
	     'estudiante':dato,
	     'ficha':ficha_id,
       	 'objetivo':hoy,
          'mensaje':mensaje,
          'viejos':viejos,
          'intervenido':intervenido,
          'sesiones':sesiones,
          'retorno':retorno,
          'pasos':pasos,
          'estado':estado,
          'ultimo':ultimo,
          'confirma':confirma,
          'asiste':asiste,
        		 
        		 
	})

def historia_supervisor(request,ficha,pk):
	
	mensaje=""
	ultimo=""
	
	dato = get_object_or_404(Estudiante, pk=pk)
	
	ficha_id=Ficha_derivacion.objects.get(pk=ficha,estado=1)
	try:
		sesiones = sesion.objects.filter(Estudiante__id=pk).order_by('fecha')
	except sesion.DoesNotExist:
		sesiones=None

	# Ultimo numero registrado en las sesiones	
	try:
		#ultimo = sesion.objects.latest('dato')
		ultimo=sesion.objects.filter(Estudiante__id=pk).latest('numero')
		
	except sesion.DoesNotExist:
		ultimo=None
	try:
		hoy= objetivo_intervencion.objects.get(Estudiante=dato,activo=1)
	except objetivo_intervencion.DoesNotExist:
		hoy=None
 
	try:
 		viejos=	objetivo_intervencionhistoria.objects.filter(Estudiante__id=pk)	
 	except viejos.DoesNotExist:
		viejos=None				
	

	try:
 		retorno=Motivo_Retorno_Ficha_derivacion.objects.get(Ficha_derivacion=ficha_id)
 		
	except Motivo_Retorno_Ficha_derivacion.DoesNotExist:
		retorno=None				
	try:
		intervenido=Intervenidos.objects.get(Estudiante__id=pk)
	except Intervenidos.DoesNotExist:
		intervenido=None
	
	try:
 		pasos=Pasos_intervencion.objects.filter(Intervenidos=intervenido)
	except Pasos_intervencion.DoesNotExist:
		pasos=None				
	try:
		estado=Estado.objects.filter(Estudiante__id=pk)
	except Estado.DoesNotExist:
		estado=None
		
	try:
		modelito= objetivo_intervencion.objects.filter(Estudiante=dato,activo=1)		
	except objetivo_intervencion.DoesNotExist:
		modelito=None
	try:
		confirma=Confirma.objects.filter(Estudiante=dato)
	except Confirma.DoesNotExist:
		confirma=None
	try:
		asiste=Registro.objects.filter(Estudiante=dato)
	except Registro.DoesNotExist:
		asiste=None
		
	
	return render(
		request,
		'sesion/historia_supervisor.html',
		 context={
	     'estudiante':dato,
	     'ficha':ficha_id,
       	 'objetivo':hoy,
          'mensaje':mensaje,
          'viejos':viejos,
          'intervenido':intervenido,
          'sesiones':sesiones,
          'retorno':retorno,
          'pasos':pasos,
          'estado':estado,
          'ultimo':ultimo,
          'confirma':confirma,
          'asiste':asiste,
        		 
        		 
	})



def historia_dupla(request,ficha,pk):
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	ficha_id=Ficha_derivacion.objects.get(pk=ficha,estado=1)
	
 	try: 
 		sesiones = sesion.objects.filter(Estudiante__id=pk)			
 	except sesion.DoesNotExist:
 		sesiones=None
 	
 	try:
 		intervenido=Intervenidos.objects.get(Estudiante__id=pk)
 	except Intervenidos.DoesNotExist:
 		intervenido=None
	
	try:
		modelito= objetivo_intervencion.objects.get(Estudiante=dato,activo=1)			
	except objetivo_intervencion.DoesNotExist:
		modelito=None
	
    
	try:
 		retorno=Motivo_Retorno_Ficha_derivacion.objects.get(Ficha_derivacion=ficha_id)
 		
	except Motivo_Retorno_Ficha_derivacion.DoesNotExist:
		retorno=None
    #book_id=get_object_or_404(Book, pk=pk)
	
	try:
		asiste=Registro.objects.filter(Estudiante=dato)
	except Registro.DoesNotExist:
		asiste=None

	return render(
		request,
		'sesion/historia_dupla.html',
		 context={
	     'estudiante':dato,
	     'ficha':ficha_id,
	     'sesiones':sesiones,
	     'modelito':modelito,
	     'retorno':retorno,
       	 'asiste':asiste,
          'intervenido':intervenido,
          
        		 
        		 
	})	

# Crear Seguimiento de otra isntitucion para un estudiante


def CrearSeguimiento(request,pk):
	
    #group_required = 'puede_administrar_encuestas
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	
	if request.method=='POST':
		form = SeguimientocentroForm(request.POST, request.FILES)
 		if form.is_valid():
			instance = form.save(commit=False)
			instance.Estudiante=dato
			instance.tipo_s=0
			instance.usuario = request.user
			instance.save()
			
			
			url = reverse(('sesion:seguimiento_listar'), kwargs={ 'pk': dato.id })
			return HttpResponseRedirect(url)
			
		else:
			form = SeguimientocentroForm(request.POST, request.FILES)
	
	form = SeguimientocentroForm()
	
	context = {
		"form": form,
		"dato": dato,
		
		 }
	return render(request, 'sesion/seguimiento.html', context)
	
class SeguimeintoDelete(DeleteView):

	model = Seguimiento
	template_name = 'sesion/seguimiento_eliminar.html'
	success_url = reverse_lazy('derivacion:inst_retorno')	

	def get_context_data(self, **kwargs):
		context=super(SeguimeintoDelete,self).get_context_data(**kwargs)
		return context

class SeguimientoUpdate(UpdateView):

	model = Seguimiento
	template_name = 'sesion/seguimiento.html'
	form_class = SeguimientoForm
	success_url = reverse_lazy('derivacion:inst_retorno')	

	def get_context_data(self, **kwargs):
		context=super(SeguimientoUpdate,self).get_context_data(**kwargs)
		
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		seguir=Seguimiento.objects.get(pk=pk)
		estudiante= Estudiante.objects.get(id=seguir.Estudiante.id)
		context['dato'] = estudiante
		
		return context
	


class ListarSeguimiento(ListView):
	model = Seguimiento
	template_name = 'sesion/listar_seguimiento.html'
	paginate_by = 5

		
	def get_queryset(self):
		queryset = super(ListarSeguimiento, self).get_queryset()
		return queryset.filter(Estudiante=self.kwargs['pk'],usuario=self.request.user)



def confirma_ver(request,pk,age):

	dato = get_object_or_404(Estudiante, pk=pk)
	agendo=agenda.objects.get(id=age)
	try:
		confirma=Confirma.objects.get(agenda=agendo)
	except Confirma.DoesNotExist:
		confirma=None
	
	template = 'sesion/confirma_ver.html'
    
	context = {
        "confirma": confirma,
        "agendo":agendo,
        "dato": dato,

        }
	return render(request, template, context)


def confirma_ver_busqueda(request,pk,age):

	dato = get_object_or_404(Estudiante, pk=pk)
	agendo=agenda.objects.get(id=age)
	try:
		confirma=Confirma.objects.get(agenda=agendo)
	except Confirma.DoesNotExist:
		confirma=None
	
	template = 'sesion/confirma_ver_busqueda.html'
    
	context = {
        "confirma": confirma,
        "agendo":agendo,
        "dato": dato,

        }
	return render(request, template, context)

def  confirma_modificar(request,pk,age):

	dato = get_object_or_404(Estudiante, pk=pk)
	agendo=get_object_or_404(agenda,id=age)
	

	try:
		confirma=Confirma.objects.get(agenda=agendo)
		x = datetime.date.today()
		form = Formconfirma(request.POST or None, instance=confirma)
		template = "sesion/crearconfirmacion.html"         
	
		if request.method=='POST':
			form = Formconfirma(request.POST or None, instance=confirma)
 			if form.is_valid():

				instance = form.save(commit=False)
				instance.usuario = request.user
				instance.Estudiante=dato
				instance.fecha_creacion=x
				instance.save()
	        
				url = reverse(('sesion:intervencion_listar'), kwargs={ 'pk': dato.id })
				return HttpResponseRedirect(url)

	except Confirma.DoesNotExist:
		confirma=None
		form = Formconfirma(request.POST or None, instance=confirma)
		mensaje="Estudiante sin confirmación para modificar"
		template = "sesion/crearconfirmacion.html"         
		context={
	        "dato": dato,
	        "formulario": form,
	        "agendo":agendo,
	        "mensaje":mensaje,

	        }


		return render(request, template, context) 
	
	
        
	context={
	        "dato": dato,
	        "formulario": form,
	        "agendo":agendo,
	        }


	return render(request, template, context) 


	


