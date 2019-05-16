# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView,TemplateView
from dupla.models import Ficha_derivacion_dupla,Entrevista_ingreso_dupla,DiagnosticoI,Logros,Intervencion_casos, \
Intervencion_sesion,Intervencion_convivencia,Intervencion_convivencia_curso,Relacion_Intervencion_convivencia_estudiante, \
Intervencion_convivencia_mediacion,Continuidad_dupla,Derivacion_Ficha_derivacion_dupla

from sesion.models import Seguimiento
from plan.models import Actividades,Plan,Plancillo,Base,Accion,Planes_externos,Hecho_Actividades,Indicador_base

from dupla.forms import derivacionduplaForm,Entrevista_ingreso_duplaForm,Diagnostico_duplaForm,IndicadorAuto_duplaForm,Intervencion_casosForm, \
		Intervencion_sesionForm,Intervencion_convivenciaForm,Derivacion_Ficha_derivacionForm,Intervencion_convivencia_cursoForm, \
		BuscarMoverForm,Intervencion_sesioninicialForm,SeguimientoForm,Intervencion_convivencia_mediacionForm, ContinuidadForm

from bitacora.models import Lista
from derivacion.models import Ficha_derivacion,Motivo_Retorno_Ficha_derivacion
from sesion.models import sesion,Intervenidos,objetivo_intervencion
from alumno.models import Estudiante,establecimiento,Escolaridad,curso
from profesional.models import Cargo,Profesional
from secretaria.models import Registro 
from django.db.models import Q
from django.urls import reverse
import datetime
import math

#Proceso de busquedad 

import operator


class Ficha_derivacion_duplas(CreateView):
	model = Ficha_derivacion_dupla	
	form_class = derivacionduplaForm
	template_name = 'dupla/ficha_derivacion_dupla.html'
	success_url = reverse_lazy('alumno:listar_estudiantes_establecimiento')
	
	    
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(Ficha_derivacion_duplas, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL


		try:
			ficha=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk)
			mensaje="Estudiante ya cuenta con ficha de derivación"
		except Ficha_derivacion_dupla.DoesNotExist:
			mensaje=""
		
		
		context['dato']=Estudiante.objects.get(id=pk)
		context['mensaje']=mensaje
		indice = self.kwargs.get('establecimiento')
		escuela=establecimiento.objects.get(pk=indice)
		context['escuela']=escuela
		return context
		
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST,request.FILES)
		
		if form.is_valid():
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			colegio=self.kwargs.get('establecimiento') # El mismo nombre que en tu URL
			escuela=establecimiento.objects.get(id=colegio)
			try:
				ficha=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk)
				return self.render_to_response(self.get_context_data(form=form))
			except Ficha_derivacion_dupla.DoesNotExist:
				
				form.instance= form.save(commit=False)
				#motivos=form.instance.Motivo_derivacion
				#for motivo in motivos:

				#	form.intance.Motivo_derivacion.add(motivo)
				form.instance.establecimiento = establecimiento.objects.get(id=colegio)
				form.instance.usuario = self.request.user
				form.instance.pasada=1
				form.instance.derivado=1
				
				estudiante=Estudiante.objects.get(id=pk)
				form.instance.Estudiante=estudiante
				#Campos para registrar valores al moemnto de crear la ficha
				form.instance.edad=estudiante.edad
				
				form.instance.curso=estudiante.curso.get_numero()
				form.instance.letra=estudiante.curso.get_letra()
				form.instance.save()
				form.save_m2m()
			
				
				
				url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': estudiante.curso.establecimiento.id })
				return HttpResponseRedirect(url)

		else:
			mensaje="Ficha ya existe"
			return self.render_to_response(self.get_context_data(form=form))

# Modificar una ficha interna dupla
def FichaderivacionduplaUpdate(request,pk):
# modificar un indicador el cual depende de una base de un plan para un establecimiento
	
	mensaje=""
	estudiante= get_object_or_404(Estudiante, pk=pk)
	try:
		ficha=Ficha_derivacion_dupla.objects.get(Estudiante=estudiante,estado=1)
	except Ficha_derivacion_dupla.DoesNotExist:
		ficha=None
		mensaje="Estudiante sin ficha de derivación para modificar"
	
	colegio=estudiante.curso.establecimiento

	
	if request.method=='POST':
		formulario = derivacionduplaForm(request.POST or None, instance=ficha)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.usuario = request.user
				
			instance.save()
			formulario.save_m2m()
		
				
				
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': colegio.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = derivacionduplaForm(request.POST or None, instance=ficha)
	else:


				
		formulario = derivacionduplaForm(request.POST or None, instance=ficha)
	context = {
		"form": formulario,
		"ficha":ficha,
		"dato":estudiante,
		"mensaje":mensaje,


		 }
	return render(request, 'dupla/ficha_derivacion_dupla.html', context)


#Ficha de un estudiante desde la dupla
def FichaDuplaDetailView(request,pk):


	try:
		estudiante_id=Estudiante.objects.get(pk=pk)
		colegio=Escolaridad.objects.get(Estudiante__id=pk)
	except Estudiante.DoesNotExist:
		estudiante_id=None
	try:
		ficha_id=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk)
	except Ficha_derivacion_dupla.DoesNotExist:
		ficha_id=None		
		

    #book_id=get_object_or_404(Book, pk=pk)
	return render(
        request,
        'dupla/dupla_ver_ficha.html',
        context={'estudiante':estudiante_id,
        		 'ficha':ficha_id,
        		 'colegio':colegio	}
    )

# Modificar una ficha de ingreso parte del proceso de las duplas 
def FichaingresonduplaUpdate(request,pk):
# modificar un indicador el cual depende de una base de un plan para un establceimiento
	
	mensaje=""
	estudiante= get_object_or_404(Estudiante, pk=pk)

	try:
		ficha=Ficha_derivacion_dupla.objects.get(Estudiante=estudiante,estado=1)
	
		try:
			ficha_ingreso=Entrevista_ingreso_dupla.objects.get(ficha_derivacion_dupla=ficha)
			
		except Entrevista_ingreso_dupla.DoesNotExist:
			ficha_ingreso=None	
			mensaje="Estudiante sin ficha para modificar"
	except Ficha_derivacion_dupla.DoesNotExist:
		ficha=None
		ficha_ingreso=None
		mensaje="Estudiante sin ficha de ingreso para modificar"
		colegio=estudiante.curso.establecimiento

	
	if request.method=='POST':
		estudiante= get_object_or_404(Estudiante, pk=pk)
		colegio=estudiante.curso.establecimiento

		
 
		formulario = Entrevista_ingreso_duplaForm(request.POST , request.FILES or None, instance=ficha_ingreso)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.usuario = request.user
			#instance.save()
			instance.save()
			formulario.save_m2m()

		
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': colegio.id})
			return HttpResponseRedirect(url)
		else:		
			
				
			formulario = Entrevista_ingreso_duplaForm(request.POST, request.FILES or None, instance=ficha_ingreso)
	else:


		print("Fecha y Hora:", ficha_ingreso) 			
		formulario = Entrevista_ingreso_duplaForm(instance=ficha_ingreso)
	context = {
		"form": formulario,
		"ficha":ficha,
		"ficha_dupla":ficha,

		"ficha_ingreso":ficha_ingreso,
		"entrevista_ingreso":ficha_ingreso,
		"dato":estudiante,
		"mensaje":mensaje,


		 }
	return render(request, 'dupla/Entrevista_ingreso_dupla.html', context)

class Estudiante_listar_fichas_duplas(ListView):
	model = Ficha_derivacion_dupla
	template_name = 'dupla/Estudiante_listar_fichas_duplas.html'
	

	def get_context_data(self, **kwargs):
		context = super(Estudiante_listar_fichas_duplas, self).get_context_data(**kwargs)

		colegio=establecimiento.objects.get(id=self.kwargs['pk'])
		usuario=self.request.user
		profesional=Profesional.objects.get(usuario=usuario)
		estado=profesional.tipo_profesional
		ficha= Ficha_derivacion_dupla.objects.filter(Q(establecimiento=colegio) & Q(pasada=1)) 
		context['ficha']=ficha
		context['colegio']=colegio
		

		return context
	    #if estado==4:
	    #	return qs.filter(Q(establecimiento=colegio.nombre) & Q(pasada=2)) 
	    #else:
	    #	success_url = reverse_lazy('alumno:listar_estudiantes_establecimiento')
	    

