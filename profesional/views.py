# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from profesional.models import Profesional,Cargo
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from profesional.forms import CambioProfesionalForm,profesionalForm,CargoForm,Acciones_profesionalForm
from profesional.models import Acciones_profesional
from sesion.models import Intervenidos,Pasos_intervencion,Seguimiento
from alumno.models import Estudiante
from usuario.models import Profile
import datetime
from django.urls import reverse

# Create your views here.
class ProfesionalList(ListView):
	model = Profesional
	template_name = 'profesional/profesional_listar.html'
	paginate_by = 6


	def get_context_data(self, **kwargs):
		context=super(ProfesionalList,self).get_context_data(**kwargs)
		perfil=Profile.objects.get(user=self.request.user)
		if  perfil.area== 2 or  perfil.area== 3 or  perfil.area== 4:
			context['acceso'] = 1

		else:
			context['acceso'] = 0	        
		return context


# Listar equipo profesional por establecimiento dependiendo del director
class ProfesionalListDirector(ListView):
	model = Profesional
	template_name = 'profesional/profesional_listar_director.html'
	


	def get_context_data(self, **kwargs):
		context=super(ProfesionalListDirector,self).get_context_data(**kwargs)
		perfil=Profile.objects.get(user=self.request.user)
		
		if  perfil.area== 7:
			
			director=Profesional.objects.get(usuario=self.request.user)
			funcion_cargo=Cargo.objects.filter(profesional=director)
			for cargos in funcion_cargo:
				funcion=cargos

	
			equipo=Cargo.objects.filter(escuela=funcion.escuela)
			print equipo
			context['equipo'] = equipo
			context['escuela'] = funcion.escuela


		else:
			context['equipo'] = None	        
		return context


class ProfesionalListCentro(ListView):
	model = Profesional
	template_name = 'profesional/profesional_listar_centro.html'
	paginate_by = 6

	def get_context_data(self, **kwargs):
		context=super(ProfesionalListCentro,self).get_context_data(**kwargs)
		perfil=Profile.objects.get(user=self.request.user)
		if  perfil.area== 2 or  perfil.area== 3 or  perfil.area== 4:
			context['acceso'] = 1
		else:
			context['acceso'] = 0	        
		return context


