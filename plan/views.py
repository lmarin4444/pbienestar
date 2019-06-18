# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from plan.models import Plan,Base,Indicador_base,Accion,Plancillo,Actividades,Hecho_Actividades,Planes_mineduc
from alumno.models import curso
from bitacora.models import Lista
from django.http import HttpResponseRedirect
from plan.forms import PlanForm,Base_PlanForm,Indicador_baseForm,Accion_baseForm,Base_PlancilloForm,Base_ActividadesForm, \
	Indicador_baseLogroForm,Base_ActividadesPlanificacion,Base_ActividadesPlan,Hecho_ActividadesForm,Justificar_ActividadesForm, \
	Reagendar_ActividadesForm,PlanFormMineduc
from alumno.models import establecimiento
import datetime
from django.db.models import Q

#Para el envio de mensaje
from django.contrib import messages

# Create your views here.
class ingresar_plan(CreateView):
	model = Plan	
	form_class = PlanForm
	template_name = 'plan/plan_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ingresar_plan, self).get_context_data(**kwargs)
			colegio = self.kwargs.get('pk') # El mismo nombre que en tu URL
			escuela=establecimiento.objects.get(id=colegio)
			try:
				x= datetime.date.today() 
				annio=str(int(x.year))
				plan=Plan.objects.get(establecimiento=escuela,annio=annio)
				context['escuela']=escuela
				context['plan']=plan
				context['mensaje']='--Ya cuenta con un plan '
				return context
			except Plan.DoesNotExist:
				context['escuela']=escuela
				context['mensaje']=''
				return context
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST,request.FILES)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			
		if request.method == 'POST':
			form = PlanForm(request.POST)
		        #codigo
			if form.is_valid():
				pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
				escuela=establecimiento.objects.get(id=pk)
				try:
					x= datetime.date.today() 
					annio=str(int(x.year))
					plan=Plan.objects.get(establecimiento=escuela,annio=annio)
					return self.render_to_response(self.get_context_data(form=form))
				except Plan .DoesNotExist:
					instance = form.save(commit=False)
					

					instance.establecimiento=establecimiento.objects.get(id=pk)
					
					instance.usuario=self.request.user
					x= datetime.date.today() 
					instance.annio=str(int(x.year))

					instance.save()

					url = reverse(('plan:PlanListView'), kwargs={ 'pk': pk })
					return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(form=form))

# Ingresar plan externo del mineduc
# Create your views here.
class ingresar_plan_mineduc(CreateView):
	model = Planes_mineduc	
	form_class = PlanFormMineduc
	template_name = 'plan/plan_mineduc_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ingresar_plan_mineduc, self).get_context_data(**kwargs)
			colegio = self.kwargs.get('pk') # El mismo nombre que en tu URL
			escuela=establecimiento.objects.get(id=colegio)
			
			context['escuela']=escuela
			context['mensaje']=''
			return context
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST,request.FILES)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			
		if request.method == 'POST':
			form = PlanFormMineduc(request.POST)
		        #codigo
			if form.is_valid():
				pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
				escuela=establecimiento.objects.get(id=pk)
				
				instance = form.save(commit=False)
					

				instance.establecimiento=establecimiento.objects.get(id=pk)
					
				instance.usuario=self.request.user
				

				instance.save()

				url = reverse(('plan:PlanListViewMineduc'), kwargs={ 'pk': pk })
				return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(form=form))

# Listado de planes mineduc de un establecimiento
def PlanMineducListView(request,pk):
#Registrar los bases para cada plan
	try:
		colegio=establecimiento.objects.get(id=pk)
		x= datetime.date.today() 
		annio=str(int(x.year))
		plan=Planes_mineduc.objects.get(establecimiento=colegio,annio=annio)
		
		
	except Planes_mineduc.DoesNotExist:
		plan =None

	if request.method == 'POST':

		colegio=establecimiento.objects.get(id=pk)
		x= datetime.date.today() 
		annio=str(int(x.year))
		plan=Planes_mineduc.objects.get(establecimiento=colegio,annio=annio)
		
		form = PlanFormMineduc(request.POST)
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
        'plan/plan_ingresar_planificacion.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'form':form,
        		 'base':base,
        		 }
    )

# Listado de todos los planes de gestion de un establecimiento
def PlanListView(request,pk):
#Registrar los bases para cada plan

	
	try:
		colegio=establecimiento.objects.get(id=pk)
		x= datetime.date.today() 
		annio=str(int(x.year))
		plan=Plan.objects.get(establecimiento=colegio,annio=annio)
		base=Base.objects.filter(plan=plan)
		
	except Plan.DoesNotExist:
		plan =None
		base=None

	if request.method == 'POST':

		colegio=establecimiento.objects.get(id=pk)
		x= datetime.date.today() 
		annio=str(int(x.year))
		plan=Plan.objects.get(establecimiento=colegio,annio=annio)
		
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
        'plan/plan_ingresar_planificacion.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'form':form,
        		 'base':base,
        		 }
    )




class ingresar_indicador(CreateView):
	model = Indicador_base	
	form_class = Indicador_baseForm
	template_name = 'plan/plan_indicador_form.html'
	success_url = reverse_lazy('plan:PlanListView')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			try:
				
			
				context = super(ingresar_indicador, self).get_context_data(**kwargs)
				base = self.kwargs.get('pk') # El mismo nombre que en tu URL

				accion_base=Base.objects.get(id=base)
				
				indicadores=Indicador_base.objects.filter(base=accion_base).count()
				
				indicadores_lista=Indicador_base.objects.filter(base=accion_base)
				cantidad_indicadores_base=accion_base.cantidad_indicadores

				
				if (cantidad_indicadores_base > indicadores):
					mensaje="Debe ingresar mas indicadores"

				if (cantidad_indicadores_base == indicadores):
					mensaje="Cantidad de indicadores igual a la cantidad declarada "

				if (cantidad_indicadores_base < indicadores):
					mensaje="Cantidad de indicadores ingresados supera la cantidad declarada "	
			
				context['indicadores']=indicadores
				context['cantidad_indicadores_base']=cantidad_indicadores_base
				context['indicadores_lista']=indicadores_lista

				context['accion_base']=accion_base
				context['mensaje']=mensaje

				return context
			
			except Base.DoesNotExist:
				context['indicadores_lista']=''
				context['accion_base']=''
				context['mensaje']=''
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		
		
			
		if request.method == 'POST':
			form = Indicador_baseForm(request.POST)
		        #codigo
			if form.is_valid():
				pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
				colegio= self.kwargs.get('colegio')
				escuela=establecimiento.objects.get(id=colegio)
				accion_base=Base.objects.get(id=pk)

				
				
				form = form.save(commit=False)
				form .usuario=request.user	
				form.base=accion_base
				form.nivel_logro=0
				form.justificacion_logro='Sin justificación,solo creado'

				
					
					
					
				form.save()
				
			
				
				url = reverse(('plan:IndicadorListView'), kwargs={'pk':accion_base.id})
				return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(form=form))