class entrevista_ingreso_dupla(CreateView):
	model = Entrevista_ingreso_dupla	
	form_class = Entrevista_ingreso_duplaForm
	template_name = 'dupla/Entrevista_ingreso_dupla.html'
	success_url = reverse_lazy('alumno:listar_estudiantes_establecimiento')
	    
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(entrevista_ingreso_dupla, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET,request.FILES)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		mensaje=""
		try:
			dato=Estudiante.objects.get(id=pk)
			ficha_dupla=Ficha_derivacion_dupla.objects.get(Estudiante=dato,estado=1)# Ficha de derivacion activa
			profe_jefe=ficha_dupla.profe_jefe
			try:
				entrevista_ingreso=Entrevista_ingreso_dupla.objects.get(ficha_derivacion_dupla=ficha_dupla)
			except Entrevista_ingreso_dupla.DoesNotExist:
				entrevista_ingreso=None
		except Ficha_derivacion_dupla.DoesNotExist:
			profe_jefe=None
			ficha_derivacion_dupla=None
			ficha_dupla=None
			mensaje='Estudiante sin ficha de derivación '
			try:
				entrevista_ingreso=Entrevista_ingreso_dupla.objects.get(ficha_derivacion_dupla=ficha_dupla)
			except Entrevista_ingreso_dupla.DoesNotExist:
				entrevista_ingreso=None

		
		context['dato']=Estudiante.objects.get(id=pk)
		context['mensaje']=mensaje
		establecimiento=Estudiante.objects.get(id=pk)
		escuela=establecimiento.curso.establecimiento.nombre
		context['escuela']=escuela
		context['ficha_dupla']=ficha_dupla
		context['entrevista_ingreso']=entrevista_ingreso
		context['profe_jefe']=profe_jefe

		return context
		
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST,request.FILES)
		
		if form.is_valid():
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			estudiante=Estudiante.objects.get(id=pk)
			ficha_derivacion_dupla=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk)	
			form.instance= form.save(commit=False)
				#motivos=form.instance.Motivo_derivacion
				#for motivo in motivos:

				#	form.intance.Motivo_derivacion.add(motivo)
			form.instance.usuario = self.request.user
			form.instance.quien_deriva=self.request.user.username+" "+self.request.user.first_name+" "+self.request.user.last_name

				
			form.instance.ficha_derivacion_dupla=ficha_derivacion_dupla
			
				#Campos para registrar valores al moemnto de crear la ficha
				
			form.instance.save()
			
			
				
				
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': estudiante.curso.establecimiento.id })
			return HttpResponseRedirect(url)

		else:
			mensaje="Ficha ya existe"
			return self.render_to_response(self.get_context_data(form=form))

#visualizar una entrevista de ingreso
def Ver_entrevista_ingreso(request,pk):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	try:
		ficha=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk,estado=1)
		
	except Ficha_derivacion_dupla.DoesNotExist:
		mensaje="Estudiante sin Ficha derivación dupla"	
		ficha=None
	
	
	ficha_id=Entrevista_ingreso_dupla.objects.all()
	form = Entrevista_ingreso_duplaForm(instance=ficha_id or None)

	form = Entrevista_ingreso_duplaForm()
	

					
	return render(
        request,
        'dupla/entrevista_ingreso_dupla_ver.html',
        context={'formulario':form,
        		'dato':estudiante_id,
        		 'ficha':ficha_id,
        		 
        		 'mensaje':mensaje,
        		 
        		 

	})




def DiagnosticoListView(request,pk):
#Registrar los logros de cada uno,  para cada diagnostico


	try:
		colegio=establecimiento.objects.get(id=pk)
		x= datetime.datetime.now()
		
		y = datetime.datetime.now().year 
		

		diagnostico=DiagnosticoI.objects.get(establecimiento=colegio,annio=y)
		
		logros=Logros.objects.filter(diagnostico=diagnostico)
	except DiagnosticoI.DoesNotExist:
		diagnostico=None
		logros=None

	if request.method == 'POST':

		colegio=establecimiento.objects.get(id=pk)
		x= datetime.datetime.now()
		
		y = datetime.datetime.now().year 
		diagnostico=DiagnosticoI.objects.get(establecimiento=colegio,annio=y)
		print(diagnostico)
		form = IndicadorAuto_duplaForm(request.POST)
		if form.is_valid():
			form.instance= form.save(commit=False)
			print (form.instance.porcentaje)
			if form.instance.porcentaje>0 and form.instance.porcentaje<=100: 
				form.instance.diagnostico=diagnostico
				form.save()
				return redirect('dupla:DiagnosticoListView', pk=pk)
			
						
		
	else:
		form = IndicadorAuto_duplaForm()
	
		
	

	form = IndicadorAuto_duplaForm()
	return render(
        request,
        'dupla/diagnostico_ver_ficha.html',
        context={'colegio':colegio,
        		 'diagnostico':diagnostico,
        		 'form':form,
        		 'logros':logros,}
    )



def DiagnosticoListView_Ver_todos(request,pk,anio):
#Registrar los logros de cada uno,  para cada diagnostico


	try:
		colegio=establecimiento.objects.get(id=pk)
		diagnostico=DiagnosticoI.objects.get(establecimiento=colegio,annio=anio)
		print diagnostico
		logros=Logros.objects.filter(diagnostico=diagnostico)
	except DiagnosticoI.DoesNotExist:
		diagnostico=None
		logros=''

	
	return render(
        request,
        'dupla/diagnostico_ver_ficha_todos.html',
        context={'colegio':colegio,
        		 'diagnostico':diagnostico,
        		 'logros':logros,}
    )



def DiagnosticoListViewTodos(request,pk):
#Registrar los logros de cada uno,  para cada diagnostico

	
		
	colegio=establecimiento.objects.get(id=pk)
			
			
	try:
		diagnostico=DiagnosticoI.objects.filter(establecimiento=colegio)
		logros=Logros.objects.filter(diagnostico=diagnostico)
	except DiagnosticoI.DoesNotExist:
		diagnostico=None
	
		
	return render(
        request,
        'dupla/diagnostico_todos.html',
        context={'colegio':colegio,
        		 'diagnostico':diagnostico,
        		 
        		 'logros':logros,}
    )



class ingresar_diagnostico(CreateView):
	model = DiagnosticoI	
	form_class = Diagnostico_duplaForm
	template_name = 'dupla/diagnostico_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ingresar_diagnostico, self).get_context_data(**kwargs)
			colegio = self.kwargs.get('pk') # El mismo nombre que en tu URL
			escuela=establecimiento.objects.get(id=colegio)
			try:
				x= datetime.date.today() 
				
				print str(int(x.year))
				diagnostico=DiagnosticoI.objects.get(establecimiento=escuela, annio=str(int(x.year)))
				print diagnostico
				context['escuela']=escuela
				context['diagnostico']=diagnostico
				context['mensaje']='--Ya cuenta con diagnóstico'
				return context
			except DiagnosticoI.DoesNotExist:
				context['escuela']=escuela
				context['mensaje']=''
				context['diagnostico']=''
				
				return context
			
			

		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST,request.FILES)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			
		if request.method == 'POST':
			form = Diagnostico_duplaForm(request.POST)
		        #codigo
			if form.is_valid():
				pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
				escuela=establecimiento.objects.get(id=pk)
				try:
					x= datetime.date.today() 
					annio=str(int(x.year))
					diagnostico=DiagnosticoI.objects.get(establecimiento=escuela,annio=annio)
					return self.render_to_response(self.get_context_data(form=form))
				except DiagnosticoI.DoesNotExist:
					instance = form.save(commit=False)
					

					instance.establecimiento=establecimiento.objects.get(id=pk)
					
					instance.usuario=self.request.user
					x= datetime.date.today() 
					
					
					instance.annio=str(int(x.year))

					instance.save()

					url = reverse(('dupla:DiagnosticoListView'), kwargs={ 'pk': pk })
					return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(form=form))


def modificar_diagnostico(request,pk):
# Realizar un retorno de una ficha de derivacion a la dupla 
	
	diagnostico = get_object_or_404(DiagnosticoI, pk=pk)
	escuela=diagnostico.establecimiento
	if request.method=='POST':
		formulario = Diagnostico_duplaForm(request.POST or None, instance=diagnostico)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.establecimiento=diagnostico.establecimiento
			instance.usuario = request.user
			instance.save()
			url = reverse(('dupla:DiagnosticoListView'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)
				
		formulario = Diagnostico_duplaForm(request.POST or None, instance=diagnostico)
	else:


				
		form = Diagnostico_duplaForm(request.POST or None, instance=diagnostico)
	context = {
		"form": form,
		
		"diagnostico":diagnostico,
		"escuela":escuela,
		 }
	return render(request, 'dupla/diagnostico_form.html', context)	

class indicador_auto(CreateView):
	model = Logros
	form_class = IndicadorAuto_duplaForm
	template_name = 'dupla/indicador_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(indicador_auto, self).get_context_data(**kwargs)
		
		context['dato']="Motivación Escolar"
		context['dimension']="Autoestima Académica y Motivación Escolar"

		
		return context

# Proceso de creación de pla de intervencion
class Intervencion_casosCrear(CreateView):
	model = Intervencion_casos	
	form_class = Intervencion_casosForm
	template_name = 'dupla/crear_intervencion_casos.html'
	success_url = reverse_lazy('alumno:listar_estudiantes_establecimiento')
	
	
	    
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(Intervencion_casosCrear, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		colegio = self.kwargs.get('colegio') # El mismo nombre que en tu URL
		estudiante=Estudiante.objects.get(id=pk)
		escuela=establecimiento.objects.get(id=colegio)
		try:
			plan_intervencion=Intervencion_casos.objects.get(estudiante=estudiante)
			mensaje="Estudiante cuenta con un plan de intervención"
		except Intervencion_casos.DoesNotExist:
			mensaje=''	

		try:
			ficha_derivacion_dupla=Ficha_derivacion_dupla.objects.get(Estudiante=estudiante)
		except Ficha_derivacion_dupla.DoesNotExist:
			mensaje="Para ingresar plan de intervención de casos DEBE INGRESAR FICHA DE DERIVACIÓN INTERNA"
			
		

		print mensaje
		context['estudiante']=estudiante
		context['colegio']=escuela
		context['mensaje']=mensaje
		
		return context
		
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			colegio= self.kwargs.get('colegio') # El mismo nombre que en tu URL
			escuela=establecimiento.objects.get(id=colegio)
			estudiante=Estudiante.objects.get(id=pk)
			
				#motivos=form.instance.Motivo_derivacion
				#for motivo in motivos:

				#	form.intance.Motivo_derivacion.add(motivo)
			try:
				form.instance= form.save(commit=False)
				ficha_derivacion_dupla=Ficha_derivacion_dupla.objects.get(Estudiante=estudiante)	
				print ficha_derivacion_dupla
				form.instance.usuario = self.request.user
				form.instance.estudiante=estudiante
				form.instance.ficha_derivacion_dupla=ficha_derivacion_dupla
				#Campos para registrar valores al moemnto de crear la ficha

				form.instance.save()
				form.save_m2m()
				url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={'pk': escuela.id })
				return HttpResponseRedirect(url)
			
			except Ficha_derivacion_dupla.DoesNotExist:
					
				url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={'pk': escuela.id })
				return HttpResponseRedirect(url)
				
		else:
			mensaje="Ficha ya existe"
			return self.render_to_response(self.get_context_data(form=form))

