# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView,TemplateView,View
from derivacion.forms import derivacionForm,IntervencionForm,FormRetorno,MotivoRetornoForm,RetornoFaltainfoForm
from derivacion.models import Ficha_derivacion
from alumno.models import Estudiante,Escolaridad
from alumno.models import curso
from alumno.models import Profesor
from alumno.models import establecimiento
from alumno.forms import EstudianteForm
from derivacion.models import Bitacora,intervencion,Retorno,Red_apoyo,Motivo_Retorno_Ficha_derivacion
from profesional.models import Profesional
from profesional.forms import ProfesinalEstablecimientoForm
from sesion.models import Intervenidos,Pasos_intervencion,Estado,sesion
from django.urls import reverse
from datetime import datetime
import time
import datetime
from django.db.models import Q
# Usados para borrar los archivos de las fichas
from django.db.models.signals import pre_delete
from django.dispatch import receiver
#from django_pdf.utileria import render_pdf
#Historia de los estudiantes del centro

#historia de una ficha retornada
def historia_retorno(request,ficha,pk):
	mensaje=""
	estudiante_id= get_object_or_404(Estudiante, pk=pk)	
	estudiante=estudiante_id.id

	ficha_id=Ficha_derivacion.objects.get(Ficha_derivacion__id=ficha,estado=1)
	sesiones = sesion.objects.get(sesion__Estudiante__id=pk)


	try:
 			 # try something
 		hoy= objetivo_intervencion.objects.filter(objetivo_intervencion__Estudiante__id=pk,activo=1)
 		

	except objetivo_intervencion.DoesNotExist:
			  # do something
		hoy=None				
	if hoy==None:	
		mensaje='Debe ingresar  objetivos'

	else:	
		viejos=	objetivo_intervencionhistoria.objects.filter(objetivo_intervencionhistoria__Estudiante__id=pk)	
		
    #book_id=get_object_or_404(Book, pk=pk)
    
	return render(
		request,
		'sesion/historia.html',
		 context={
	     'estudiante':estudiante_id,
	     'ficha':ficha_id,
       	 'objetivo':hoy,
          'mensaje':mensaje,
          'viejos':viejos,
          'sesiones':sesiones,
        		 
        		 
	})

#mensaje de gracias
def gracias(request):
    
    return render (request,"derivacion/mensaje.html",{})	