def IndicadorListView(request,pk):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico

	try:
		
		base=Base.objects.get(pk=pk)
		indicadores=Indicador_base.objects.filter(base=base)
	except Indicador_base .DoesNotExist:
		indicadores =None

	return render(
        request,
        'plan/base_ver_indicadores.html',
        context={'base':base,
        		 'indicadores':indicadores,
        		
        		 }
    )

# Modificar indicadores 





class ingresar_acciones(CreateView):
	model = Accion
	form_class = Accion_baseForm
	template_name = 'plan/plan_accion_form.html'
	success_url = reverse_lazy('plan:PlanListView')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			
			base = self.kwargs.get('pk') # base en la cual se esta trabajando
			colegio=self.kwargs.get('colegio') # colegio en el cual estar trabajando
			try:
				
			
				context = super(ingresar_acciones, self).get_context_data(**kwargs)
				

				accion_base=Base.objects.get(id=base)
				plan=accion_base.plan
				indicadores=Accion.objects.filter(base=accion_base).count()
				
				indicadores_lista=Accion.objects.filter(base=accion_base)
				cantidad_indicadores_base=accion_base.cantidad_indicadores

				
				if (cantidad_indicadores_base > indicadores):
					mensaje="Debe ingresar mas acciones"

				if (cantidad_indicadores_base == indicadores):
					mensaje="Cantidad de acciones igual a la cantidad declarada "

				if (cantidad_indicadores_base < indicadores):
					mensaje="Cantidad de acciones ingresadas supera la cantidad de acciones declaradas "	
			
				context['indicadores']=indicadores
				context['cantidad_indicadores_base']=cantidad_indicadores_base
				context['indicadores_lista']=indicadores_lista

				context['accion_base']=accion_base
				context['plan']=plan
				context['mensaje']=mensaje
				context['colegio']=colegio
				context['base']=accion_base
				

				return context
			
			except Accion.DoesNotExist:
				context['indicadores_lista']=''
				context['accion_base']=accion_base
				context['base']=accion_base
				context['mensaje']=''
				context['colegio']=colegio
				context['form'] = self.form_class(fecha=date())

		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
				
		if request.method == 'POST':
			form = self.form_class(request.POST,request.FILES)
		        #codigo
			if form.is_valid():
				pk = self.kwargs.get('pk') # Envio indicador de la base
				colegio= self.kwargs.get('colegio')# Envio indicador del colegio
				escuela=establecimiento.objects.get(id=colegio)
				accion_base=Base.objects.get(id=pk)
				form.instance = form.save(commit=False)
				form.instance .usuario=request.user	
				form.instance.base=accion_base
					
				form.instance.save()
				form.save_m2m()
			
				url = reverse(('plan:AccionesListView'), kwargs={'pk':accion_base.id})
				return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(form=form))


def AccionesListView(request,pk):
# 

	try:
		base=Base.objects.get(id=pk)
		indicadores=Accion.objects.filter(base=base)
	except Accion.DoesNotExist:
		indicadores =''

	return render(
        request,
        'plan/base_ver_accion.html',
        context={'base':base,
        		 'indicadores':indicadores,
        		
        		 }
    )


class ver_plancillo(CreateView):
	model = Plancillo	
	form_class = Base_PlancilloForm
	template_name = 'plan/accion_actividades_ver.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ver_plancillo, self).get_context_data(**kwargs)
			accion = self.kwargs.get('pk') # El mismo nombre que en tu URL
			base= self.kwargs.get('base') # El mismo nombre que en tu URL
			base_activa=Base.objects.get(id=base)
			accion_activa=Accion.objects.get(id=accion)
			try:
				plan=Plancillo.objects.filter(accion=accion_activa)
				context['accion']=accion_activa
				context['plan']=plan

				context['mensaje']='Listado de planes / Actividades '
				context['base']=base_activa
				return context
			except Plancillo.DoesNotExist:
				context['accion']=accion_activa
				context['mensaje']='Listado de planes / Sin Cronogramas '
				context['base']=base_activa
				return context


class ingresar_plancillo(CreateView):
	model = Plancillo	
	form_class = Base_PlancilloForm
	template_name = 'plan/plancillo_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ingresar_plancillo, self).get_context_data(**kwargs)
			accion = self.kwargs.get('pk') # El mismo nombre que en tu URL
			base= self.kwargs.get('base') # El mismo nombre que en tu URL
			base_activa=Base.objects.get(id=base)
			accion_activa=Accion.objects.get(id=accion)
			try:
				plan=Plancillo.objects.filter(accion=accion_activa)
				context['accion']=accion_activa
				context['plan']=plan

				context['mensaje']='Listado de planes / Actividades '
				context['base']=base_activa
				return context
			except Plancillo.DoesNotExist:
				context['accion']=accion_activa
				context['mensaje']='Listado de planes / Sin Cronogramas '
				context['base']=base_activa
				return context
					
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST,request.FILES)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		base=self.kwargs.get('base') # El mismo nombre que en tu URL	
		base_activa=Base.objects.get(id=base)
		if request.method == 'POST':
			form = Base_PlancilloForm(request.POST)
		        #codigo
			if form.is_valid():
		
				accion_activa=Accion.objects.get(id=pk)

				instance = form.save(commit=False)
				instance.accion=accion_activa
				numero=instance.numero
				print numero
				letra=instance.letra
				print letra
				establecimiento=base_activa.plan.establecimiento
				if (numero >0 or numero<=14) and (letra>0 or letra <=4): 
					try:
						cursando=curso.objects.get(numero=numero,letra=letra,establecimiento=establecimiento)
					except curso.DoesNotExist:
						cursando=""
				else:
					cursando=""
					instance.numero=15
					instance.letra=5
				instance.curso=cursando
				instance.usuario=self.request.user
				instance.save()

				url = reverse(('plan:ver_plancillo'), kwargs={ 'pk': accion_activa.id ,'base':base_activa.id })
				return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(form=form))


def ActividadesListView(request,pk):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico


	try:
		colegio=establecimiento.objects.get(id=pk)
		plan=Plan.objects.get(establecimiento=colegio)
		base=Base.objects.filter(plan=plan)
		
	except Plan.DoesNotExist:
		plan =None

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
        'plan/plan_ver_ficha.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'form':form,
        		 'base':base,
        		 }
    )

def PlancilloListView(request,pk):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico


	try:
		accion_base=Accion.objects.get(id=pk)
		base=Base.objects.get(id=base)
		plancillo=objects.get(accion=accion_base)
		
	except Plancillo.DoesNotExist:
		plan =None

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
        'plan/plan_ver_ficha.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'form':form,
        		 'base':base,
        		 }
    )