#Ver el plan de intervencion de un estudiante
def IntervencionCasosDetailView(request,pk):


	try:
		estudiante_id=Estudiante.objects.get(pk=pk)
		plan=Intervencion_casos.objects.get(estudiante=estudiante_id)

		try:
			sesiones=Intervencion_sesion.objects.filter(intervencion_casos=plan).order_by('fecha')
			
		except Intervencion_sesion.DoesNotExist:
			sesiones=None
	except Intervencion_casos.DoesNotExist:
		plan =None
		sesiones=None

	if request.method == 'POST':

		estudiante_id=Estudiante.objects.get(pk=pk)
		
		plan=Intervencion_casos.objects.get(estudiante=estudiante_id)
		
		form = Intervencion_sesioninicialForm(request.POST)
		if form.is_valid():
			
			try:
				agendado=Lista.objects.get(fecha=form.instance.fecha,horario=form.instance.horario,usuario=request.user)
				estado="Error no disponible"
				
				return redirect('comienza:mi_error_404')
			except Lista.DoesNotExist:
				
				form.instance= form.save(commit=False)
				form.instance.intervencion_casos=plan
				form.instance.usuario=request.user
				#Ingreso de datos a campos no llenados anteriormente con el formulario
				form.objetivo_especifico=""
				form.tematicas=""
				form.observacion=""
				form.participantes=""
				form.numero=0
				form.instance.save()
				form.save_m2m()
				sesion=Intervencion_sesion.objects.get(fecha=form.instance.fecha,horario=form.instance.horario,usuario=request.user)
				
				# Registrar la sesion en un la lista de la bitacora
				Lista.objects.create(fecha=form.instance.fecha,horario=form.instance.horario,nombre='Atención de caso',
							curso=estudiante_id.curso.numero,tipo_letras=estudiante_id.curso.letra,
							ambito=2,tipo_actividad=13,participantes=form.instance.participantes,
							establecimiento=estudiante_id.curso.establecimiento,desarrollo="",
							numero=1,sesion=sesion,usuario=form.instance.usuario)


				estado="ingresada"
				
				return redirect('dupla:IntervencionCasosDetailView', pk=pk)
							
	else:
		form = Intervencion_sesioninicialForm()	


    #book_id=get_object_or_404(Book, pk=pk)
	estado=""
	
	return render(
        request,
        'dupla/dupla_ver_intervencioncasos.html',
        context={'estudiante':estudiante_id,
        		 'plan':plan,
        		 'colegio':estudiante_id.curso.establecimiento,
        		 'form':form,
        		 'sesiones':sesiones,
        		 'estado':estado,

        		 	}
    )



# Modificar plan de caso
def PlanCasosUpdate(request,pk):
# modificar un indicador el cual depende de una base de un plan para un establceimiento
	
	mensaje=""
	estudiante= get_object_or_404(Estudiante, pk=pk)
	try:
		casos=Intervencion_casos.objects.get(estudiante=estudiante)
	except Intervencion_casos.DoesNotExist:
		casos=None
		mensaje="Estudiante sin plan de intervención para modificar"
	
	colegio=estudiante.curso.establecimiento

	
	if request.method=='POST':
		formulario = Intervencion_casosForm(request.POST or None, instance=casos)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.usuario = request.user
				
			instance.save()
			formulario.save_m2m()
		
				
				
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': colegio.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Intervencion_casosForm(request.POST or None, instance=casos)
	else:


				
		formulario = Intervencion_casosForm(request.POST or None, instance=casos)
	context = {
		"form": formulario,
		"casos":casos,
		"dato":estudiante,
		"mensaje":mensaje,
		"colegio":colegio,


		 }
	return render(request, 'dupla/crear_intervencion_casos.html', context)

# Listar una intervencion de casos 
def Dupla_casos(request,pk):
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	
	try:
		ficha=Ficha_derivacion_dupla.objects.get(Estudiante=dato,estado=1)
		try:
			plan_caso=Intervencion_casos.objects.get(ficha_derivacion_dupla=ficha)
			try:
				sesiones=Intervencion_sesion.objects.filter(intervencion_casos=plan_caso)
			except Intervencion_sesion.DoesNotExist:	
				sesiones=None
			
		except Intervencion_casos.DoesNotExist:
			plan_caso=None
			sesiones=None
	except Ficha_derivacion_dupla.DoesNotExist:
		ficha=None
		sesiones=None
		plan_caso=None

	
	try:
		retorno=Derivacion_Ficha_derivacion_dupla.objects.get(ficha_derivacion_dupla=ficha,ficha_derivacion_dupla__estado=1)
	except Derivacion_Ficha_derivacion_dupla.DoesNotExist:
		retorno=None

	return render(
		request,
		'dupla/casos_dupla.html',
		 context={
	     'estudiante':dato,
	     'ficha':ficha,
	     'sesiones':sesiones,
	     'retorno':retorno,
       	 'plan_caso':plan_caso,
         
          
        		 
        		 
	})



#Modificar una sesion de intervencion

def SesionDuplaUpdate(request,pk,colegio):

    #group_required = 'puede_administrar_encuestas
	mensaje=""

	sesion = get_object_or_404(Intervencion_sesion, pk=pk)
	
	if request.method=='POST':
		formulario = Intervencion_sesionForm(request.POST)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			try:
 			 # try something
	 			hoy=Intervencion_sesion.objects.get(Q(fecha=instance.fecha) & Q(horario=instance.horario)& Q(usuario=request.user))
	 			
			except Intervencion_sesion.DoesNotExist:
			  # do something
				hoy=None
				
			if hoy==None:	
				instance.intervencion_casos=sesion.intervencion_casos
				instance.usuario = request.user
				instance.save()
				return HttpResponseRedirect('/calendario/show/calendar')
			else:
				mensaje='Horario ocupado por '+hoy.intervencion_casos.estudiante.nombres+" "+hoy.intervencion_casos.estudiante.firs_name+" "+hoy.intervencion_casos.estudiante.last_name
				formulario = Intervencion_sesionForm(request.POST or None, instance=hoy)
	else:
		formulario = Intervencion_sesionForm()
	
	context = {
		"formulario": formulario,
		"sesion": sesion,
		"mensaje":mensaje,
		 }
	return render(request, 'sesion/formcita_nueva.html', context)