#Ver a todos los intervenidos 
class EntradasFicha(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion
	template_name = 'derivacion/entradas_totales.html'
	paginate_by = 100
#muestra a todas las derivaciones realizadas   
	
	def get_queryset(self):
		queryset = super(EntradasFicha, self).get_queryset()
		return queryset.filter(derivado=2,estado=1)

	def get_context_data(self, **kwargs):
		context = super(EntradasFicha, self).get_context_data(**kwargs)
		intervenidos = Intervenidos.objects.all()
		
		context['intervenidos'] = intervenidos
		return context		


#Ver a todos los intervenidos  por el supervisor
class EntradasFichaSupervisor(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion
	template_name = 'derivacion/entradas_totales_supervisor.html'
	paginate_by = 100
#muestra a todas las derivaciones realizadas   
	
	def get_queryset(self):
		queryset = super(EntradasFichaSupervisor, self).get_queryset()
		return queryset.filter(derivado=2,estado=1)

	def get_context_data(self, **kwargs):
		context = super(EntradasFichaSupervisor, self).get_context_data(**kwargs)
		intervenidos = Intervenidos.objects.all()
		
		context['intervenidos'] = intervenidos
		return context		




#Ver a todas las fichas intervenidas
class ModificarFicha(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion
	template_name = 'derivacion/modificar_entradas_totales.html'
	paginate_by = 6
#muestra a todas las derivaciones realizadas   
	
	def get_queryset(self):
		queryset = super(ModificarFicha, self).get_queryset()
		return queryset.filter(derivado=2,estado=1,usuario=self.request.user)
	

	def get_context_data(self, **kwargs):
		context = super(ModificarFicha, self).get_context_data(**kwargs)
		dato = Estudiante.objects.all()
		context['dato'] = dato
		return context	


#Listar las intervencion del usuario actual

class EntradasList(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Intervenidos 
	template_name = 'sesion/intervenidos_profesional.html'
	paginate_by = 6
 
 	def get_queryset(self):
		queryset = super(EntradasList, self).get_queryset()
		
		return queryset.filter(usuario=self.request.user)

	

#listado de derivaciones derv¡vadas a otras instituciones
class EntradasOtrasList(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion
	template_name = 'derivacion/entradas_ficha.html'
	paginate_by = 5
#muestra a todas las derivaciones realizadas   
	
	def get_queryset(self):
		queryset = super(EntradasOtrasList, self).get_queryset()
		return queryset.filter(derivado=2,pasada=4,estado=1)
#listado de derivaciones retoro dupla
class EntradasRetornoDuplaList(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion
	template_name = 'derivacion/entradas_fichas_termino.html'
	paginate_by = 5
#muestra a todas las derivaciones realizadas   
	
	def get_queryset(self):
		queryset = super(EntradasRetornoDuplaList, self).get_queryset()
		return queryset.filter((Q(pasada=4) | Q(pasada=7)) & Q(estado= 1))


	def get_context_data(self, **kwargs):
		context = super(EntradasRetornoDuplaList, self).get_context_data(**kwargs)
		intervenidos = Intervenidos.objects.all()
		context['intervenidos'] = intervenidos
		return context




#Grabar la primera intervencion
class asignar_intervencion(CreateView):
	model = intervencion	
	form_class = IntervencionForm
	template_name = 'derivacion/asignar_atencion.html'
	success_url = reverse_lazy('derivacion:derivacion_listar')

	def form_valid(self,form):
	    self.object = form.save(commit=False)
	    form.instance.usuario = self.request.user
	    form.instance.pasada=1
	    form.instance.derivado=1

	    self.object.save()
	    #return super(MascotaCreate, self).form_valid(form)
	    return super(asignar_intervencion, self).form_valid(form)

#para asignar los profesionales a asignar a un estudiante
		  
class AsignarUpdateView(UpdateView):
# salir un estudiante de la lista de espera
	model=Ficha_derivacion
	fields = ["pasada"]
	template_name = 'derivacion/pasada_lista_espera.html'
	success_url = reverse_lazy('derivacion:centro_listar')
	
	def get_context_data(self,**kwargs):
        # Llamamos ala superclase
		context=super(AsignarUpdateView,self).get_context_data(**kwargs)
		return context
	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object
		object = super(AsignarUpdateView, self).get_object()
        # Grabamos el valor 3 porque sale de la lista de eppera 
		object.pasada = 3 #significa que ya no esta en lista de espera
		object.save()
        # Retornamos el objeto
		return HttpResponseRedirect(self.get_success_url())    
        	
# enviar a una intervencion aun estudiante

#la clase para el metodo ajax de los prefesionales
class BusquedaAjaxView(TemplateView):
	def get(self,request,*args,**kwargs):
		id_profesional=request.GET['id']
		print id_profesional
	



#para traer a un estudiante
class BitacoraDetailView(DetailView):
    model = Bitacora
    template_name = 'derivacion/bitacora.html'
    

def get_context_data(self, **kwargs):
        context = super(BitacoraDetailView, self).get_context_data(**kwargs)
        context['certifica'] =BItacora.nombres
        return context



class EntradasBitacora(ListView):
        '''Entradas por mes'''
	model = Bitacora
	template_name = 'derivacion/listar_bitacora.html'
#muestra a todas las derivaciones realizadas   
    
def get_queryset(self, *args, **kwargs):
        return Bitacora.objects.filter(user=self.request.user)



def listadousuarios(request):
	lista = serializers.serialize('json', User.objects.all(), fields=['username', 'first_name'])
	return HttpResponse(lista, content_type='application/json')

def index(request):
	return render(request, 'derivacion/index.html')
	
def mascota_view(request):
	if request.method == 'POST':
		form = MascotaRAForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('derivacion:mascotara_listar')
	else:
		form = MascotaRAForm()
	return render(request, 'derivacion/mascotara_form.html', {'form':form})



def centro_deriva(request):
	if request.method == 'POST':
		form = MascotaRAForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('derivacion:mascotara_listar')
	else:
		form = MascotaRAForm()
	return render(request, 'derivacion/mascotara_form.html', {'form':form})	


def mascota_list(request):
	mascota = ficha_derivacion.objects.filter(pasada=True)
	contexto = {'mascotas':mascota}
	return render(request, 'derivacion/mascotara_list.html', contexto)


class seguimientoListView(ListView): 
	model = Ficha_derivacion 
	template_name = 'derivacion/listar_centro.html'
	paginate_by = 5
#muestra a todas las derivaciones realizadas   
	
	def get_queryset(self):
		queryset = super(seguimientoListView, self).get_queryset()
		return queryset.filter((Q(derivado=2) & Q(pasada=1)) & Q(estado=1))
		


##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
#Para listar los estudiantes intervenidos
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# para mostrar todos los estudiantes en intervencion
# para mostrar todos los estudiantes en proceso 
class seguimientocentroListView(ListView): 
	model = Ficha_derivacion 
	template_name = 'derivacion/listar_centro.html'
#muestra a todas las derivaciones realizadas    
	def get_queryset(self, *args, **kwargs):
		return Ficha_derivacion.objects.filter(derivado=2,Pasada=3,estado=1)
# para mostrar todos los estudiantes en proceso 
  
class listaesperaListView(ListView): 
	model = Ficha_derivacion 
	template_name = 'derivacion/espera_centro.html'
#muestra las lista de espera  
	def get_queryset(self, *args, **kwargs):
		
		return Ficha_derivacion.objects.filter(pasada=2,estado=1)

def estudiante_list(request):
	mascota = Estudiante.objects.all().order_by('id')
	contexto = {'Estudiante':Estudiante}
	return render(request, 'derivacion/estudiante_list.html', contexto)

def mascota_edit(request, ):
	mascota = ficha_derivacion.objects.get(id=id_MascotaRA,estado=1)
	if request.method == 'POST':
		form = MascotaRAForm(instance=mascota)
	else:
		form = MascotaRaForm(request.POST, instance=mascota)
		if form.is_valid():
			form.save()
		return redirect('derivacion:secretaria_listar')
	return render(request, 'derivacion/mascotara_form.html', {'form':form})



def mascota_delete(request, id_MascotaRA):
	mascota = MascotaRA.objects.get(id=id_MascotaRA)
	if request.method == 'POST':
		MascotaRA.delete()
		return redirect('derivacion:derivacion_listar')
	return render(request, 'derivacion/mascotara_delete.html', {'mascota':mascota})

class MascotaList(ListView):
	
	paginate_by = 6
	
	template_name = 'derivacion/mascotara_list.html'
	def get_queryset(self, *args, **kwargs):
		return Ficha_derivacion.objects.filter(usuario=self.request.user,derivado=1)

#listado de las derivaciones realizadas por usuario 

class MascotaseguimientoList(ListView):
	
	paginate_by = 5
	
	template_name = 'derivacion/mascotara_list.html'
	def get_queryset(self, *args, **kwargs):
		return Ficha_derivacion.objects.filter(usuario=self.request.user,estado=1)


# para mostra el retorno
class RetornoList(ListView):
	
	paginate_by = 6
	template_name = 'derivacion/listar_retorno.html'
	
	def get_queryset(self, *args, **kwargs):
		return Ficha_derivacion.objects.filter(usuario=self.request.user,pasada=5,estado=1)
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(RetornoList, self).get_context_data(**kwargs)
		context['retorno']=Motivo_Retorno_Ficha_derivacion.objects.filter(**kwargs)
        # Agregamos el publisher
		
		#query = super(RetornoList, self).Ficha_derivacion.queryset()
		#print query
		#context['Motivo_Retorno_Ficha_derivacion'] = self.Motivo_Retorno_Ficha_derivacion
		return context

# para mostra el retorno a otra institucion 
class RetornoInstList(ListView):
	
	paginate_by = 100
	template_name = 'derivacion/listar_retorno_inst.html'
	success_url = reverse_lazy('derivacion:derivacion_listar')
	def get_queryset(self, *args, **kwargs):
		return Ficha_derivacion.objects.filter(Q(usuario=self.request.user) & (Q(pasada=4) | Q(pasada=7)) & Q(estado=1))
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(RetornoInstList, self).get_context_data(**kwargs)
		context['retorno']=Motivo_Retorno_Ficha_derivacion.objects.filter(**kwargs)
		print context
        # Agregamos el publisher
		
		#query = super(RetornoList, self).Ficha_derivacion.queryset()
		#print query
		#context['Motivo_Retorno_Ficha_derivacion'] = self.Motivo_Retorno_Ficha_derivacion
		return context



class MascotaCreate(CreateView):
	model = Ficha_derivacion	
	form_class = derivacionForm
	template_name = 'derivacion/mascotara_form.html'
	success_url = reverse_lazy('derivacion:derivacion_listar')
	
	    
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(MascotaCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		print pk
		try:
			ficha=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
			mensaje="Estudiante ya cuenta con ficha de derivación"
		except Ficha_derivacion.DoesNotExist:
			mensaje="Estudiante sin ficha de derivación"
		
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
			try:
				ficha=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
				return self.render_to_response(self.get_context_data(form=form))
			except Ficha_derivacion.DoesNotExist:
				
				form.instance= form.save(commit=False)
				#motivos=form.instance.Motivo_derivacion
				#for motivo in motivos:

				#	form.intance.Motivo_derivacion.add(motivo)
				form.instance.usuario = self.request.user
				form.instance.pasada=1
				form.instance.derivado=1
				
				estudiante=Estudiante.objects.get(id=pk)
				form.instance.Estudiante=estudiante
				#Campos para registrar valores al moemnto de crear la ficha
				form.instance.edad=estudiante.edad
				form.instance.establecimiento=estudiante.curso.establecimiento.nombre
				form.instance.curso=estudiante.curso.get_numero()
				form.instance.letra=estudiante.curso.get_letra()
				form.instance.save()
				form.save_m2m()
			
				
				
				url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': estudiante.curso.establecimiento.id })
				return HttpResponseRedirect(url)

		else:
			mensaje="Ficha ya existe"
			return self.render_to_response(self.get_context_data(form=form))

# Prueba el ingreso de la ficha de derivacion	    
class MascotaCreate_Prueba(CreateView):
	model = Estudiante	
	form_class = EstudianteForm
	second_form_class= ProfesinalEstablecimientoForm
	template_name = 'alumno/ingresar_escolaridad.html'
	success_url = reverse_lazy('alumno:estudiante_listar')

	
	def get_context_data(self, **kwargs):
		context = super(MascotaCreate_Prueba, self).get_context_data(**kwargs)
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
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

# vista para almacenar el motivo de la devuelta a la dupla
class MascotaUpdate(UpdateView):
	model = Ficha_derivacion
	form_class = derivacionForm
	template_name = 'derivacion/mascotara_form.html'
	success_url = reverse_lazy('derivacion:derivacion_listar')

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		
		context = super(MascotaUpdate, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk')
		ficha=Ficha_derivacion.objects.get(id=pk,estado=1)
		escuela=establecimiento.objects.get(id=ficha.Estudiante.curso.establecimiento.id)
		escolar=Escolaridad.objects.get(Estudiante__id=ficha.Estudiante.id)
		dato=ficha.Estudiante
		context['escolar'] = escolar
		context['escuela'] = escuela
		context['dato'] = dato
		return context

class MascotaUpdate(UpdateView):
	model = Ficha_derivacion
	form_class = derivacionForm
	template_name = 'derivacion/mascotara_form_centro.html'
	success_url = reverse_lazy('derivacion:derivacion_listar')

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		
		context = super(MascotaUpdate, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk')
		ficha=Ficha_derivacion.objects.get(id=pk,estado=1)
		escuela=establecimiento.objects.get(id=ficha.Estudiante.curso.establecimiento.id)
		escolar=Escolaridad.objects.get(Estudiante__id=ficha.Estudiante.id)
		dato=ficha.Estudiante
		context['escolar'] = escolar
		context['escuela'] = escuela
		context['dato'] = dato
		return context

	

class MascotaUpdate_centro(UpdateView):
	model = Ficha_derivacion
	form_class = derivacionForm
	template_name = 'derivacion/mascotara_centro_form.html'
	success_url = reverse_lazy('derivacion:intervencion_listar')

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		
		context = super(MascotaUpdate_centro, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk')
		ficha=Ficha_derivacion.objects.get(id=pk,estado=1)
		escuela=establecimiento.objects.get(id=ficha.Estudiante.curso.establecimiento.id)
		escolar=Escolaridad.objects.get(Estudiante__id=ficha.Estudiante.id)
		dato=ficha.Estudiante
		context['escolar'] = escolar
		context['escuela'] = escuela
		context['dato'] = dato

		return context
	def post(self, request, *args,**kwargs):
		pk = self.kwargs.get('pk')
		ficha=Ficha_derivacion.objects.get(id=pk)
		estudiante=ficha.Estudiante
		form = self.get_form()

		if request.method=='POST':
			form = derivacionForm(request.POST, request.FILES)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.Estudiante=estudiante
				
				instance.usuario=request.user
				instance.save()



				return super(MascotaUpdate_centro, self).form_valid(form)
		else:
			return super(MascotaUpdate_centro, self).form_invalid(form)

class MascotaDelete(DeleteView):
	model = Ficha_derivacion
	template_name = 'derivacion/mascotara_delete.html'
	success_url = reverse_lazy('derivacion:derivacion_listar')	
# pasar una derivacion al centro 
# Usamos el Decorador receiver para ejecutar nuestra función
# cuando el Post el borrado.
	@receiver(pre_delete, sender=Ficha_derivacion)
	def post_pre_delete_handler(sender, instance, **kwargs):
	    instance.Imagen.delete(False)

class DerivacionUpdate(UpdateView):
	model = Ficha_derivacion
	form_class = derivacionForm
	template_name = 'derivacion/mascotara_form.html'
	success_url = reverse_lazy('derivacion:derivacion_listar')

class Modificarderivacion(UpdateView):
    #Especificamos que el modelo a utilizar para modificar una derivacion
    model = Ficha_derivacion
    #Establecemos que la plantilla se llamara modificar persona
    template_name = 'lista_espera.html'
    #Determinamos los campos con los que se va a trabajar, esto es obligatorio sino nos saldra un error
    fields = ['Estudiante.nombre','Estudiante.firs_name','Estudiante.last_name','pasada']
    #Con esta linea establecemos que se hara despues que la operacion de modificacion se complete correctamente
    success_url = reverse_lazy('derivacion:centro_listar')

# Proceso de envio de cada una de las derivaciones
class EsperaUpdateView(UpdateView):
# pasar una derivacion a lista de espera

	model=Ficha_derivacion

	fields = ["pasada","derivado"]
	template_name = 'derivacion/pasada_lista_espera.html'
	success_url=reverse_lazy('derivacion:centro_listar')
    #success_url = reverse_lazy('derivacion:centro_listar')
	

	def get_context_data(self, **kwargs):
		context=super(EsperaUpdateView,self).get_context_data(**kwargs)
		return context

	def get_queryset(self):
		queryset = super(EsperaUpdateView, self).get_queryset()
		return queryset.filter(estado=1)

	def post(self,request,*args,**kwargs):
		        # Llamamos ala superclase
		self.object=self.get_object
		object = super(EsperaUpdateView, self).get_object()
	        # Grabamos el valor 2 que es lidta de espera
		object.pasada = 2 # porque 2 significa que esta en lista de espera
		object.derivado = 2 # porque 3 significa que ya paso por la revison del centro
		object.fecha_espera= datetime.datetime.now()
		object.save()
	        # Retornamos el objeto
	        #return object
		return HttpResponseRedirect(self.get_success_url())    




#Enviar a otra institucion
class RedapoyoUpdateView(UpdateView):
# pasar una derivacion a lista de espera
	queryset = Ficha_derivacion.objects.filter(estado=1)
	fields = ["observacion"]
	template_name = 'derivacion/pasada_red_apoyo.html'
    #success_url = reverse_lazy('derivacion:centro_listar')
	def get_object(self,request,*args,**kwargs):
		observacion=request.GET[observacion]
		Ficha=ficha_derivacion.objects.get(id=id,estado=1)
		        # Llamamos ala superclase
		object = super(RedapoypUpdateView,self).get_object()
		        # Grabamos el valor 2 que es lidta de espera
		object.observacion = observacion # porque 2 significa que esta en lista de espera
			

		object.save()
	        # Retornamos el objeto
	        #return object
        
	def get_success_url(self):
		#return reverse("derivacion:centro_listar")
		#success_url = reverse_lazy('derivacion:centro_listar')
		success_url = '/'
# enviar a una intervencion aun estudiante
def request_GET_D(campo):
	camtot=''
	camyear=campo+'_year'
	cammonth=campo+'_month'
	camday=campo+'_day'
	dia='00'+request_GET(request,camday)
	dia=dia[-2:]
	mes='00'+request_GET(request,cammonth)
	mes=mes[-2:]
	anho=request_GET(request,camyear)
	if anho and int(mes) and int(dia):
		camtot=str(anho)+'-'+mes+'-'+dia
	else:
		camtot=''    
	return camtot 

def convert_date(x,y,z):
    orig_date = datetime.datetime.date(x,y,z)
    orig_date = str(orig_date)
    d = datetime.strptime(orig_date,"%Y-%m-%d")
    d = d.strftime('%Y-%m-%d')
    return d


class IntervencionUpdateView(UpdateView):
# pasar una derivacion a lista de espera
	model=Ficha_derivacion
	second_model=Estudiante
	
	fields = ["pasada","derivado"]
	template_name = 'derivacion/pasada_intervencion_centro.html'
	success_url = reverse_lazy('sesion:intervenidos_listar')
	
	def get_context_data(self,**kwargs):
		context=super(IntervencionUpdateView,self).get_context_data(**kwargs)
		return context

	def post(self,request,*args,**kwargs):
	
		id_ficha = kwargs['pk']
		ficha_derivacion = self.model.objects.get(id=id_ficha)
		estudiante = self.second_model.objects.get(id=ficha_derivacion.Estudiante_id)
		x=ficha_derivacion.fecha_derivacion
		fecha_derivacion=x
		
		print ("Fecha y hora = %s" % x)
		print ("Fecha y hora en formato ISO = %s" % x.isoformat() )
		print (u"Año = %s" %x.year)
		print ("Mes = %s" %x.month)
		print ("Dia =  %s" %x.day)
		print ("Formato dd/mm/yyyy =  %s/%s/%s" % (x.day, x.month, x.year) )
		
		
		d=x.day
		m=x.month
		y=x.year
		if d <= 9:
			d='0'+str(d)
			print d
		if m <= 9:
			m='0'+str(m)
		
			  
		#fecha_derivacion=request_GET_D(fecha_derivacion)
		#print fecha_derivacion
		#fecha_derivacion=convert_date(y,m,d)
		
		per=ficha_derivacion.usuario.first_name
		per=per+' '+ficha_derivacion.usuario.last_name
		
	
        # Llamamos ala superclase
		object = super(IntervencionUpdateView, self).get_object()
		
        # Grabamos el valor 2 que es lidta de espera
		object.pasada = 3 # porque 3 significa que inicia intervencion
		object.derivado = 2 # porque esta en intervencion en el centro

		object.save()
		fecha_1 = datetime.datetime.now()
		#fecha_1=request_GET_D(request,ahora)
		

		Intervenidos.objects.create(Estudiante=estudiante, fecha_intervencion=fecha_1,estado='Incio de la intervención', sintesis='Inicio en el centro',usuario=self.request.user,fecha_derivacion='2018-02-02',Profesional=per,dia=d,mes=m,anno=y)
		#crea el estado de un estuddiante con el fin de verlo ene fituto y saber en que estado esta
		Estado.objects.create(Estudiante=estudiante, Estado='Evaluación',fecha_estado=fecha_1)
		intervenido=Intervenidos.objects.get(Estudiante=estudiante)
		Pasos_intervencion.objects.create(Intervenidos=intervenido, usuario=self.request.user,fecha_pasos=fecha_1)

        # Retornamos el objeto
        #return object
		return HttpResponseRedirect('/sesion/intervenido')
		#return HttpResponseRedirect(self.get_success_url())
	        
		
class DerivaciUpdateView(UpdateView):
# pasar una derivacion a lista de espera
	queryset = Ficha_derivacion.objects.all()
	fields = ["pasada","derivado"]
	template_name = 'derivacion/pasada_lista_espera.html'
    #success_url = reverse_lazy('derivacion:centro_listar')
	def get_object(self):
        # Llamamos ala superclase
		object = super(DerivaciUpdateView, self).get_object()
        # Grabamos el valor 2 que es lidta de espera
		object.pasada = 3 # porque 2 significa que esta en lista de espera
		object.derivado = 2 # porque 3 significa que ya paso por la revison del centro

		object.save()
        # Retornamos el objeto
        #return object
        
	def get_success_url(self):
		#return reverse("derivacion:centro_listar")
		#success_url = reverse_lazy('derivacion:centro_listar')
		success_url = '/'
#Retornar a un estudiante a la dupla

#Retornar a un estudiante a la dupla
# Este retorno sera para las fichas con informacion incompleta
def RetornoUpdateView(request,pk):
# Realizar un retorno de una ficha de derivacion a la dupla 
	
	dato = get_object_or_404(Estudiante, pk=pk)
	
	ficha_derivacion=Ficha_derivacion.objects.get(Estudiante_id=pk,estado=1)
	
	ficha_id=ficha_derivacion.id
	
	if request.method=='POST':
		formulario = RetornoFaltainfoForm(request.POST,request.FILES)
 		if formulario.is_valid():
 			instance = formulario.save(commit=False)
			instance.Ficha_derivacion=ficha_derivacion
			instance.fecha_retorno=datetime.datetime.now()
			instance.motivo_termino=0
			instance.Red_apoyo=Red_apoyo.objects.get(nombre='No es derivado a otra institución')
			instance.save()
			ficha_derivacion.pasada=5
			ficha_derivacion.derivado=2
			ficha_derivacion.save()

			#infoarchivo2 = Ficha_derivacion.objects.get(id = ficha_id)
			#infoarchivo2.pasada= 5 #porque pasa a otra institucion
			#infoarchivo2.derivado = 2 # porque ya fue vista por el centro
			#infoarchivo2.estado = 1 # porque aun sigue activa dentro del centro 
			#infoarchivo2.save()

			return redirect('derivacion:centro_listar')
			return HttpResponseRedirect('/derivacion/centro_listar')
			
	else:
		formulario = RetornoFaltainfoForm()

	context = {
		"formulario": formulario,
		"dato": dato,
		"ficha":ficha_derivacion,
		 }
	return render(request, 'derivacion/pasada_retorno_falta_info.html', context)	

# Este retorno sera desde el centro realizado por el Psicologo del centro
# y sera diferente al de retorno por falta de informacion que es el que hace la fucnion anterior
def RetornoDefinitivo(request,pk):
# Realizar un retorno de una ficha de derivacion a la dupla 
	
	dato = get_object_or_404(Estudiante, pk=pk)

	ficha_derivacion=Ficha_derivacion.objects.get(Estudiante_id=dato,estado=1)

	ficha_id=ficha_derivacion.id

	
	if request.method=='POST':
		formulario = MotivoRetornoForm(request.POST,request.FILES)
 		if formulario.is_valid():
 			instance = formulario.save(commit=False)
 			if instance.docfile1 !=  None:
 				instance.docfile1=request.FILES['docfile1']
 			if instance.docfile2 !=  None:
 				instance.docfile2=request.FILES['docfile2']
 			if instance.docfile3 !=  None:
 				instance.docfile3=request.FILES['docfile3']
			instance.Ficha_derivacion=ficha_derivacion
			instance.fecha_retorno=datetime.datetime.now()
			instance.save()
			
			infoarchivo2 = Ficha_derivacion.objects.get(id = ficha_id)
			infoarchivo2.pasada= 4 #porque pasa a otra institucion, si una ficha pasa a otra institucion 
			#automaticamente queda en la lista de los podibles egresados ya que se va del centro

			infoarchivo2.derivado = 2 # porque ya fue vista por el centro
			infoarchivo2.estado = 1 # porque aun sigue estando activa dentro del centro
			infoarchivo2.save()
			#inter=Intervenidos.objects.get(Estudiante=dato)
			#inter.activo=2
			#inter.save()


			return HttpResponseRedirect('/derivacion/intervencion_otrar')
	else:
		formulario = MotivoRetornoForm()

	context = {
		"formulario": formulario,
		"dato": dato,
		"ficha":ficha_derivacion,
		 }
	return render(request, 'derivacion/pasada_retorno.html', context)	


# Modificar una derivacion a otra institucion 
# Realizado el viernes 4 de mayo por error capacitacion de dani
def ModificarRetornoDefinitivo(request,ficha,pk):
# Realizar un retorno de una ficha de derivacion a la dupla 
	
	dato = get_object_or_404(Estudiante, pk=pk)
	Ficha=Ficha_derivacion.objects.get(id=ficha)
	retorno_ficha=Motivo_Retorno_Ficha_derivacion.objects.get(Ficha_derivacion=Ficha)
	
	if request.method == 'POST':
		formulario = MotivoRetornoForm(instance=retorno_ficha)
	else:
		formulario = MotivoRetornoForm(instance=retorno_ficha)
		if formulario.is_valid():
			formulario.save()

			
		
			return HttpResponseRedirect('/derivacion/intervencion_otrar')


	context = {
		"formulario": formulario,
		"dato": dato,
		"ficha":Ficha,
		 }
	return render(request, 'derivacion/pasada_retorno_modificar.html', context)	



# salir de la lista de espera
class SalirEsperaUpdateView(UpdateView):
# pasar una derivacion a lista de espera
	queryset = Ficha_derivacion.objects.all()
	fields = ["pasada","derivado"]
	template_name = 'derivacion/pasada_lista_espera.html'
    #success_url = reverse_lazy('derivacion:centro_listar')
	def get_object(self):
        # Llamamos ala superclase
		object = super(SalirEsperaUpdateView, self).get_object()
        # Grabamos el valor 2 que es lidta de espera
		object.pasada = 1 # porque 2 significa que esta en lista de espera
		object.derivado = 2 # porque 3 significa que ya paso por la revison del centro

		object.save()
        # Retornamos el objeto
        #return object
        

	def get_success_url(self):
		#return reverse("derivacion:centro_listar")
		#success_url = reverse_lazy('derivacion:centro_listar')
		success_url = '/'

		
#enviar una derivacion al centro
# Proceso de envio de cada una de las derivaciones
class DerivadoUpdateView(UpdateView):
# pasar una derivacion a lista de espera
	
	model=Ficha_derivacion
	fields = ["derivado","pasada"]
	template_name = 'derivacion/pasada_centro.html'
	success_url=reverse_lazy('derivacion:derivacion_listar')

	def get_context_data(self,**kwargs):
		context=super(DerivadoUpdateView,self).get_context_data(**kwargs)
		return context
	def post(self,request,*args,**kwargs):
        # Llamamos ala superclase
		self.object=self.get_object
		object = super(DerivadoUpdateView, self).get_object()
        # Grabamos el valor 2 que es la forma de decirle a centro que entro una derivacion
		object.derivado = 2 # porque 2 significa que ya es la primera vez que se deriva
		if object.pasada == 5:
			object.pasada = 1 # porque 2 significa que ya es la primera vez que se deriva
		object.save()
        # Retornamos el objeto
        #return object
		#return HttpResponseRedirect(self.get_success_url())
		return HttpResponseRedirect('/derivacion/gracias/')


# hotoria de un estudiante dentro del centro de bienestar
def historia(request, id_estudiante):
	estudiante = Estudiante.objects.get(id=id_estudiante)
	
	ficha=Ficha_derivacion.objects.get(Estudiante__id=id_estudiante,estado=1)
	

	try:
 			 # try something
 		retorno=Motivo_Retorno_Ficha_derivacion.objects.filter(Estudiante__id=id_estudiante)
 		
 		
	except Motivo_Retorno_Ficha_derivacion.DoesNotExist:
			  # do something
		retorno=None		


	intervenido=Intervenidos.objects.get(Estudiante__id=id_estudiante)

	try:
		pasos=Pasos_intervencion.objects.filter(Intervenidos=intervenido)

	except Pasos_intervencion.DoesNotExist:
		pasos=None	
	#print pasos
	try:
		estado=Estado.objects.filter(Estudiante__id=id_estudiante)
	
	except Estado.DoesNotExist:
		estado=None
	try:
		objetivos=objetivo_intervencion.objects.filter(Estudiante__id=id_estudiante,activo=1)		
	except objetivo_intervencion.DoesNotExist:
		objetivo=None
		
	try:
		viejos=objetivo_intervencionhistoria.objects.filter(Estudiante__id=id_estudiante)	
	except objetivo_intervencionhistoria.DoesNotExist:
		viejos=None
			
	#print viejos
	
	context = {
		"nino": estudiante,
		"ficha": ficha,
		"retorno":retorno,
		"intervenido":intervenido,
		"pasos":Pasos_intervencion,
		"estado":estado,
		"objetivos":objetivos,
		"viejos":viejos,


		 }
	return render(request, 'derivacion/pasada_retorno.html', context)		 

#Ver a todos los intervenidos 
class ReporteIntervenidos(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion
	template_name = 'derivacion/reporte_entradas_totales.html'
	paginate_by = 10
#muestra a todas las derivaciones realizadas   
	
	
	def get_context_data(self, **kwargs):
		
		context = super(ReporteIntervenidos, self).get_context_data(**kwargs)
		try:
			intervenido = Intervenidos.objects.filter(usuario=self.request.user)
		except Intervenidos.DoesNotExist:
			intervenido=None
		
		diccionario=[]
		
		if intervenido:
			for intervencion in intervenido:
				dato=intervencion.Estudiante
				#print 'intervenido', dato
				try:
					ficha=Ficha_derivacion.objects.get(Estudiante=dato,estado=1,usuario=self.request.user)
				except Ficha_derivacion.DoesNotExist:
					ficha=None
				estado=intervencion.estado
				try:
					sesion_est=sesion.objects.filter(Estudiante=dato)
					
					ultimo=sesion_est.latest('numero')
								
					apoderado=0
					dupla=0
					pie=0
					profesores=0

					for asistido in sesion_est:
						
						if asistido.participantes == 1 or asistido.participantes == 9:
							apoderado=apoderado+1
						if asistido.participantes == 10:
							dupla=dupla+1
						if asistido.participantes == 11:
							pie=pie+1
						if asistido.participantes == 12:
							profesores=profesores+1
					insubid = {
					        "estudiante" : dato, 
					        "estado" : estado,
					        "ultimo" : ultimo.numero,
					        "apoderado" : apoderado,
					        "dupla" : dupla,
					        "pie" : pie,
					        "profesores" :profesores,
					        

					    }
					diccionario.append(insubid)		

							
		    		
				except sesion.DoesNotExist:
					ultimo=0
					apoderado=0
					dupla=0
					pie=0
					profesores=0


		
					

		


			

		context['intervenido'] = intervenido
		context['ficha'] = ficha
		context['diccionario'] = diccionario


		return context	

# Ver todos los intervenidos por el supervisor 
#Ver a todos los intervenidos 
class ReporteIntervenidosSupervisor(ListView):
        '''listar todos los estudiantes intervenidos'''
	model = Ficha_derivacion
	template_name = 'derivacion/reporte_entradas_totales_supervisor.html'
	paginate_by = 100
#muestra a todas las derivaciones realizadas   
	
	
	def get_context_data(self, **kwargs):
		
		context = super(ReporteIntervenidosSupervisor, self).get_context_data(**kwargs)
		try:
			intervenido = Intervenidos.objects.filter(usuario=self.request.user)
		except Intervenidos.DoesNotExist:
			intervenido=None
		
		diccionario=[]
		
		
		for intervencion in intervenido:
			dato=intervencion.Estudiante
			
			try:
				ficha=Ficha_derivacion.objects.get(Estudiante=dato,estado=1,usuario=self.request.user)
			except Ficha_derivacion.DoesNotExist:
				ficha=None
			estado=intervencion.estado
			try:
				sesion_est=sesion.objects.filter(Estudiante=dato)
				
				ultimo=sesion_est.latest('numero')
							
				apoderado=0
				dupla=0
				pie=0
				profesores=0

				for asistido in sesion_est:
					
					if asistido.participantes == 1 or asistido.participantes == 9:
						apoderado=apoderado+1
					if asistido.participantes == 10:
						dupla=dupla+1
					if asistido.participantes == 11:
						pie=pie+1
					if asistido.participantes == 12:
						profesores=profesores+1
				insubid = {
				        "estudiante" : dato, 
				        "estado" : estado,
				        "ultimo" : ultimo.numero,
				        "apoderado" : apoderado,
				        "dupla" : dupla,
				        "pie" : pie,
				        "profesores" :profesores,
				        

				    }
				diccionario.append(insubid)		

							
		    		
			except sesion.DoesNotExist:
				ultimo=0
				apoderado=0
				dupla=0
				pie=0
				profesores=0

		context['intervenido'] = intervenido
		context['ficha'] = ficha
		context['diccionario'] = diccionario


		return context	








def search(request):

    # si no es una peticion ajax, devolvemos error 400
    if not request.is_ajax() or request.method != "POST":
        return HttpResponseBadRequest()

    # definimos el termino de busqueda
    q = request.POST['q']

    #verificamos si el termino de busqueda es un documento de identidad
    match = re.match(r'^(?P<CI>[0-9]{2,})$', q)
    isCI = (False, True)[match != None]

    # generamos la query
    if isCI:
        users = User.objects.filter(CI=match.groupdict()['CI'])
    else:
        users = User.objects.filter(username__contains=q)

    # seleccionamos las columnas que deseamos obtener para el json
    user_fields = (
        'username',
        'email',
        'CI'
    )

    # to json!
    data = serializers.serialize('json', users, fields=user_fields)

    # eso es todo por hoy ^^
    return HttpResponse(data, content_type="application/json")


class PDFPrueba(View):
    	"""Regresa pdf desde template"""
	def get(self, request, *args, **kwargs):
		datos={
    			"nombre":"Hector",
    			"apellidos":"Rojas",
    			"edad":"44",


		}
		pdf=render_pdf("derivacion/mi_pdf.html",{"datos":datos})	
		return HttpResponse(pdf, content_type="applications/pdf")
    		