class ProfesionalCreate(CreateView):
	model = Profesional
	form_class = profesionalForm
	template_name = 'profesional/profesional_form.html'
	success_url = reverse_lazy('profesional:profesional_listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)		
		if form.is_valid():

			ingresado=form.save(commit=False)
			usuario=ingresado.usuario
			#dupla=ingresado.profesional
			#profesional_dupla=Profesional.objects.get(id=dupla.id)

			#num=profesional_dupla.tipo_profesional+1
			
			
			Profile.objects.create(user=ingresado.usuario, adress=ingresado.domicilio,location='Cabildo',birth_date='2018-02-02',area=num)
			ingresado.save()
			form.save_m2m()
			url = reverse(('profesional:profesional_listar'))
			return HttpResponseRedirect(url)
			
		else:
			return self.render_to_response(self.get_context_data(form=form))

	

class ProfesionalUpdate(UpdateView):
	model = Profesional
	form_class = profesionalForm
	template_name = 'profesional/profesional_form.html'
	success_url = reverse_lazy('profesional:profesional_listar')


class ProfesionalDelete(DeleteView):
	model = Profesional
	template_name = 'profesional/profesional_delete.html'
	success_url = reverse_lazy('profesional:profesional_listar')	


#cambiar profesional 
	
def CambioCreateView(request,pk):

	dato = get_object_or_404(Estudiante, pk=pk)

	intervenido=Intervenidos.objects.get(Estudiante_id=dato)

	intervenido_id=intervenido.id

	if request.method=='POST':
		formulario = CambioProfesionalForm(request.POST,request.FILES)
 		if formulario.is_valid():
 			instance = formulario.save(commit=False)
			instance.Intervenidos=intervenido
			instance.que_paso='Cambio de Psícologa o Psícologo del centro de Bienestar'
			date = datetime.date.today()
			instance.fecha_pasos=date 

			instance.save()
			usuario=formulario.instance.usuario
			
			infoarchivo2 = Intervenidos.objects.get(id = intervenido_id)
			infoarchivo2.usuario=usuario
			#infoarchivo2.Profesional=usuario.first_name+ " "+usuario.last_name
			infoarchivo2.numero = 2
			infoarchivo2.save()



			return HttpResponseRedirect('/derivacion/intervencion_list')
	else:
		formulario = CambioProfesionalForm()

	context = {
		"formulario": formulario,
		"dato": dato,
		"intervenido":intervenido,
		 }
	return render(request, 'profesional/cambio_profesional.html', context)	

# Crear accion profesional 
class AccionProfesional(CreateView):
	model = Acciones_profesional    
	form_class = Acciones_profesionalForm
	template_name = 'profesional/accion_profesional_form.html'
	success_url = reverse_lazy('profesional:AccionesProfesionalList')
	paginate_by = 100	    
	def get_context_data(self, **kwargs):
	            # Llamamos ala implementacion primero del  context
		context = super(AccionProfesional, self).get_context_data(**kwargs)
		            
		            #pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		usuario=self.request.user
		            
		profesional=Profesional.objects.get(usuario=usuario)
		context['profesional']=profesional
		context['usuario']=usuario
		            
		return context
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			solicitud = form.save(commit=False)
			x= datetime.date.today() 
			solicitud.fecha=x
			profesional=Profesional.objects.get(usuario=self.request.user)
			solicitud.profesional=profesional
			solicitud.save()
			
			# Retornamos el objeto
			url = reverse(('profesional:AccionesProfesionalList'))
			return HttpResponseRedirect(url)


# Crear accion profesional 
class AccionProfesionalCentro(CreateView):
	model = Acciones_profesional    
	form_class = Acciones_profesionalForm
	template_name = 'profesional/accion_profesional_centro_form.html'
	success_url = reverse_lazy('profesional:AccionesProfesionalList')
	paginate_by = 100	    
	def get_context_data(self, **kwargs):
	            # Llamamos ala implementacion primero del  context
		context = super(AccionProfesionalCentro, self).get_context_data(**kwargs)
		            
		            #pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		usuario=self.request.user
		            
		profesional=Profesional.objects.get(usuario=usuario)
		context['profesional']=profesional
		context['usuario']=usuario
		            
		return context
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			solicitud = form.save(commit=False)
			x= datetime.date.today() 
			solicitud.fecha=x
			profesional=Profesional.objects.get(usuario=self.request.user)
			solicitud.profesional=profesional
			solicitud.save()
			
			# Retornamos el objeto
			url = reverse(('profesional:AccionesProfesionaCentrolList'))
			return HttpResponseRedirect(url)

# Listar acciones extras profesionales del centro bienestar

# Agregar acciones a los profesionales en la medida que se realicen acciones 
class AccionesProfesionaCentrolList(ListView):
	model = Acciones_profesional
	template_name = 'profesional/accion_profesional_centro_listar.html'

 
 	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(AccionesProfesionaCentrolList, self).get_context_data(**kwargs)
		
		# ubicar profesional por medio del user

		try:
			profesional=Profesional.objects.get(usuario=self.request.user)
			acciones=Acciones_profesional.objects.filter(profesional=profesional)
			
		except Profesional.DoesNotExist:
			profesional=None
			acciones=None
		
		context['profesional']=profesional
		context['acciones']=acciones
		
		return context

# Agregar acciones a los profesionales en la medida que se realicen acciones 
class AccionesProfesionalList(ListView):
	model = Acciones_profesional
	template_name = 'profesional/accion_profesional_listar.html'

 
 	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(AccionesProfesionalList, self).get_context_data(**kwargs)
		
		# ubicar profesional por medio del user

		try:
			profesional=Profesional.objects.get(usuario=self.request.user)
			acciones=Acciones_profesional.objects.filter(profesional=profesional)
			
		except Profesional.DoesNotExist:
			profesional=None
			acciones=None
		
		context['profesional']=profesional
		context['acciones']=acciones
		
		return context
# Listar el seguimiento de modo total
class SeguimientoProfesionalList(ListView):
	model = Seguimiento
	template_name = 'profesional/accion_profesional_listar_Seguimiento.html'
	paginate_by = 5
 
 	def get_context_data(self, **kwargs):
		context = super(SeguimientoProfesionalList, self).get_context_data(**kwargs)
		profesional=Profesional.objects.get(usuario=self.request.user)
		
		try:
			seguimiento=Seguimiento.objects.filter(usuario=self.request.user).order_by('fecha')
		
		except Seguimiento.DoesNotExist:
			seguimiento=None
		
	    
		context['profesional']=profesional
		context['seguimiento']=seguimiento
		
		return context

# Proceso de borrado de una accion externa realizada
class AccionExternaDelete(DeleteView):

	model = Acciones_profesional
	template_name = 'profesional/accion_eliminar.html'
	success_url = reverse_lazy('profesional:AccionesProfesionalList')	

	def get_context_data(self, **kwargs):
		context=super(AccionExternaDelete,self).get_context_data(**kwargs)
		return context

	# Listar los seguimientos realizados por un profesion al determinado
class ListarSeguimiento(ListView):
	model = Seguimiento
	template_name = 'profesional/ver_seguimiento.html'
	paginate_by = 50
#muestra a todas las derivaciones realizadas   
	
	  
	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(ListarSeguimiento, self).get_context_data(**kwargs)
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			seguimiento=Seguimiento.objects.get(pk=pk)
			estudiante=seguimiento.Estudiante
			escuela=estudiante.curso.establecimiento
			
		
			
			context['seguimiento']=seguimiento
			context['dato']=estudiante

			
			return context