#Modificar una cita
def ModificarCita(request,pk,colegio):


	
	sesion = get_object_or_404(Intervencion_sesion, pk=pk)
	caso=sesion.intervencion_casos
	estudiante=caso.estudiante
	colegio = get_object_or_404(establecimiento, pk=colegio)
	mensaje=""

	
	if request.method=='POST':
		formulario = Intervencion_sesionForm(request.POST or None, instance=sesion)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			try:
 			 
	 			hoy=Intervencion_sesion.objects.get(Q(fecha=instance.fecha) & Q(horario=instance.horario)& Q(usuario=request.user))
	 			instance.intervencion_casos=sesion.intervencion_casos
				instance.usuario = request.user
				instance.save()
				formulario.save_m2m()
				mensaje="Fecha / Hora / usuario ocupados"

				#borrar la cita de la Bitacora diaria ( Lista)
				agendado=Lista.objects.get(Q(fecha=instance.fecha) & Q(horario=instance.horario)& Q(usuario=request.user))
				
				agendado.delete()
				if instance == 1:
					numero=1

	 			Lista.objects.create(fecha=instance.fecha,horario=instance.horario,nombre='Atención de caso',
						curso=estudiante.curso.numero,tipo_letras=estudiante.curso.letra,
						ambito=1,tipo_actividad=0,participantes=instance.participantes,
						establecimiento=estudiante.curso.establecimiento,desarrollo="",
						numero=numero,usuario=instance.usuario)
	
			except Intervencion_sesion.DoesNotExist:
				instance.intervencion_casos=sesion.intervencion_casos
				instance.usuario = request.user
				
				instance.save()
				
				mensaje="Sesión modificada exitosamente"


				instance.intervencion_casos=sesion.intervencion_casos
				instance.usuario = request.user					
				instance.save()
			
				formulario.save_m2m()

				
			url = reverse(('dupla:IntervencionCasosDetailView'), kwargs={ 'pk': estudiante.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Intervencion_sesionForm(request.POST or None, instance=sesion)
	else:


				
		formulario = Intervencion_sesionForm(request.POST or None, instance=sesion)
	context = {
		"form": formulario,
		"mensaje":mensaje,
		"sesion":sesion,
		"colegio":colegio,
		 }
	return render(request, 'dupla/intervencion_sesion_form.html', context)

class eliminar_cita(DeleteView):
	model = Intervencion_sesion
	template_name = 'dupla/eliminar_cita.html'

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(eliminar_cita, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		a=self.kwargs.get('pk') # El mismo nombre que en tu URL
		cita=Intervencion_sesion.objects.get(id=a)
		caso=cita.intervencion_casos
		estudiante=caso.estudiante
		
		context['cita']=cita
		context['caso']=caso
		context['estudiante']=estudiante
		

		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(eliminar_cita, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		cita=Intervencion_sesion.objects.get(pk=pk)
		#ir a buscar la cita a la bitacora
		agendado=Lista.objects.get(sesion=cita)
		caso=cita.intervencion_casos
		estudiante=caso.estudiante
		agendado.delete()
		object.delete()
		
        # Retornamos el objeto
		url = reverse(('dupla:IntervencionCasosDetailView'), kwargs={ 'pk': estudiante.id})
		return HttpResponseRedirect(url)

#Modificar una derivacion a otra institucion 
# Modificar una derivacion a otra institucion 
# Realizado el viernes 4 de mayo por error capacitacion de dani
def ModificarRetornoDefinitivo(request,pk):
# Realizar un retorno de una ficha de derivacion a la dupla 
	
	dato = get_object_or_404(Estudiante, pk=pk)
	try:
		ficha=Ficha_derivacion_dupla.objects.get(Estudiante=dato,estado=1)
		try:
			retorno_ficha=Derivacion_Ficha_derivacion_dupla.objects.get(ficha_derivacion_dupla=ficha)
		except Derivacion_Ficha_derivacion_dupla.DoesNotExist:
			retorno_ficha=None	
	except Ficha_derivacion_dupla.DoesNotExist:
		ficha=None
		try:
			retorno_ficha=Derivacion_Ficha_derivacion_dupla.objects.get(ficha_derivacion_dupla=ficha)
		except Derivacion_Ficha_derivacion_dupla.DoesNotExist:
			retorno_ficha=None	
	
	
	
	if request.method=='POST':
		formulario = Derivacion_Ficha_derivacionForm(request.POST,request.FILES,instance=retorno_ficha)
		
 		if formulario.is_valid():
 			instance = formulario.save(commit=False)
 			if instance.docfile1 !=  None:
 				instance.docfile1=request.FILES['docfile1']
 			if instance.docfile2 !=  None:
 				instance.docfile2=request.FILES['docfile2']
 			if instance.docfile3 !=  None:
 				instance.docfile3=request.FILES['docfile3']
			instance.ficha_derivacion_dupla=ficha
			instance.fecha_retorno=datetime.datetime.now()
			instance.usuario=request.user
			instance.save()
			
			infoarchivo2 = Ficha_derivacion_dupla.objects.get(id = ficha)
			infoarchivo2.pasada= 4 #porque pasa a otra institucion, si una ficha pasa a otra institucion 
			#automaticamente queda en la lista de los podibles egresados ya que se va del centro

			infoarchivo2.derivado = 2 # porque ya fue vista por el centro
			infoarchivo2.estado = 1 # porque aun sigue estando activa dentro del centro
			infoarchivo2.save()
			#inter=Intervenidos.objects.get(Estudiante=dato)
			#inter.activo=2
			#inter.save()


	if request.method == 'POST':
		formulario = Derivacion_Ficha_derivacionForm(request.POST,request.FILES,instance=retorno_ficha)
		if formulario.is_valid():
			formulario.save(commit=False)
			usuario=request.user
			formulario.save()

			return HttpResponseRedirect('/derivacion/intervencion_otrar')

	else:
		formulario = Derivacion_Ficha_derivacionForm(instance=retorno_ficha)
		


	context = {
		"formulario": formulario,
		"dato": dato,
		"ficha":ficha,
		 }
	return render(request, 'dupla/pasada_retorno_modificar.html', context)	




#Logicas para controlar las acciones de convivencia escolar del establecimiento 
def listar_convivencia_escolar(request,pk):
		
	colegio=establecimiento.objects.get(id=pk)
	
	estudiando=Intervencion_convivencia.objects.filter(establecimiento=colegio,usuario=request.user).order_by('fecha')
	estudiando1=Intervencion_convivencia_curso.objects.filter(establecimiento=colegio,usuario=request.user).order_by('fecha')
	estudiando2=Intervencion_convivencia_mediacion.objects.filter(establecimiento=colegio,usuario=request.user).order_by('fecha')
	


	contexto = {'estudiando':estudiando,
				'estudiando1':estudiando1,
				'estudiando2':estudiando2,
				

				'escuela':colegio,

				 }
	return render(request, 'dupla/listar_convivencia_escolar.html', contexto)

#Crear un evento de convivencia escolar

class indicador_convivencia(CreateView):
	model = Intervencion_convivencia
	form_class = Intervencion_convivenciaForm
	template_name = 'dupla/convivencia_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(indicador_convivencia, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		colegio=establecimiento.objects.get(id=pk)
		context['colegio']=colegio
		
		return context
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			colegio=establecimiento.objects.get(id=pk)# El mismo nombre que en tu URL
			form.instance= form.save(commit=False)
			#el nombre de cada uno de los if es el mismo de la base de datos
			# asi que no se pueden cambiar 
			try:
				agendado=Lista.objects.get(fecha=form.instance.fecha,horario=form.instance.horario,usuario=request.user)
				mensaje="Error no disponible"
				return redirect('dupla:Fallaconvivencia')
			except Lista.DoesNotExist:
				
				#Crear el evento en la botacora
				# Registrar la sesion en un la lista de la bitacora
				Lista.objects.create(fecha=form.instance.fecha,horario=form.instance.horario,nombre='Convivencia escolar',
							curso=15,tipo_letras=5,
							ambito=3,tipo_actividad=14,participantes=form.instance.participantes,
							establecimiento=colegio,desarrollo='Convivencia escolar',numero=2,usuario=request.user)

				form.instance.usuario = self.request.user
				form.instance.establecimiento=colegio
				form.instance.evento=None
						
				form.instance.save()
				form.save_m2m()
				
				url = reverse(('dupla:listar_convivencia_escolar'), kwargs={ 'pk': colegio.id })
				return HttpResponseRedirect(url)

		else:
			
			return self.render_to_response(self.get_context_data(form=form))	

#Evento de convivencia escolar con un curso

class indicador_convivencia_curso(CreateView):
	model = Intervencion_convivencia_curso
	form_class = Intervencion_convivencia_cursoForm
	template_name = 'dupla/convivencia_cursoform.html'
	success_url = reverse_lazy('comienza:ver_dupla')
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(indicador_convivencia_curso, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		colegio=establecimiento.objects.get(id=pk)
		context['colegio']=colegio
		
		return context
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			colegio=establecimiento.objects.get(id=pk)# El mismo nombre que en tu URL
			form.instance= form.save(commit=False)
			#el nombre de cada uno de los if es el mismo de la base de datos
			# asi que no se pueden cambiar 
			try:
				agendado=Lista.objects.get(fecha=form.instance.fecha,horario=form.instance.horario,usuario=request.user)
				mensaje="Error no disponible"
				return redirect('dupla:listar_convivencia_escolar', pk=pk)
			except Lista.DoesNotExist:
				
				#Crear el evento en la botacora
				# Registrar la sesion en un la lista de la bitacora
				Lista.objects.create(fecha=form.instance.fecha,horario=form.instance.horario,nombre='Convivencia escolar',
							curso=form.instance.curso,tipo_letras=form.instance.letra,
							ambito=3,tipo_actividad=15,participantes=form.instance.participantes,
							establecimiento=colegio,desarrollo='Convivencia escolar',numero=2,usuario=request.user)

				form.instance.usuario = self.request.user
				form.instance.establecimiento=colegio
				form.instance.evento=None
				form.instance.tipo_convivencia=1
						
				form.instance.save()
				form.save_m2m()
				
				url = reverse(('dupla:listar_convivencia_escolar'), kwargs={ 'pk': colegio.id })
				return HttpResponseRedirect(url)

		else:
			
			return self.render_to_response(self.get_context_data(form=form))	


#Evento de convivencia escolar para los estudiantes 

	
def ConvivenciaListView(request,pk):
#Registrar los bases para cada plan

	try:
		colegio=establecimiento.objects.get(id=pk)
		convivencia=Intervencion_convivencia.objects.filter(establecimiento=colegio)
		base=Base.objects.filter(plan=plan)
		
	except Plan.DoesNotExist:
		plan =None

	if request.method == 'POST':

		colegio=establecimiento.objects.get(id=pk)
		
		plan=Plan.objects.get(establecimiento=colegio)
		
		form = Intervencion_convivenciaForm(request.POST)
		if form.is_valid():
			form.instance= form.save(commit=False)
			
			
			form.instance.plan=plan
			form.instance.usuario=request.user
			form.save()
			return redirect('plan:PlanListView', pk=pk)
				
	else:
		form = Intervencion_convivenciaForm()
	
	form = Intervencion_convivenciaForm()
	return render(
        request,
        'plan/plan_ver_ficha.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'form':form,
        		 'base':base,
        		 }
    )
# Creación de evento convivencia escolar medicion
class indicador_convivencia_mediacion(CreateView):
	model = Intervencion_convivencia_mediacion
	form_class = Intervencion_convivencia_mediacionForm
	template_name = 'dupla/convivencia_mediacion_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(indicador_convivencia_mediacion, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		colegio=establecimiento.objects.get(id=pk)
		context['colegio']=colegio
		
		return context
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			colegio=establecimiento.objects.get(id=pk)# El mismo nombre que en tu URL
			form.instance= form.save(commit=False)
			#el nombre de cada uno de los if es el mismo de la base de datos
			# asi que no se pueden cambiar 
			try:
				agendado=Lista.objects.get(fecha=form.instance.fecha,horario=form.instance.horario,usuario=request.user)
				mensaje="Error no disponible"
				return redirect('dupla:Fallaconvivencia')
			except Lista.DoesNotExist:
				
				#Crear el evento en la bitacora
				# Registrar la sesión en un la lista de la bitacora
				
				form.instance.usuario = self.request.user
				form.instance.establecimiento=colegio
				form.instance.tipo_convivencia=2
				form.instance.evento=None
						
				form.instance.save()
				form.save_m2m()
				medida=Intervencion_convivencia_mediacion.objects.get(fecha=form.instance.fecha,horario=form.instance.horario,usuario=request.user)
				# Creacion en la agenda bitacora diaria
				Lista.objects.create(fecha=form.instance.fecha,horario=form.instance.horario,nombre='Convivencia escolar mediación',
							curso=15,tipo_letras=5,
							ambito=3,tipo_actividad=14,participantes=form.instance.participantes,
							establecimiento=colegio,mediacion=medida,desarrollo='Mediación escolar',numero=2,usuario=request.user)

				url = reverse(('dupla:listar_convivencia_escolar'), kwargs={ 'pk': colegio.id })
				return HttpResponseRedirect(url)

		else:
			
			return self.render_to_response(self.get_context_data(form=form))




# derivacion a otra institucion 
def RetornoDefinitivo(request,pk):
# Realizar un retorno de una ficha de derivacion a la dupla 
	
	dato = get_object_or_404(Estudiante, pk=pk)
	colegio=dato.curso.establecimiento
	mensaje=""
	
	try:
		ficha_derivacion_dupla=Ficha_derivacion_dupla.objects.get(Estudiante_id=dato,estado=1)
		ficha_id=ficha_derivacion_dupla.id
		if request.method=='POST':
			formulario = Derivacion_Ficha_derivacionForm(request.POST,request.FILES)
	 		if formulario.is_valid():
	 			instance = formulario.save(commit=False)
	 			if instance.docfile1 !=  None:
	 				instance.docfile1=request.FILES['docfile1']
	 			if instance.docfile2 !=  None:
	 				instance.docfile2=request.FILES['docfile2']
	 			if instance.docfile3 !=  None:
	 				instance.docfile3=request.FILES['docfile3']
				instance.ficha_derivacion_dupla=ficha_derivacion_dupla
				instance.fecha_retorno=datetime.datetime.now()
				instance.usuario=request.user
				instance.motivo=instance.get_motivo_termino()
				instance.save()
				
				infoarchivo2 = Ficha_derivacion_dupla.objects.get(id = ficha_id)
				infoarchivo2.pasada= 4 #porque pasa a otra institucion, si una ficha pasa a otra institucion 
				#automaticamente queda en la lista de los podibles egresados ya que se va del centro

				infoarchivo2.derivado = 2 # porque ya fue creada
				infoarchivo2.estado = 1 # porque aun sigue estando activa
				infoarchivo2.save()
				#inter=Intervenidos.objects.get(Estudiante=dato)
				#inter.activo=2
				#inter.save()
				
				
				url = reverse(('dupla:EntradasDerivadas'), kwargs={ 'pk': colegio.id })
				return HttpResponseRedirect(url)
		else:
			formulario = Derivacion_Ficha_derivacionForm()
	except Ficha_derivacion_dupla.DoesNotExist:
		ficha_derivacion_dupla=None
		ficha_id=None
		formulario = Derivacion_Ficha_derivacionForm()
		mensaje="Estudiante sin ficha de derivación - No es posible ingresar la derivación"
	
	

	context = {
		"formulario": formulario,
		"dato": dato,
		"ficha":ficha_derivacion_dupla,
		"mensaje":mensaje,

		 }
	return render(request, 'dupla/derivacion_retorno.html', context)


class EntradasDerivadas(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion_dupla
	template_name = 'dupla/entradas_fichas.html'
	
# Muestra a todas las derivaciones realizadas   
	
	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(EntradasDerivadas, self).get_context_data(**kwargs)
			colegio = self.kwargs.get('pk') # El mismo nombre que en tu URL
			escuela = establecimiento.objects.get(id=colegio)
			fichas  = Ficha_derivacion_dupla.objects.filter( Q(usuario=self.request.user)& Q(establecimiento= escuela) &Q(estado=1))
			
			context['fichas']=fichas
			context['escuela']=escuela
			return context


class ListarCasos(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion_dupla
	template_name = 'dupla/casos_fichas.html'
	paginate_by = 10
#muestra a todas las derivaciones realizadas   
	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ListarCasos, self).get_context_data(**kwargs)
			colegio = self.kwargs.get('pk') # El mismo nombre que en tu URL
			escuela=establecimiento.objects.get(id=colegio)
			fichas=Ficha_derivacion_dupla.objects.filter(Q(establecimiento= escuela) & Q(estado= 1))
			continuidad=Continuidad_dupla.objects.filter(ficha_derivacion_dupla__establecimiento= escuela) 
			context['fichas']=fichas
			context['escuela']=escuela
			context['continuidad']=continuidad

			
			return context			

class EntradasDerivadasIntitucion(ListView):
        '''listar todos los estudiantes derivados a otra institucion '''
	model = Ficha_derivacion_dupla
	template_name = 'dupla/entradas_fichas_derivadas.html'
	paginate_by = 20
#muestra a todas las derivaciones realizadas   
	
	  
	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(EntradasDerivadasIntitucion, self).get_context_data(**kwargs)
			colegio = self.kwargs.get('pk') # El mismo nombre que en tu URL
			escuela=establecimiento.objects.get(id=colegio)
			fichas=Ficha_derivacion_dupla.objects.filter(Q(pasada= 4) & Q(estado= 1) & Q(usuario=self.request.user)& Q(establecimiento= escuela))
			

			
			context['fichas']=fichas
			context['escuela']=escuela

			
			return context


class ListarEstablecimientos(ListView):
# en el acceso de las aciiones con los establecimientos 
# se establecen acciones exclusivas para el encargado de convivencia y se determina en base al tipo de
# cargo que tiene en el establecimiento y este es desde el numero 6 -7-8 -9	
	model = Cargo
	template_name = 'dupla/establecimiento_profesional.html'
	success_url = reverse_lazy('alumno:establecimiento_listar')	
	paginate_by = 100
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(ListarEstablecimientos, self).get_context_data(**kwargs)
		try:
			dup=Profesional.objects.get(usuario=self.request.user)
			context['profesional']=Cargo.objects.filter(profesional=dup)

		
			return context
		except Profesional.DoesNotExist:
			return context



class RBMidentificadorListView(ListView):
	model = Estudiante
	template_name = 'dupla/template_busqueda.html'
	context_object_name = 'dupla:busqueda'

	def get_context_data(self, **kwargs):
	    ctx = super(RBMidentificadorListView, self).get_context_data(**kwargs)
	    ctx['search_url'] = 'dupla:busqueda'
	    return ctx

	def get_queryset(self):
	    queryset = super(RBMidentificadorListView, self).get_queryset()
	    # En el admin_base.jade tenemos un input#search(name='q', type='search')
	    # usamos la sig linea para obtener la consulta solicitada.
	    pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
	    print pk
	    q = self.request.GET.getlist('q')
	    
	    terms = [term for term in q]
	    
	    estudiantado=Estudiante.objects.filter(curso__establecimiento__id=pk)
	    
	    if q:  # Si el campo no esta vacio, construimos el filtro
			queryset = reduce(operator.or_,
			                          (estudiantado.filter(Q(nombres__contains=t) \
			                                                        | Q(firs_name__contains=t))
			                            for t in terms
			                            )
			                          )
			return queryset




# Proceso de convivencia escolar 

# 1 Evento cualquiera tipo_evento =1
def BuscarConvivencia(request,pk):
#Registrar los bases para cada plan


	
	colegio=establecimiento.objects.get(id=pk)



	if request.method == 'POST':

		colegio=establecimiento.objects.get(id=pk)
		
		plan=Plan.objects.get(establecimiento=colegio)
		
		form = Base_PlanForm(request.POST)
		if form.is_valid():
			form.instance= form.save(commit=False)
			
			

			form.instance.plan=plan
			form.instance.usuario=request.user
			form.save()
			return redirect('plan:PlanListView', pk=pk)
				
	else:
		form = Base_PlanForm()
	
	form = Base_PlanForm()
	return render(
        request,
        'dupla/buscarconvivencia.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'form':form,
        		 'base':base,
        		 }
    )



 # Proceso de convivencia escolar 

# 1 Evento cualquiera tipo_evento =1
def BuscarConvivencia(request,pk):
#Registrar los bases para cada plan


	
	colegio=establecimiento.objects.get(id=pk)



	if request.method == 'POST':

		colegio=establecimiento.objects.get(id=pk)
		
		plan=Plan.objects.get(establecimiento=colegio)
		
		form = Base_PlanForm(request.POST)
		if form.is_valid():
			form.instance= form.save(commit=False)
			
			

			form.instance.plan=plan
			form.instance.usuario=request.user
			form.save()
			return redirect('plan:PlanListView', pk=pk)
				
	else:
		form = Base_PlanForm()
	
	form = Base_PlanForm()
	return render(
        request,
        '404.html',
        context={'mensaje':'Infromación no encontrada o no almacenadad ',
        		 'plan':plan,
        		 'form':form,
        		 'base':base,
        		 }
    )   


#Enviar mensaje de problemas cuando no se pueda ingresar una contongencia de 
#convivencia escolar
def Fallaconvivencia(request):
#Registrar los bases para cada plan

	mensaje="Error el proceso de ingreso, horario ocupado"
	return render(
        request,
        'plan/falla.html',
        context={'mensaje':mensaje,
        		
        		 }
    )

# Ingresar estudiantes a un evento de convivencia escolar 
# Ingresar apoderado 
#class Estudiante_convivencia_crear(CreateView):

#	model = Intervencion_convivencia_estudiante
#	form_class = Intervencion_convivencia_estudianteForm
#	template_name = 'dupla/Intervencion_convivencia_estudiante.html'
	
#	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
#		context = super(Estudiante_convuvencia_crear, self).get_context_data(**kwargs)
#		if 'form' not in context:
#			context['form'] = self.form_class(self.request.GET)
#		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
#		curso = self.kwargs.get('curso') # El mismo nombre que en tu URL
#		letra = self.kwargs.get('letra') # El mismo nombre que en tu URL
		
#		context['colegio']=Estudiante.objects.get(id=pk)
#		context['letra']=Estudiante.objects.get(id=pk)
#		context['curso']=Estudiante.objects.get(id=pk)
#		return context
	
	
#	def post(self, request, *args, **kwargs):
#		self.object = self.get_object
#		form = self.form_class(request.POST)
		
#		if form.is_valid():
#			solicitud = form.save(commit=False)
#			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
#			estudiante=Estudiante.objects.get(id=pk)
#			family=estudiante.Familia

#			solicitud.Familia=family
#			solicitud.Estudiante=estudiante
#			solicitud.save()
			
			
#			url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante.id })
#			return HttpResponseRedirect(url)	


#		else:
#			return self.render_to_response(self.get_context_data(form=form))

# Ejemplo de filtros con el forms
def mover(request, idAsignado,idcolegio):
	
	escuela=establecimiento.objects.get(id=idcolegio)
	print escuela
	asignado=Intervencion_convivencia.objects.get(id=idAsignado)
	assignment = Relacion_Intervencion_convivencia_estudiante.objects.filter(intervencion_convivencia=asignado)
	print assignment
	
		
	if request.method == 'POST':
		asignado=Intervencion_convivencia.objects.get(id=idAsignado)
		print asignado
		form = BuscarMoverForm(name=request.POST.get('assignment'),)
		if form.is_valid():
            # Actual Registro
			form.intervencion_convivencia= asignado
            
			form.save()
			
            
            # Nuevo Registro
            #fecha_hora_actual = datetime.now()
            #new_person = form.cleaned_data['person']
            #new_assignment = ResourcesAssignment(
            #    person_warehouse=new_person,
            #    resource_warehouse=assignment.resource_warehouse,
            #    date_assignment=fecha_hora_actual,
            #    assigned=True,
            #)
            #new_assignment.save()
            #form.save_m2m()
		return redirect("dupla:listar_convivencia_escolar", idcolegio)
	else:
		form = BuscarMoverForm(idcolegio)

    #template = get_template("dupla/mover.html") 
	context = {
         'form': form,
         'escuela': escuela,
         'evento': assignment,

         

	}
    #return HttpResponse(template.render(context, request))
	return render(request, 'dupla/mover.html', context)



#Proceso de busqueda de historia de cada uno de los estudiantes del establecimiento
def historia_dupla(request,pk):
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	try:
		ficha_id=Ficha_derivacion.objects.get(Estudiante=dato,estado=1)
	except Ficha_derivacion.DoesNotExist:
		ficha_id=None
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

	try:
		asiste=Registro.objects.filter(Estudiante=dato)
	except Registro.DoesNotExist:
		asiste=None
#Agregar todas aquellas acciones desarrolladas en el area de las duplas



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

# Ver la hostoria dentro de la dupla psicosocial
#----
#Proceso de busqueda de hoistiria de cada uno de los estudiantes del establecimiento
def historia_dupla_caso(request,pk):
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	try:
		# En la ficha_derivacion_dupla tambien tenemos el estado 1 para saber que es la ficha actual
		ficha_d=Ficha_derivacion_dupla.objects.get(Estudiante=dato,estado=1)
	except Ficha_derivacion_dupla.DoesNotExist:
		ficha_d=""
	
	# Obtener el 
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

	try:
		asiste=Registro.objects.filter(Estudiante=dato)
	except Registro.DoesNotExist:
		asiste=None
#Agregar todas aquellas acciones desarrolladas en el area de las duplas



	return render(
		request,
		'sesion/historia_dupla_caso.html',
		 context={
	     'estudiante':dato,
	     'ficha':ficha_id,
	     'sesiones':sesiones,
	     'modelito':modelito,
	     'retorno':retorno,
       	 'asiste':asiste,
          'intervenido':intervenido,
          
        		 
        		 
	})	

#-----
#Registrar sesiones de atencion de casos
def IntervencionCasosRegistar(request,pk):


	try:
		sesion=Intervencion_sesion.objects.get(pk=pk)
		estudiante_id=Estudiante.objects.get(pk=sesion.estudiante)
		
		plan=Intervencion_casos.objects.get(estudiante=estudiante_id)
		form = Intervencion_sesionIngresar(instance=sesion)
		try:
			sesiones=Intervencion_sesion.objects.filter(intervencion_casos=plan)
			
		except Intervencion_sesion.DoesNotExist:
			sesiones=""
	except Intervencion_casos.DoesNotExist:
		plan =""
		sesiones=""
		Intervencion_sesionIngresar=sesion		
	if request.method == 'POST':

		sesion=Intervencion_sesion.objects.get(pk=pk)
		estudiante_id=Estudiante.objects.get(pk=sesion.estudiante)
		
		
		plan=Intervencion_casos.objects.get(estudiante=estudiante_id)
		
		form = Intervencion_sesionForm(request.POST)
		if form.is_valid():
			
			try:
				agendado=Lista.objects.get(fecha=form.instance.fecha,horario=form.instance.horario,usuario=request.user)
				mensaje="Error no disponible"
				return redirect('dupla:IntervencionCasosDetailView', pk=pk)
			except Lista.DoesNotExist:
				
				form.instance= form.save(commit=False)
				form.instance.intervencion_casos=plan
				form.instance.usuario=request.user

				# Registrar la sesion en un la lista de la bitacora
				Lista.objects.create(fecha=form.instance.fecha,horario=form.instance.horario,nombre='Atención de caso',
							curso=estudiante_id.curso.numero,tipo_letras=estudiante_id.curso.letra,
							ambito=2,tipo_actividad=13,participantes=form.instance.participantes,
							establecimiento=estudiante_id.curso.establecimiento,desarrollo="",
							numero=1,usuario=form.instance.usuario)

				form.instance.save()
				form.save_m2m()
				return redirect('dupla:IntervencionCasosDetailView', pk=pk)
							
	else:
		form = Intervencion_sesionForm()	


    #book_id=get_object_or_404(Book, pk=pk)
	return render(
        request,
        'dupla/dupla_ver_intervencioncasos.html',
        context={'estudiante':estudiante_id,
        		 'plan':plan,
        		 'colegio':estudiante_id.curso.establecimiento,
        		 'form':form,
        		 'sesiones':sesiones,
        		 	}
    )


# Ingresar el estado de una intervencion planificada 


def IngresarIntervencion_sesion(request,pk,colegio):


	
	sesion = get_object_or_404(Intervencion_sesion, pk=pk)
	caso=sesion.intervencion_casos
	estudiante=caso.estudiante
	colegio = get_object_or_404(establecimiento, pk=colegio)
	mensaje=""

	
	if request.method=='POST':
		formulario = Intervencion_sesionIngresar(request.POST or None, instance=sesion)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			instance.fecha=sesion.fecha
 			instance.horario=sesion.horario	 
	 		instance.intervencion_casos=sesion.intervencion_casos	
	 			
			instance.usuario = request.user
			instance.save()
			formulario.save_m2m()
			mensaje="Sesión actualizada -  Estudiante asistió"

			#Actualizar la cita como asistida 
			agendado=Lista.objects.get(Q(fecha=instance.fecha) & Q(horario=instance.horario)& Q(usuario=request.user))
			agendado.numero=2

			x= datetime.date.today() 
			dia=x.day
			mes=x.month
			
			url = reverse(('bitacora:IntervencionCasosDetailView'), kwargs={ 'dia':dia, 'mes':mes })
			return HttpResponseRedirect(url)
				
			
				
		formulario = Intervencion_sesionIngresar(request.POST or None, instance=sesion)
	else:


				
		formulario = Intervencion_sesionIngresar(request.POST or None, instance=sesion)
	context = {
		"form": formulario,
		"mensaje":mensaje,
		"sesion":sesion,
		"colegio":colegio,
		 }
	return render(request, 'dupla/intervencion_sesion_form.html', context)



#Logicas para controlar las acciones de convivencia escolar del establecimiento 
# Crear la lista de estudiantes de un curso
def listar_curso_convivencia_escolar(request,pk,evento,letra=None,numero=None):
		
	colegio=establecimiento.objects.get(id=pk)
	estudiantes_colegio=Estudiante.objects.filter(curso__establecimiento=colegio)
	intervencion=Intervencion_convivencia.objects.get(id=evento)
	try:
		Curso=curso.objects.get(numero=numero,letra=letra,establecimiento=colegio)
		estudiantes_curso=Estudiante.objects.filter(curso=Curso)
		contexto = {'colegio':colegio,
					'Curso':Curso,
					'estudiantes_colegio':estudiantes_colegio,
					'estudiantes_curso':estudiantes_curso,
										

					 }
		return render(request, 'dupla/listar_curso_colegio.html', contexto)

	except curso.DoesNotExist:
			
		Curso=""
		contexto = {'colegio':colegio,
					'Curso':Curso,
					'estudiantes_colegio':estudiantes_colegio,
					
					
					

					

					 }
		return render(request, 'dupla/listar_curso_colegio.html', contexto)
# Seguimiento de las duplas
#Listado de estudiantes por establecimiento- dado que cada profesional tiene asignados un grupo de establecimientos
def listar_estudiantes_seguimiento(request,pk):
		
	estudiando=Escolaridad.objects.filter(establecimiento__id=pk)
	escuela=establecimiento.objects.get(id=pk)
	
	contexto = {'estudiando':estudiando,
				'escuela':escuela,
				 }
	return render(request, 'dupla/estudiante_seguimiento.html', contexto)

# Seguimiento de un estudiante
# Es igual al seguimiento de los estudiante que van al centro de bienestar pero 
# con los casos de dupla 

# -----------------------------------------------------------------------------
def CrearSeguimiento(request,pk):
	
    #group_required = 'puede_administrar_encuestas
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	escuela=dato.curso.establecimiento
	if request.method=='POST':
		form = SeguimientoForm(request.POST)
 		if form.is_valid():
			instance = form.save(commit=False)
			instance.Estudiante=dato
			instance.usuario = request.user
			instance.save()
			
			
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id })
			return HttpResponseRedirect(url)
			
		else:
			form = SeguimientoForm(request.POST)
	
	form = SeguimientoForm()
	
	context = {
		"form": form,
		"dato": dato,
		
		 }
	return render(request, 'dupla/seguimiento.html', context)

def CrearContinuidad(request,pk):
	
    #group_required = 'puede_administrar_encuestas
	mensaje=""
	dato = get_object_or_404(Estudiante, pk=pk)
	escuela=dato.curso.establecimiento
	ficha=Ficha_derivacion_dupla.objects.get(Estudiante=dato, estado=1)
	try:
		continuidad=Continuidad_dupla.objects.get(ficha_derivacion_dupla=ficha)
	except Continuidad_dupla.DoesNotExist:
		continuidad=None
	
	if request.method=='POST':
		form = ContinuidadForm(request.POST)
 		if form.is_valid():
			instance = form.save(commit=False)
			instance.ficha_derivacion_dupla=ficha
			instance.usuario = request.user
			instance.save()
			form.save_m2m()
			
			
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id })
			return HttpResponseRedirect(url)
			
		else:
			form = ContinuidadForm(request.POST)
	
	form = ContinuidadForm()
	
	context = {
		"form": form,
		"dato": dato,
		"continuidad": continuidad,
		
		 }
	return render(request, 'dupla/continuidad.html', context)	
	