class ingresar_Actividad(CreateView):
	model = Actividades	
	form_class = Base_ActividadesForm
	template_name = 'plan/Actividades_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')
	success_message = "Fecha y hora ocupada por el usuario o Planificación fuera de plazo"
	
	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ingresar_Actividad, self).get_context_data(**kwargs)
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			actividad=Actividades.objects.get(id=pk)
			plancillo=actividad.plancillo
			accion=plancillo.accion
			base=accion.base
			plan=base.plan
			form = Base_ActividadesForm(instance=actividad)
			
			context['plancito']=plancillo
			context['accion']=accion
			context['base']=base
			context['plan']=plan
			context['actividad']=actividad
			context['form']=form

			context['mensaje']=""
			
			return context
			
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		actividad_activa=Actividades.objects.get(pk=pk)	
		if request.method == 'POST':
			form = Base_ActividadesForm(request.POST or None, instance=actividad_activa)
		        #codigo
			if form.is_valid():
				
				#Verificar si el plan existe 
				
				plancito=actividad_activa.plancillo
				accion=plancito.accion
				base=accion.base
				plan=base.plan	
				
				form.instance = form.save(commit=False)
				#Establecer el mes en base a la fecha dada
				h=datetime.date.today() #Mes actual
				mes_actual=h.month-1
		
				
				x= form.instance.fecha
				mes=x.month -1


				
				if actividad_activa.mes >= mes_actual:
					form.instance.mes=mes# Mes selecionado en la entrada
					hoy=datetime.date.today() # Fecha de hoy para saber que esta fuera de plazo en la planificacion
					usuario=self.request.user # Verificar usuario activo

					#verificar si la actividad ya existe 
					
					try:
						agendado=Lista.objects.get(horario=form.instance.horario,fecha=form.instance.fecha,usuario=usuario)
						#agendado=Lista.objects.get(Q(horario=instance.horario) & Q(fecha=instance.fecha) & Q(usuario=usuario) & Q(fecha__gte=hoy))            
						
						messages.success(self.request, self.success_message)
						url = reverse(('plan:ingresar_Actividad'), kwargs={ 'pk': pk })

						return HttpResponseRedirect(url)
					except Lista.DoesNotExist:
						
						
						form.instance.usuario=self.request.user
						form.instance.plancillo=plancito
						form.instance.estado=0# ACCION SOLO PLANIFICADA
						form.instance.save()
						form.save_m2m()
						#Crear una entrada en la bitacora de accion

						Lista.objects.create(fecha=form.instance.fecha,horario=form.instance.horario,nombre=form.instance.nombre,
							curso=plancito.numero,tipo_letras=plancito.letra,
							ambito=1,tipo_actividad=12,participantes=form.instance.participantes,
							establecimiento=plan.establecimiento,desarrollo="",
							planes_externos=form.instance.planes_externos,numero=1,actividad=form.instance,usuario=form.instance.usuario)

						url = reverse(('plan:ver_actividades'), kwargs={ 'pk': plancito.id })
						return HttpResponseRedirect(url)
					
				else:
					
					messages.success(self.request, self.success_message)
					url = reverse(('plan:ingresar_Actividad'), kwargs={ 'pk': pk })

					return HttpResponseRedirect(url)						
			else:
				form = Base_ActividadesForm(request.POST or None, instance=actividad_activa)
				return self.render_to_response(self.get_context_data(Base_ActividadesForm=form))
	
	def get_success_message(self, cleaned_data):
	            print (cleaned_data)
	            return "Error "

class ingresar_Actividad_plan(CreateView):
	model = Actividades	

	form_class = Base_ActividadesPlan
	template_name = 'plan/Actividades_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ingresar_Actividad_plan, self).get_context_data(**kwargs)
			plancito = self.kwargs.get('pk') # El mismo nombre que en tu URL
			
			plancillo=Plancillo.objects.get(id=plancito)
			
			accion=plancillo.accion
			
			base=accion.base
			
			plan=base.plan
			
			context['plancito']=plancillo
			context['accion']=accion
			context['base']=base
			context['plan']=plan
			context['form']=Base_ActividadesPlan
			context['escuela']=plan.establecimiento

			context['mensaje']=""
			
			return context
			
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		plancito = self.kwargs.get('pk') # El mismo nombre que en tu URL
		plancillo=Plancillo.objects.get(id=plancito)
		accion=plancillo.accion
		base=accion.base
		plan=base.plan
			
		if request.method == 'POST':
			form = Base_ActividadesPlan(request.POST)
		        #codigo
			if form.is_valid():
								
				instance = form.save(commit=False)
				instance.usuario=self.request.user

				instance.plancillo=plancillo


				instance.save()
				form.save_m2m()
				
				url = reverse(('plan:ver_actividades'), kwargs={ 'pk': pk })
				return HttpResponseRedirect(url)
			else:
				form = Base_ActividadesPlan(request.POST)
				return render(request, 'plan/Actividades_form.html', {'form': form,
					'plan': plan,
					'accion': accion,
					'base': base,
					'plancito': plancillo,

					})






class ver_actividades(ListView):
	model = Actividades	
	
	template_name = 'plan/actividades_ver.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ver_actividades, self).get_context_data(**kwargs)
			plan = self.kwargs.get('pk') # El mismo nombre que en tu URL
			plancito=Plancillo.objects.get(id=plan)
			accion=plancito.accion
			
			try:
				actividades=Actividades.objects.filter(plancillo=plancito)
				context['plan']=plancito
				context['actividades']=actividades
				context['accion']=accion
				context['base']=accion.base
				

				
				return context
			except Actividades.DoesNotExist:
				context['plan']=plancito
				context['accion']=accion
				context['base']=accion.base

				context['actividades']=None
				return context

class ver_bases(ListView):
	model = Base	
	
	template_name = 'plan/bases_ver.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ver_bases, self).get_context_data(**kwargs)
			base = self.kwargs.get('pk') # El mismo nombre que en tu URL
			
			base_activa=Base.objects.get(id=base)
			
			try:
				accion_activa=Accion.objects.filter(base=base_activa)
				indicador_base=Indicador_base.objects.filter(base=base_activa)
				plancillo_activo=Plancillo.objects.all()
				
				actividades_activas=Actividades.objects.all()
				context['accion']=accion_activa
				context['indicadores']=indicador_base
				context['plancillo']=plancillo_activo
				context['actividades']=actividades_activas
				
			except Accion.DoesNotExist:
				context['accion']=""
				context['indicadores']=""
				context['plancillo']=""
				context['actividades']=""

			try:
				indicador_activo=Indicador_base.objects.filter(base=base_activa)
				context['indicador_base']=indicador_activo
			
			except Indicador_base.DoesNotExist:
				context['indicador_base']=""	
			context['base']=base_activa	
			return context