class SeguimeintoDelete(DeleteView):

	model = Seguimiento
	template_name = 'dupla/seguimiento_eliminar.html'
	success_url = reverse_lazy('derivacion:inst_retorno')	

	def get_context_data(self, **kwargs):
		context=super(SeguimeintoDelete,self).get_context_data(**kwargs)
		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(SeguimeintoDelete, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		seguir=Seguimiento.objects.get(pk=pk)
		
		estudiante=seguir.Estudiante
		seguir.delete()
		
		
        # Retornamos el objeto
		url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': estudiante.curso.establecimiento.id })
		return HttpResponseRedirect(url)	

class SeguimientoUpdate1(UpdateView):

	model = Seguimiento
	template_name = 'dupla/seguimiento.html'
	form_class = SeguimientoForm
	success_url = reverse_lazy('derivacion:inst_retorno')	

	def get_context_data(self, **kwargs):
		context=super(SeguimientoUpdate,self).get_context_data(**kwargs)
		
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		seguir=Seguimiento.objects.get(pk=pk)
		estudiante= Estudiante.objects.get(id=seguir.Estudiante.id)
		context['dato'] = estudiante
		
		return context
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		seguir=Seguimiento.objects.get(pk=pk)
		estudiante= Estudiante.objects.get(id=seguir.Estudiante.id)

		escuela=estudiante.curso.establecimiento
		form = self.form_class(request.POST,request.FILES)
		if form.is_valid():
					
			form.instance= form.save(commit=False)
					#motivos=form.instance.Motivo_derivacion
					#for motivo in motivos:

					#	form.intance.Motivo_derivacion.add(motivo)
			
			form.instance.usuario = self.request.user
			form.instance.Estudiante=estudiante
			form.instance.save()
					
					
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id })
			return HttpResponseRedirect(url)

		else:
				
			return self.render_to_response(self.get_context_data(form=form))
		
			
# Forma de modificar un seguimiento de modo que no se repitan los reistros

class ListarSeguimiento(ListView):
	model = Seguimiento
	template_name = 'dupla/listar_seguimiento.html'
	paginate_by = 50

		
	def get_context_data(self, **kwargs):
		context=super(ListarSeguimiento,self).get_context_data(**kwargs)
		
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante= Estudiante.objects.get(id=pk)
		seguir=Seguimiento.objects.filter(Estudiante=estudiante)
		escuela=estudiante.curso.establecimiento
		context['dato'] = estudiante
		context['seguir'] = seguir
		context['escuela'] = escuela

		
		return context


# Ver todas las acciones que se realizaran en el plan de gestion 
# Listado de planes externos por establecimiento 
def PlanesMostrarEscuelaListView(request,pk):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico


    try:
        
        x= datetime.date.today() 
        annio=str(int(x.year))
        escuela=establecimiento.objects.get(id=pk)
        plan=Plan.objects.get(annio=annio,establecimiento=escuela)
        
        base=Base.objects.filter(plan=plan)
        indicador_base=Indicador_base.objects.filter(base__plan=plan)
        accion=Accion.objects.filter(base__plan=plan)
        plancillo=Plancillo.objects.filter(accion__base__plan=plan)
        actividades=Actividades.objects.filter(plancillo__accion__base__plan=plan).order_by('fecha')
        
        hecho_a=Hecho_Actividades.objects.filter(actividades__plancillo__accion__base__plan=plan).order_by('fecha')
        mensaje="Plan presente en la planificación de los establecimientos"
        
    except Actividades.DoesNotExist:
        plan =None
        base=None
        indicador_base=None
        accion=None
        plancillo=None
        actividades=None
        hecho_a=None
        mensaje="Plan externo sin planificación"
    
    return render(
        request,
        'dupla/ver_planes_total.html',
        context={
                 
                 'plan':plan,
                 'base':base,
                 'indicador_base':indicador_base,
				 'accion':accion,
                 'plancillo':plancillo,
                 'actividades':actividades,
                 'hecho_a':hecho_a,
				 'mensaje':mensaje,

                 }
    ) 