def modificar_plan(request,pk):
# Modificar un plan  
	
	plan = get_object_or_404(Plan, pk=pk)
	
	escuela=plan.establecimiento

	
	if request.method=='POST':
		formulario = PlanForm(request.POST or None, instance=plan)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.establecimiento=plan.establecimiento
			instance.usuario = request.user
				
			instance.save()
				
				
			url = reverse(('plan:PlanListView'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = PlanForm(request.POST or None, instance=plan)
	else:


				
		form = PlanForm(request.POST or None, instance=plan)
	context = {
		"form": form,
		
		"plan":plan,
		"escuela":escuela,
		 }
	return render(request, 'plan/plan_accion_form.html', context)	




def modificar_base(request,pk):
# Realizar un retorno de una ficha de derivacion a la dupla 
	
	dato = get_object_or_404(Base, pk=pk)
	plan=dato.plan
	escuela=plan.establecimiento
 
	
	if request.method=='POST':
		formulario = Base_PlanForm(request.POST or None, instance=dato)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.plan=plan
			instance.usuario = request.user
			instance.save()
			url = reverse(('plan:PlanListView'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Base_PlanForm(request.POST or None, instance=dato)
	else:


				
		form = Base_PlanForm(request.POST or None, instance=dato)
	context = {
		"form": form,

		"plan":plan,
		"base":dato,
		"escuela":escuela,
		"colegio":escuela.id,

		 }
	return render(request, 'plan/plan_accion_form.html', context)	

class eliminar_base(DeleteView):
	model = Base
	template_name = 'plan/eliminar_base.html'

	        

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(eliminar_base, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		b=self.kwargs.get('pk') # El mismo nombre que en tu URL
		base=Base.objects.get(id=b)
		plan=base.plan
		context['base']=base
		context['plan']=plan
		context['escuela']=plan.establecimiento

		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(eliminar_base, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		base=Base.objects.get(pk=pk)
		escuela=base.plan.establecimiento
		print escuela
		object.delete()
		
        # Retornamos el objeto
		url = reverse(('plan:PlanListView'), kwargs={ 'pk': escuela.id})
		return HttpResponseRedirect(url)
		
def modificar_accion(request,pk):
# Realizar un retorno de una ficha de derivacion a la dupla 
	
	accion= get_object_or_404(Accion, pk=pk)
	base=accion.base 
	plan=base.plan

	escuela=plan.establecimiento
	colegio=escuela.id
	if request.method=='POST':
		formulario = Accion_baseForm(request.POST or None, instance=accion)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			base=instance.base
			instance.base=base
			instance.usuario = request.user
			instance.save()
			formulario.save_m2m()	
			url = reverse(('plan:AccionesListView'), kwargs={ 'pk': base.id})
			return HttpResponseRedirect(url)
		formulario = Accion_baseForm(request.POST or None, instance=accion)
	else:		
		formulario = Accion_baseForm(request.POST or None, instance=accion)
	context = {
		"form": formulario,
		"plan":plan,
		"escuela":escuela,
		"base":base,
		"accion":accion,


		"colegio":colegio,

		 }
	return render(request, 'plan/plan_accion_form.html', context)	


class eliminar_accion(DeleteView):
	model = Accion
	template_name = 'plan/eliminar_accion.html'

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(eliminar_accion, self).get_context_data(**kwargs)
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		a=self.kwargs.get('pk') # El mismo nombre que en tu URL
		accion=Accion.objects.get(id=a)
		base=accion.base
		plan=base.plan
		context['accion']=accion
		context['base']=base
		context['plan']=plan
		context['escuela']=plan.establecimiento
		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(eliminar_accion, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		accion=Accion.objects.get(pk=pk)
		base=accion.base
		
		object.delete()
		
        # Retornamos el objeto
		url = reverse(('plan:AccionesListView'), kwargs={ 'pk': base.id})
		return HttpResponseRedirect(url)

def modificar_indicador(request,pk):
# modificar un indicador el cual depende de una base de un plan para un establceimiento
	
	indicador= get_object_or_404(Indicador_base, pk=pk)
	base=indicador.base 
	
	plan=base.plan
	escuela=plan.establecimiento

	
	if request.method=='POST':
		formulario = Indicador_baseLogroForm(request.POST or None, instance=indicador)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			base=instance.base
			instance.base=base
			instance.usuario = request.user
				
			instance.save()
		
			formulario.save_m2m()	
				
			url = reverse(('plan:IndicadorListView'), kwargs={ 'pk': base.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Indicador_baseLogroForm(request.POST or None, instance=indicador)
	else:


				
		formulario = Indicador_baseLogroForm(request.POST or None, instance=indicador)
	context = {
		"form": formulario,
		"indicador":indicador,
		"accion_base":base,

		"plan":plan,
		"escuela":escuela,
		 }
	return render(request, 'plan/plan_indicador_form.html', context)	


class eliminar_indicador(DeleteView):
	model = Indicador_base
	template_name = 'plan/eliminar_indicador.html'

	        

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(eliminar_indicador, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		a=self.kwargs.get('pk') # El mismo nombre que en tu URL
		indicador=Indicador_base.objects.get(id=a)
		base=indicador.base
		plan=base.plan
		context['indicador']=indicador
		context['base']=base
		context['plan']=plan
		context['escuela']=plan.establecimiento

		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(eliminar_indicador, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		indicador=Indicador_base.objects.get(pk=pk)
		base=indicador.base
		
		object.delete()
		
        # Retornamos el objeto
		url = reverse(('plan:IndicadorListView'), kwargs={ 'pk': base.id})
		return HttpResponseRedirect(url)	

def modificar_plancillo(request,pk):
# modificar un indicador el cual depende de una base de un plan para un establceimiento
	
	plancillo= get_object_or_404(Plancillo, pk=pk)
	accion=plancillo.accion
	base=accion.base
	plan=base.plan 
	escuela=plan.establecimiento

	
	if request.method=='POST':
		formulario = Base_PlancilloForm(request.POST or None, instance=plancillo)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			accion=instance.accion
			base=accion.base
			instance.accion=accion
			instance.usuario = request.user
				
			instance.save()
		
				
				
			url = reverse(('plan:ver_plancillo'), kwargs={ 'pk': accion.id,'base':base.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Base_PlancilloForm(request.POST or None, instance=plancillo)
	else:


				
		formulario = Base_PlancilloForm(request.POST or None, instance=plancillo)
	context = {
		"form": formulario,
		"indicador":accion,
		"accion_base":base,

		"plan":plan,
		"escuela":escuela,
		 }
	return render(request, 'plan/plancillo_form.html', context)	


class eliminar_plancillo(DeleteView):
	model = Plancillo
	template_name = 'plan/eliminar_plancillo.html'

	        

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(eliminar_plancillo, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		p=self.kwargs.get('pk') # El mismo nombre que en tu URL
		plancito=Plancillo.objects.get(id=p)
		accion=plancito.accion
		base=accion.base
		plan=base.plan
		context['plancito']=plancito
		context['accion']=accion
		context['base']=base
		context['plan']=plan
		

		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(eliminar_plancillo, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		plancito=Plancillo.objects.get(pk=pk)
		accion=plancito.accion
		base=accion.base
		
		object.delete()
		
        # Retornamos el objeto
		url = reverse(('plan:ver_plancillo'), kwargs={ 'pk': accion.id,'base':base.id})
		return HttpResponseRedirect(url)

def ActividadesListView(request,pk):
#Registrar los bases para cada plan


	try:
		plan=Plan.objects.get(id=pk)
		base=Base.objects.filter(plan=plan)
		accion=Accion.objects.all()
		plancillo=Plancillo.objects.all()
		actividades=Actividades.objects.all()
		cantidad_bases=base.count()
	except Plan.DoesNotExist:
		plan=""
		base=""
		accion=""
		plancillo=""
		actividades=""
       
	
	return render(
        request,
        'plan/plan_ver_actividades.html',
        context={'plan':plan,
        		 'base':base,
        		 'accion':accion,
        		 'plancillo':plancillo,
        		 'actividades':actividades,
        		 'cantidad_bases':cantidad_bases,
        		 }
    )



#ver los planes por area 1: Dupla PsicoSocial
def ActividadesDuplaListView(request,pk):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico


	try:
		colegio=establecimiento.objects.get(id=pk)
		x= datetime.date.today() 
		annio=str(int(x.year))
		plan=Plan.objects.get(establecimiento=colegio,annio=annio)
		base=Base.objects.filter(plan=plan)
		accion=Accion.objects.all()
		plancillo=Plancillo.objects.all()
		actividades=Actividades.objects.filter(Q(tipo=0)|Q(tipo=1)|Q(tipo=3)|Q(tipo=4))
		
	except Plan.DoesNotExist:
		plan =None

	
	return render(
        request,
        'plan/plan_ver_ficha_dupla.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'base':base,
        		 'accion':accion,
        		 'plancillo':plancillo,
        		 'actividades':actividades,
        		 }
    )

#ver los planes por area 2: Encargado de convivencia
def ActividadesConvivenciaListView(request,pk):
#Registrar los logros de cada uno de las dimensiones de logros para cada diagnostico


	try:
		colegio=establecimiento.objects.get(id=pk)
		x= datetime.date.today() 
		annio=str(int(x.year))
		plan=Plan.objects.get(establecimiento=colegio,annio=annio)
		base=Base.objects.filter(plan=plan)
		accion=Accion.objects.all()
		plancillo=Plancillo.objects.all()
		actividades=Actividades.objects.filter(Q(tipo=0)|Q(tipo=2)|Q(tipo=5)|Q(tipo=6)|Q(tipo=7)|Q(tipo=8) )
		
	except Plan.DoesNotExist:
		plan =None

	
	return render(
        request,
        'plan/plan_ver_ficha_convivencia.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'base':base,
        		 'accion':accion,
        		 'plancillo':plancillo,
        		 'actividades':actividades,
        		 }
    )

#Para planificar las actividades de las duplas  dentro de cada mes 

def PlanificacionListView(request,pk):
# Mostrar la planificacion de la dupla de un establecimiento


	try:
		
		escuela=establecimiento.objects.get(id=pk)
		x= datetime.date.today() 
		annio=str(int(x.year))
		try:
			plan=Plan.objects.get(establecimiento=escuela,annio=annio)
		except Plan.DoesNotExist:
			plan=None
		
		base=Base.objects.filter(plan=plan)
		accion=Accion.objects.all()
		plancillo=Plancillo.objects.all()
		actividades=Actividades.objects.all()
		Listado=Lista.objects.filter(establecimiento=escuela)
		
		
	except establecimiento.DoesNotExist:
		
		
		plancillo=""
		accion=""
		base=""
		plan=""
		actividad=""
		escuela=""
		listado=""
	
	

	if request.method=='POST':
		formulario = Base_ActividadesPlanificacion(request.POST or None)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			plancillo=instance.plancillo
			accion=Plancillo.accion
			base=accion.base
			instance.accion=accion
			instance.usuario = request.user
				
			instance.save()
		
				
				
			url = reverse(('plan:ver_plancillo'), kwargs={ 'pk': accion.id,'base':base.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Base_ActividadesPlanificacion(request.POST or None)
	else:


				
		formulario = Base_ActividadesPlanificacion(request.POST or None)
	context = {
		"form": formulario,
		"indicador":accion,
		"accion_base":base,
		"Listado":Listado,
		"plan":plan,
		"escuela":escuela,
		 }
	return render(request, 'plan/plan_ingresar_planificacion_duplas.html', context)	    


#Para planificar las actividades de las duplas  dentro de cada mes 

def PlanificacionEncargadoListView(request,pk):
#Listar las acciones planificadas para el encargado de convivencia


	try:
		
		x= datetime.date.today() 
		annio=str(int(x.year))
		escuela=establecimiento.objects.get(id=pk)
		plan=Plan.objects.get(establecimiento=escuela,annio=annio)
		base=Base.objects.filter(plan=plan).order_by('fecha')
		accion=Accion.objects.all().order_by('fecha')
		plancillo=Plancillo.objects.all().order_by('fecha')
		actividades=Actividades.objects.all().order_by('fecha')
		Listado=Lista.objects.filter(establecimiento=escuela)


		
		
	except plan.DoesNotExist:
		
 
		plancillo=""
		accion=""
		base=""
		plan=""
		actividad=""
		escuela=""
	
	

	if request.method=='POST':
		formulario = Base_ActividadesPlanificacion(request.POST or None, instance=actividad)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			plancillo=instance.plancillo
			accion=Plancillo.accion
			base=accion.base
			instance.accion=accion
			instance.usuario = request.user
				
			instance.save()
		
				
				
			url = reverse(('plan:ver_plancillo'), kwargs={ 'pk': accion.id,'base':base.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Base_ActividadesPlanificacion(request.POST or None, instance=actividad)
	else:


				
		formulario = Base_ActividadesPlanificacion(request.POST or None)
	context = {
		"form": formulario,
		"indicador":accion,
		"accion_base":base,

		"plan":plan,
		"escuela":escuela,
		 }
	return render(request, 'plan/plan_ingresar_planificacion_encargado.html', context)	    

#Ingresar planificacion por area 1: Dupla PsicoSocial

def PlanificacionDuplaListView(request,pk,mes):
#Mostar planificacion por mes para las duplas 


	try:
		colegio=establecimiento.objects.get(id=pk)
		
		x= datetime.date.today() 
		annio=str(int(x.year))
		try:
			plan=Plan.objects.get(establecimiento=colegio,annio=annio)
		except Plan.DoesNotExist:
			plan=None
		

		base=Base.objects.filter(plan=plan)
		accion=Accion.objects.all()
		plancillo=Plancillo.objects.all()
		y = datetime.datetime.now().month
		mes_actual=mes
		actividades=Actividades.objects.filter((Q(ejecutores=0)|Q(ejecutores=1)|Q(ejecutores=3)|Q(ejecutores=4)) & Q(mes=mes) )

	
		
	except Actividades.DoesNotExist:
		colegio=""
		plan=""
		base=""
		accion=""
		plancillo=""
		actividades=""
	
	
	return render(
        request,
        'plan/planificar_ver_ficha_dupla.html',
        context={
        		 'colegio':colegio,
        		 'plan':plan,
        		 'base':base,
        		 'accion':accion,
        		 'plancillo':plancillo,
        		 'actividades':actividades,
        		 'mes_actual':mes_actual,
				 
        		 }
    )

# Mostar la planificacion de las del encargado de convivencia 
def PlanificacionEncargadoConvivenciaListView(request,pk,mes):
#Mostar planificacion por mes para el encargado de convivencia 


	try:
		colegio=establecimiento.objects.get(id=pk)
		
		x= datetime.date.today() 
		annio=str(int(x.year))
		plan=Plan.objects.get(establecimiento=colegio,annio=annio)

		base=Base.objects.filter(plan=plan)
		accion=Accion.objects.all()
		plancillo=Plancillo.objects.all()
		y = datetime.datetime.now().month
		mes_actual=mes
		
		actividades=Actividades.objects.filter( (Q(tipo=0)|Q(tipo=2)|Q(tipo=5)|Q(tipo=6)|Q(tipo=7)|Q(tipo=8)) & Q(mes=mes) )
	
		
	except Actividades.DoesNotExist:
		colegio=""
		plan=""
		base=""
		accion=""
		plancillo=""
		actividades=""
	
	
	return render(
        request,
        'plan/planificar_ver_ficha_encargado.html',
        context={'colegio':colegio,
        		 'plan':plan,
        		 'base':base,
        		 'accion':accion,
        		 'plancillo':plancillo,
        		 'actividades':actividades,
        		 'mes_actual':mes_actual,
				 
        		 }
    )

class ingresar_hecho_actividades(CreateView):
	model = Hecho_Actividades	
	form_class = Hecho_ActividadesForm
	template_name = 'plan/hecho_actividades_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ingresar_hecho_actividades, self).get_context_data(**kwargs)
			a = self.kwargs.get('pk') # El mismo nombre que en tu URL
			actividad_activa=Actividades.objects.get(id=a)
			plancillo=actividad_activa.plancillo
			accion=plancillo.accion
			base=accion.base
			plan=base.plan
			context['actividad']=actividad_activa
			context['plancillo']=plancillo
			context['accion']=accion
			context['base']=base
			context['plan']=plan

			return context
			
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		#form = self.form_class(request.POST)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		agenda = self.kwargs.get('agenda') # El mismo nombre que en tu URL
			
		if request.method == 'POST':
			form = Hecho_ActividadesForm(request.POST)
		        #codigo
			if form.is_valid():
				
				actividad_activa=Actividades.objects.get(id=pk)
				dia=actividad_activa.fecha.day
				mes=actividad_activa.fecha.month
				instance = form.save(commit=False)
					

				instance.estado=1
					
				instance.usuario=self.request.user
				instance.actividades=actividad_activa
				x= datetime.date.today()
				instance.fecha=x

				instance.save()
				actividad_activa.estado=1
				actividad_activa.save()
				# Actualizar la bitacora
				agendado=Lista.objects.get(id=agenda)
				agendado.numero=2
				agendado.save()
				url = reverse(('bitacora:fechas'), kwargs={ 'dia': dia , 'mes':mes })
				return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(form=form))

# Justificar una actividad desde la bitacora
class justificar_hecho_actividades(CreateView):
	model = Hecho_Actividades	
	form_class = Justificar_ActividadesForm
	template_name = 'plan/justificar_actividades_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(justificar_hecho_actividades, self).get_context_data(**kwargs)
			a = self.kwargs.get('pk') # El mismo nombre que en tu URL
			actividad_activa=Actividades.objects.get(id=a)
			plancillo=actividad_activa.plancillo
			accion=plancillo.accion
			base=accion.base
			plan=base.plan
			context['actividad']=actividad_activa
			context['plancillo']=plancillo
			context['accion']=accion
			context['base']=base
			context['plan']=plan

			return context
			
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		#form = self.form_class(request.POST)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		agenda = self.kwargs.get('agenda') # El mismo nombre que en tu URL
			
		if request.method == 'POST':
			form = Justificar_ActividadesForm(request.POST)
		        #codigo
			if form.is_valid():
				
				actividad_activa=Actividades.objects.get(id=pk)
				dia=actividad_activa.fecha.day
				mes=actividad_activa.fecha.month
				instance = form.save(commit=False)
					

				instance.estado=3
					
				instance.usuario=self.request.user
				instance.actividades=actividad_activa
				x= datetime.date.today()
				instance.fecha=x
				# Validar que no se ingrese un estado de justificacion euivocado
				if instance.estado == 0 or instance.estado == 1 or instance.estado == 2:
					instance.estado == 3
				instance.save()
				
				actividad_activa.save()
				# Actualizar la bitacora
				agendado=Lista.objects.get(id=agenda)
				agendado.numero=3
				agendado.save()
				url = reverse(('bitacora:fechas'), kwargs={ 'dia': dia , 'mes':mes })
				return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(form=form))

# Reagendar  una actividad desde la bitacora
class reagendar_hecho_actividades(CreateView):
	model = Hecho_Actividades	
	form_class = Reagendar_ActividadesForm
	template_name = 'plan/reagendar_actividades_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(reagendar_hecho_actividades, self).get_context_data(**kwargs)
			a = self.kwargs.get('pk') # El mismo nombre que en tu URL
			actividad_activa=Actividades.objects.get(id=a)
			plancillo=actividad_activa.plancillo
			accion=plancillo.accion
			base=accion.base
			plan=base.plan
			form_class = Reagendar_ActividadesForm(instance=actividad_activa)
			context['actividad']=actividad_activa
			context['plancillo']=plancillo
			context['accion']=accion
			context['base']=base
			context['plan']=plan
			context['form']=form_class
			
			


			return context
			
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		#form = self.form_class(request.POST)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		agenda = self.kwargs.get('agenda') # El mismo nombre que en tu URL
					
		if request.method == 'POST':
			form = Reagendar_ActividadesForm(request.POST)
			       #codigo
			if form.is_valid():
				form.instance = form.save(commit=False)
				#verificar si la actividad ya existe 
				try:
					agendado=Lista.objects.get(horario=form.instance.horario,fecha=form.instance.fecha,usuario=self.request.user)
									#agendado=Lista.objects.get(Q(horario=instance.horario) & Q(fecha=instance.fecha) & Q(usuario=usuario) & Q(fecha__gte=hoy))            
															
					
					url = reverse(('plan:reagendar_hecho_actividades'), kwargs={ 'agenda': agenda, 'pk': pk })

					return HttpResponseRedirect(url)
				except Lista.DoesNotExist:
					actividad_activa=Actividades.objects.get(id=pk)
					dia=actividad_activa.fecha.day
					mes=actividad_activa.fecha.month
					instance = form.save(commit=False)
										

					form.instance.estado=1
									
					form.instance.usuario=self.request.user
					form.instance.actividades=actividad_activa
					form.instance.plancillo=actividad_activa.plancillo
					x= datetime.date.today()

					
					
					actividad_activa.estado=2
					actividad_activa.fecha=form.instance.fecha
					actividad_activa.horario=form.instance.horario
					
					
					actividad_activa.save()
								# Actualizar la bitacora

					agendado=Lista.objects.get(id=agenda)

					agendado.numero=1
					agendado.fecha=form.instance.fecha
					agendado.horario=form.instance.horario
					agendado.save()

					#Crear la entrada en el hecho de activivdades 
					Hecho_Actividades.objects.create(fecha=form.instance.fecha,observacion=str(form.instance.horario),
							estado=2,actividades=actividad_activa,logros="",
							mejora="",usuario=self.request.user)
	

			url = reverse(('bitacora:fechas'), kwargs={ 'dia': dia , 'mes':mes })
			return HttpResponseRedirect(url)
		else:
			return self.render_to_response(self.get_context_data(form=form))


# Listar una actividad VER 
#-------
class ver_actividades_bitacora(ListView):
    model = Actividades 
    
    template_name = 'plan/ver_actividad_form.html'
    success_url = reverse_lazy('comienza:ver_dupla')

    def get_context_data(self, **kwargs):
            # Llamamos ala implementacion primero del  context
            context = super(ver_actividades_bitacora, self).get_context_data(**kwargs)
            pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
            lista=Lista.objects.get(id=pk)
            dia=lista.fecha.day
            mes=lista.fecha.month
            actividades=lista.actividad
            
            
            try:
                actividad=Actividades.objects.get(pk=actividades.id)
                hecho_a=Hecho_Actividades.objects.filter(actividades=actividades)
                plancillo=actividades.plancillo
                accion=plancillo.accion
                base=accion.base
                plan=base.plan

                context['plan']=plan
                context['actividad']=actividad
                context['accion']=accion
                context['base']=base
                context['dia']=dia
                context['mes']=mes
                context['hecho_a']=hecho_a
                
                return context
            except Actividades.DoesNotExist:
                context['plan']=None
                context['accion']=None
                context['base']=None
                context['dia']=None
                context['mes']=None

                context['actividades']=None
                return context
#-----



def PlanListViewTodos(request,pk):
#Llistar todos los planes anteriores 

	
	colegio=establecimiento.objects.get(id=pk)
	try:
		planes=Plan.objects.filter(establecimiento=colegio)
		
	except Plan.DoesNotExist:
		planes=None
	
		
	return render(
        request,
        'plan/plan_todos.html',
        context={'colegio':colegio,
        		 'planes':planes,
        		 
        		 }
    )
# Ver todos los planes mineduc de un establecimiento

def PlanListViewMineduc(request,pk):
#Llistar todos los planes anteriores 

	
	colegio=establecimiento.objects.get(id=pk)
	try:
		planes=Planes_mineduc.objects.filter(establecimiento=colegio)
		
	except Plan.DoesNotExist:
		planes=None
	
		
	return render(
        request,
        'plan/plan_todos_mineduc.html',
        context={'colegio':colegio,
        		 'planes':planes,
        		 
        		 }
    )

# Listar los datos de un plan en particular
def PlanmineducListView(request,pk):

	try:
 		planes=Planes_mineduc.objects.get(id=pk)
		colegio=planes.establecimiento
	except DiagnosticoI.DoesNotExist:
		planes=None
		
	if request.method == 'POST':
		form = PlanFormMineduc(request.POST)
		if form.is_valid():
			form.form.save()
			
			
		return redirect('plan:PlanListViewMineduc', pk=pk)
			
	else:
		form = PlanFormMineduc()
	

	form = PlanFormMineduc()
	return render(
        request,
        'plan/Planes_mineduc_ver_ficha.html',
        context={'colegio':colegio,
        		 'planes':planes,
        		 'form':form,
        		 }
    )


def modificar_plan(request,pk):
# modificar un lo ingresao en un plan actual
	
	plan= get_object_or_404(Plan, pk=pk)
	escuela=plan.establecimiento

	
	if request.method=='POST':
		formulario = PlanForm(request.POST or None, instance=plan)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.establecimiento=escuela
			instance.usuario = request.user
				
			instance.save()
		
				
			url = reverse(('plan:PlanListView'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = PlanForm(request.POST or None, instance=plan)
	else:


				
		formulario = PlanForm(request.POST or None, instance=plan)
	context = {
		"form": formulario,
		"plan":plan,
		"escuela":escuela,
		 }
	return render(request, 'plan/plan_form.html', context)	



class ver_bitacora_actividad(ListView):
    model = Actividades 
    
    template_name = 'plan/ver_bitacora_actividad.html'
    success_url = reverse_lazy('comienza:ver_dupla')

    def get_context_data(self, **kwargs):
            # Llamamos ala implementacion primero del  context
            context = super(ver_bitacora_actividad, self).get_context_data(**kwargs)
            pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
            lista=Lista.objects.get(id=pk)
            dia=lista.fecha.day
            mes=lista.fecha.month
            actividades=lista.actividad

            
            try:
                actividad=Actividades.objects.get(pk=actividades.id)
                plancillo=actividades.plancillo
                accion=plancillo.accion
                base=accion.base
                plan=base.plan
                hecho_a=Hecho_Actividades.objects.filter(actividades=actividad).order_by('fecha')


                context['plan']=plan
                context['actividad']=actividad
                context['accion']=accion
                context['base']=base
                context['dia']=dia
                context['mes']=mes
                context['hecho_a']=hecho_a
                
                return context
            except Actividades.DoesNotExist:
                context['plan']=None
                context['accion']=None
                context['base']=None
                context['dia']=None
                context['mes']=None
                context['hecho_a']=None

                context['actividades']=None
                return context

# Duplicar plan 
class duplicar_plancillo(CreateView):
	model = Plancillo	
	form_class = Base_PlancilloForm
	template_name = 'plan/plancillo_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(duplicar_plancillo, self).get_context_data(**kwargs)
			accion = self.kwargs.get('pk') # El mismo nombre que en tu URL
			base= self.kwargs.get('base') # El mismo nombre que en tu URL
			planchico=self.kwargs.get('plancillo') # El mismo nombre que en tu URL
			base_activa=Base.objects.get(id=base)
			accion_activa=Accion.objects.get(id=accion)
			plancito=Plancillo.objects.get(id=planchico)
			actividades_copiadas=Actividades.objects.filter(plancillo=planchico)
			print plancito
			form = Base_PlancilloForm(instance=plancito)
			try:
				plan=Plancillo.objects.filter(accion=accion_activa)
				context['accion']=accion_activa
				context['plan']=plan

				context['mensaje']='Listado de planes / Actividades '
				context['base']=base_activa
				context['form']=form
				context['actividades_copiadas']=actividades_copiadas

				return context
			except Plancillo.DoesNotExist:
				context['accion']=accion_activa
				context['mensaje']='Listado de planes / Sin Cronogramas '
				context['base']=base_activa
				context['actividades_copiadas']=None				
				return context
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		planchico=self.kwargs.get('plancillo') # El mismo nombre que en tu URL
		plancito=Plancillo.objects.get(id=planchico)
		actividades_copiadas=Actividades.objects.filter(plancillo=plancito)
		print actividades_copiadas	
		form = Base_PlancilloForm(instance=plancito)
		
		if request.method == 'POST':
			form = Base_PlancilloForm(request.POST or None, instance=plancito)
			accion = self.kwargs.get('pk') # El mismo nombre que en tu URL
			base= self.kwargs.get('base') # El mismo nombre que en tu URL
			plancito=Plancillo.objects.get(id=planchico)
		        #codigo
			if form.is_valid():
				
				form.instance = form.save(commit=False)

				
				
				n =Plancillo.objects.create(fecha=form.instance.fecha,nombre=form.instance.nombre,responsable=form.instance.responsable,
							numero=form.instance.numero,letra=form.instance.letra,Curso=form.instance.Curso,
							cantidad_horas=form.instance.cantidad_horas,duracion=form.instance.duracion,
							justificacion=form.instance.justificacion,objetivo_general=form.instance.objetivo_general,
							objetivo_especificos=form.instance.objetivo_especificos,materiales=form.instance.materiales,
							reportes=form.instance.reportes,evaluacion=form.instance.evaluacion,accion=form.instance.accion,usuario=form.instance.usuario)
				n.save()

				
				plan_plancillo = Plancillo.objects.get(id=n.id)
				print plan_plancillo
				print actividades_copiadas
				for activo in actividades_copiadas:
					Actividades.objects.create(fecha=None,horario=1,mes=activo.mes,
						nombre=activo.nombre,tipo=activo.tipo,descripcion=activo.descripcion,ejecutores=activo.ejecutores,
						inicio=activo.inicio,desarrollo=activo.desarrollo,cierre=activo.cierre,participantes=activo.participantes,
						numero=activo.numero,letra=activo.letra,responsable=activo.responsable,cantidad_convocada=activo.cantidad_convocada,
						observaciones=activo.observaciones,planes_externos=activo.planes_externos,evaluacion=activo.evaluacion,
						estado=activo.estado,plancillo=plan_plancillo,usuario=activo.usuario
						

						)


				
				url = reverse(('plan:ver_plancillo'), kwargs={ 'pk': accion ,'base':base })

				return HttpResponseRedirect(url)
						
					
			else:
					
					
					url = reverse(('plan:ingresar_Actividad'), kwargs={ 'pk': pk })

					return HttpResponseRedirect(url)						
		else:
				form = Base_PlancilloForm(request.POST or None, instance=plancillo)
				return self.render_to_response(self.get_context_data(Base_PlancilloForm=form))

# Modificar una actividad solo construida

def modificar_actividad_plan(request,pk):
# Modificar un plan  
	
	actividad = get_object_or_404(Actividades, pk=pk)
	plancillo=actividad.plancillo
	print plancillo
	accion=plancillo.accion
	base=accion.base
	plan=base.plan
	escuela=plan.establecimiento
	colegio=escuela

	
	if request.method=='POST':
		formulario = Base_ActividadesPlan(request.POST or None, instance=actividad)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			
			instance.plancillo=plancillo
			instance.usuario = request.user
				
			instance.save()
			formulario.save_m2m()
				
				
			url = reverse(('plan:ver_actividades'), kwargs={ 'pk': plancillo.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Base_ActividadesPlan(request.POST or None, instance=actividad)
	else:


				
		formulario = Base_ActividadesPlan(request.POST or None, instance=actividad)
	context = {
		"form": formulario,
		"plan":plan,
		"base":base,
		"accion":accion,
		"plancillo":plancillo,

		"escuela":escuela,
		"colegio":colegio,

		 }
	return render(request, 'plan/actividades_form.html', context)	


# Modificar una actividad ya planificada
def modificar_actividad_planificada(request,pk):
# Modificar una actividad una vez planificada 
	
	actividad = get_object_or_404(Actividades, pk=pk)
	plancillo=actividad.plancillo
	accion=plancillo.accion
	base=accion.base
	plan=base.plan
	escuela=plan.establecimiento
	colegio=escuela

	
	if request.method=='POST':
		formulario = Base_ActividadesForm(request.POST or None, instance=actividad)
 		if formulario.is_valid():
			instance = formulario.save(commit=False)
			instance.plancillo=plancillo
			instance.usuario = request.user
			instance.save()
			formulario.save_m2m()
				
				
			url = reverse(('plan:ver_actividades'), kwargs={ 'pk': plancillo.id})
			return HttpResponseRedirect(url)
				
			
				
		formulario = Base_ActividadesForm(request.POST or None, instance=actividad)
	else:


				
		formulario = Base_ActividadesForm(request.POST or None, instance=actividad)
	context = {
		"form": formulario,
		"plan":plan,
		"base":base,
		"accion":accion,
		"plancillo":plancillo,

		"escuela":escuela,
		"colegio":colegio,

		 }
	return render(request, 'plan/actividades_form.html', context)	

# Duplicar una actividad 
class duplicar_Actividad_plan(CreateView):
	model = Actividades	

	form_class = Base_ActividadesPlan
	template_name = 'plan/Actividades_form.html'
	success_url = reverse_lazy('comienza:ver_dupla')

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(duplicar_Actividad_plan, self).get_context_data(**kwargs)
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			actividad=Actividades.objects.get(pk=pk)
			plancillo = actividad.plancillo
			form = Base_ActividadesPlan(instance=actividad)
			
			accion=plancillo.accion
			base=accion.base
			plan=base.plan
			actividad=Actividades.objects.get(pk=pk)
			
			context['plancito']=plancillo
			context['accion']=accion
			context['base']=base
			context['plan']=plan
			context['form']=form


			context['mensaje']=""
			
			return context
			
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			
		if request.method == 'POST':
			form = Base_ActividadesPlan(request.POST)
		        #codigo
			if form.is_valid():
				
				#Verificar si el plan existe 
				
				actividad=Actividades.objects.get(id=pk)
				plancito=actividad.plancillo
				accion=plancito.accion
				base=accion.base
				plan=base.plan	
				
				instance = form.save(commit=False)
				#Crear la actvidad en base a una ya creada
	
				
				instance.plancillo=plancito

				Actividades.objects.create(fecha=form.instance.fecha,horario=form.instance.horario,mes=form.instance.mes,
							nombre=form.instance.nombre,tipo=form.instance.tipo,descripcion=form.instance.descripcion,
							ejecutores=form.instance.ejecutores,inicio=form.instance.inicio,desarrollo=form.instance.desarrollo,
							cierre=form.instance.cierre,participantes=form.instance.participantes,
							numero=form.instance.numero,letra=form.instance.letra,responsable=form.instance.responsable,
							cantidad_convocada=form.instance.cantidad_convocada,

							
							observaciones=form.instance.observaciones,planes_externos=form.instance.planes_externos,
							evaluacion=form.instance.evaluacion,
							estado=form.instance.estado,plancillo=plancito,usuario=self.request.user)


	

			
				url = reverse(('plan:ver_actividades'), kwargs={ 'pk': plancito.id })
				return HttpResponseRedirect(url)
			else:
				return self.render_to_response(self.get_context_data(Base_ActividadesPlan=form))
				