# Listar el plan de gestion pero solo convivencia escolar 
#--------------------------------------------------------------------------
# Listado de planes externos por establecimiento 
def PlanesMostrarEscuelaConvivenciaescolarListView(request,pk):



    try:
        
        x= datetime.date.today() 
        annio=str(int(x.year))
        escuela=establecimiento.objects.get(id=pk)
        plan=Plan.objects.get(annio=annio,establecimiento=escuela)
       
        base=Base.objects.filter(plan=plan,dimension__Indicador__nombre='Clima de convivencia escolar')
        indicador_base=Indicador_base.objects.filter(base__plan=plan)
        accion=Accion.objects.filter(base__plan=plan)
        plancillo=Plancillo.objects.filter(accion__base__plan=plan)
        actividades=Actividades.objects.filter(plancillo__accion__base__plan=plan).order_by('fecha')
        
        hecho_a=Hecho_Actividades.objects.filter(actividades__plancillo__accion__base__plan=plan).order_by('fecha')
        mensaje="Plan presente en la planificación de los establecimientos"
        
    except Actividades.DoesNotExist:
        plan =None
        base=None
        indicador_base=None
        accion=None
        plancillo=None
        actividades=None
        hecho_a=None
        mensaje="Plan externo sin planificación"
    
    return render(
        request,
        'dupla/ver_planes_total_convivencia.html',
        context={
                 
                 'plan':plan,
                 'base':base,
                 'indicador_base':indicador_base,
				 'accion':accion,
                 'plancillo':plancillo,
                 'actividades':actividades,
                 'hecho_a':hecho_a,
				 'mensaje':mensaje,

                 }
    ) 





# Ver un plan anterior de un año anterior
# Ver todas las acciones que se realizaran en el plan de gestion 
# Listado de planes externos por establecimiento 
def PlanesAntiguoMostrarEscuelaListView(request,pk,fecha):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico


    try:
        
       
        annio=fecha
        escuela=establecimiento.objects.get(id=pk)
        plan=Plan.objects.get(annio=annio,establecimiento=escuela)
        
        base=Base.objects.filter(plan=plan)
        indicador_base=Indicador_base.objects.filter(base__plan=plan)
        accion=Accion.objects.filter(base__plan=plan)
        plancillo=Plancillo.objects.filter(accion__base__plan=plan)
        actividades=Actividades.objects.filter(plancillo__accion__base__plan=plan).order_by('fecha')
        
        hecho_a=Hecho_Actividades.objects.filter(actividades__plancillo__accion__base__plan=plan).order_by('fecha')
        mensaje="Plan presente en la planificación de los establecimientos"
        
    except Actividades.DoesNotExist:
        plan =None
        base=None
        indicador_base=None
        accion=None
        plancillo=None
        actividades=None
        hecho_a=None
        mensaje="Plan externo sin planificación"
    
    return render(
        request,
        'dupla/ver_planes_total_anterior.html',
        context={
                 
                 'plan':plan,
                 'base':base,
                 'indicador_base':indicador_base,
				 'accion':accion,
                 'plancillo':plancillo,
                 'actividades':actividades,
                 'hecho_a':hecho_a,
				 'mensaje':mensaje,

                 }
    ) 


# Eliminar un plan de intervencion de un estudiante 


def mascota_plan_casos(request, pk):

	casos = get_object_or_404(Intervencion_casos, pk=pk)
	escuela=casos.estudiante.curso.establecimiento
	if request.method == 'POST':
		casos.delete()
		return redirect('alumno:Listar_estudiante_establecimiento', {'pk':escuela})
		    
	    
	template = 'dupla/casos_delete.html'
	    
	    
	context = {
	        "casos": casos,
	        "escuela":escuela,
	        

	        }
	return render(request, template, context)



class eliminar_caso_dupla(DeleteView):
	model = Estudiante
	template_name = 'dupla/casos_delete.html'

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(eliminar_caso_dupla, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		pk=self.kwargs.get('pk') # El mismo nombre que en tu URL
		print pk
		estudiante=Estudiante.objects.get(pk=pk)
		colegio=estudiante.curso.establecimiento
		try:
			caso=Intervencion_casos.objects.get(estudiante=estudiante)
		
		except Intervencion_casos.DoesNotExist:
		
			caso=""	
		# Valor nos indica si un estudiante tiene o no un plan de intervencion para su eliminacion
	
		context['caso']=caso
		context['estudiante']=estudiante
		context['colegio']=colegio
		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(eliminar_caso_dupla, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		try:
			estudiante=Estudiante.objects.get(pk=pk)
			caso=Intervencion_casos.objects.get(estudiante=estudiante)
			escuela=estudiante.curso.establecimiento
			
			caso.delete()
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id })
			return HttpResponseRedirect(url)
		except Intervencion_casos.DoesNotExist:
			return HttpResponseRedirect(url)

def SeguimientoUpdate(request,pk):
# modificar un indicador el cual depende de una base de un plan para un establceimiento
	
	seguimiento= get_object_or_404(Seguimiento, pk=pk)
	estudiante=seguimiento.Estudiante

	
	if request.method=='POST':
		formulario = SeguimientoForm(request.POST or None, instance=seguimiento)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.usuario = request.user
				
			instance.save()
		
				
				
			url = reverse(('dupla:ListarSeguimiento'), kwargs={ 'pk': estudiante.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = SeguimientoForm(request.POST or None, instance=seguimiento)
	else:


				
		formulario = SeguimientoForm(request.POST or None, instance=seguimiento)
	context = {
		"form": formulario,
		"seguimiento":seguimiento,
		"dato":estudiante,


		 }
	return render(request, 'dupla/seguimiento.html', context)


#Ficha de un estudiante desde la dupla
def FichaEstudianteDerivacionEgresoDetailView(request,pk):

	try:
		estudiante_id=Estudiante.objects.get(pk=pk)
		colegio=Escolaridad.objects.get(Estudiante__id=pk)
	except Estudiante.DoesNotExist:
		estudiante_id=None
	try:
		ficha_id=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk,estado=1)
	except Ficha_derivacion_dupla.DoesNotExist:
		ficha_id=None		
		


	return render(
        request,
        'alumno/ver_grupo.html',
        context={'estudiante':estudiante_id,
        		 'ficha':ficha_id,
        		 'colegio':colegio	}
    )

# Proceso de eliminacion de un estudiante del caso actul y pasa a la hostoria
class EntradasRetornoCasoDuplaList(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion_dupla
	template_name = 'dupla/entradas_fichas_termino.html'

#muestra a todas las derivaciones realizadas por el equipo PsicoSocial   
	
	
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(EntradasRetornoCasoDuplaList, self).get_context_data(**kwargs)
		pk=self.kwargs.get('pk') # El mismo nombre que en tu URL
		escuela=establecimiento.objects.get(id=pk)
		fichas=Ficha_derivacion_dupla.objects.filter((Q(pasada=4) | Q(pasada=7)) & Q(estado= 1) & Q(establecimiento=escuela))
	
		# Valor nos indica si un estudiante tiene o no un plan de intervencion para su eliminacion
	
		context['fichas']=fichas
		context['escuela']=escuela
		return context


# Modificar un evento de medicaion escolar
def MediciacionUpdate(request,pk):
# modificar un indicador el cual depende de una base de un plan para un establceimiento
	

	mediacion= Intervencion_convivencia_mediacion.objects.get(pk=pk)
	print mediacion
	colegio=mediacion.establecimiento
	
	yaagendado=Lista.objects.get(fecha=mediacion.fecha,horario=mediacion.horario,usuario=mediacion.usuario)
	print yaagendado
	
	
	if request.method=='POST':
		formulario = Intervencion_convivencia_mediacionForm(request.POST or None, instance=mediacion)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			#Busca que la nueva fecha no este ocupada
			try:
				agendado=Lista.objects.get(fecha=instance.fecha,horario=instance.horario,usuario=request.user)
				mensaje=" Horario ocupado no puede realizar la modificación "

				url = reverse(('dupla:listar_convivencia_escolar'), kwargs={ 'pk': colegio.id})
				return HttpResponseRedirect(url)
				
			except Lista.DoesNotExist:
				print mediacion
				print mediacion.fecha
				print instance.fecha
				agenda=Lista.objects.get(fecha=mediacion.fecha,horario=mediacion.horario,usuario=request.user)
				print agenda
				agenda.delete()
				# Registrar la sesión en un la lista de la bitacora
				Lista.objects.create(fecha=instance.fecha,horario=instance.horario,nombre='Convivencia escolar mediación',
							curso=15,tipo_letras=5,
							ambito=3,tipo_actividad=14,participantes=instance.participantes,
							establecimiento=colegio,desarrollo='Mediación escolar',numero=2,usuario=request.user)


			instance.usuario = request.user
				
			instance.save()
		
				
			url = reverse(('dupla:listar_convivencia_escolar'), kwargs={ 'pk': colegio.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Intervencion_convivencia_mediacionForm(request.POST or None, instance=mediacion)
	else:


				
		formulario = Intervencion_convivencia_mediacionForm(request.POST or None, instance=mediacion)
	context = {
		"form": formulario,
		"mediacion":mediacion,
		"colegio":colegio,


		 }
	return render(request, 'dupla/convivencia_mediacion_form.html', context)


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
class eliminar_mediacion(DeleteView):
    model = Intervencion_convivencia_mediacion
    template_name = 'dupla/eliminar_mediacion.html'

            
    def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
        context = super(eliminar_mediacion, self).get_context_data(**kwargs)
        
        #pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
        
        b=self.kwargs.get('pk') # El mismo nombre que en tu URL
        lista=Lista.objects.get(id=b)
        
        context['lista']=lista


        return context

    def post(self,request,*args,**kwargs):          
        self.object=self.get_object

        object = super(eliminar_mediacion, self).get_object()
        pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
        
        lista=Lista.objects.get(pk=pk)
        
        
        object.delete()
        
        # Retornamos el objeto
        url = reverse(('bitacora:fechas'), kwargs={ 'dia': lista.fecha.day,'mes':lista.fecha.month})
        return HttpResponseRedirect(url)


# Ver la ficha de derivacion de un estudiante
# Ver ficha de derivacion y/o de egreso 
#Ficha de un estudiante desde la dupla
def FichaEstudianteegresoDetailView(request,pk):

	estudiante_id=Estudiante.objects.get(pk=pk)
	colegio=Escolaridad.objects.get(Estudiante__id=pk)

	try:
		ficha_id=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk,estado=1)
		try:
			deriva=Derivacion_Ficha_derivacion_dupla.objects.get(ficha_derivacion_dupla=ficha_id)
		except Derivacion_Ficha_derivacion_dupla.DoesNotExist:
			deriva=None
			
	except Ficha_derivacion.DoesNotExist:
		ficha_id=None	
		deriva=None	
			

    #book_id=get_object_or_404(Book, pk=pk)
	return render(
        request,
        'dupla/ver_derivacion_dupla.html',
        context={'estudiante':estudiante_id,
        		 'ficha':ficha_id,
        		 'deriva':deriva,
        		 
        		 'colegio':colegio	}
    )
