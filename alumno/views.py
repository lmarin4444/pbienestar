# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.http import Http404
from alumno.models import establecimiento,curso,Familia,EscolaridadAnterior
from alumno.models import Estudiante,Escolaridad
from alumno.models import Parentesco,apoderado,hermano
from sesion.models import objetivo_intervencion,Diagnostico,Intervenidos
from sesion.forms import DiagnosticoForm
from profesional.models import Profesional,Cargo
#from alumno.models import Pariente,tutor
from alumno.forms import EstablecimientoForm,EstudianteForm,ParentescoForm,ApoderadoForm,HermanoForm, \
EstudianteVerForm,EstudianteFormVersinrut,EscolaridadForm,EscolaridadActualizaForm,EscolaridadActualizaFormCentro, \
EstudianteFormUpdate,EstudianteNombresForm

from dupla.models import Intervencion_casos,Ficha_derivacion_dupla
from derivacion.models import Ficha_derivacion
from django.contrib.auth.decorators import login_required
#para los permisos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.views import generic

import json
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
#para la paguinacion 
from django.core.paginator import Paginator
from secretaria.models import Confirma
import datetime
from django.urls import reverse
from django.template import RequestContext
from itertools import cycle
from django.core.exceptions import ValidationError
from django.db.models import Q
#nos permite paguinar cuando se usan funciones y no vistas basadas en clases
def Paginate(request, queryset, pages):
    """
    PARAMETROS:
    request: Request de la vista
    queryset: Queryset a utilizar en la paginación
    pages: Cantidad de paginas del paginador
    """
    # Retorna el objeto paginator para comenzar el trabajo
    result_list = Paginator(queryset, pages)
 
    try:
        # Tomamos el valor de parametro page, usando GET
        page = int(request.GET.get('page'))
    except:
        page = 1
 
    # Si es menor o igual a 0 igualo en 1
    if page <= 0:
        page = 1
 
    # Si viene un parámetro que es mayor a la cantidad
    # de paginas le igualo el parámetro con las cant de paginas
    if(page > result_list.num_pages):
        page = result_list.num_pages
 
    # Verificamos si esta dentro del rango
    if (result_list.num_pages >= page):
        # Obtengo el listado correspondiente al page
        pagina = result_list.page(page)
 
        context = {
            'queryset': pagina.object_list,
            'page': page,
            'pages': result_list.num_pages,
            'has_next': pagina.has_next(),
            'has_prev': pagina.has_previous(),
            'next_page': page+1,
            'prev_page': page-1,
            'firstPage': 1,
        }
 
    return context

		

def ver_familia(request,pk):
	
	estudiante = Estudiante.objects.get(id=pk)
	colegio=Escolaridad.objects.get(Estudiante__id=pk)

	
	family=estudiante.Familia
	familia=Parentesco.objects.filter(Familia=family)

	#pag = Paginate(request, familia , 3)
	
	contexto = {
	'estudiante':estudiante,
	'familia':familia,
	'colegio':colegio,
	

	}

	return render(request, 'alumno/ver_familia.html', contexto)


def ver_familia_supervisor(request,pk):
	
	estudiante = Estudiante.objects.get(id=pk)
	colegio=Escolaridad.objects.get(Estudiante__id=pk)

	
	family=estudiante.Familia
	familia=Parentesco.objects.filter(Familia=family)

	#pag = Paginate(request, familia , 3)
	
	contexto = {
	'estudiante':estudiante,
	'familia':familia,
	'colegio':colegio,
	

	}

	return render(request, 'alumno/ver_familia_supervisor.html', contexto)




def buscar_familia(request):
	if request.is_ajax:
		termino=request.GET.get('term','')
		pariente=Parentesco.objects.filter(Estudiante__id=termino)
		
		data=serializers.serialize('json',pariente,fields=('nombre','apellido_p','apellido_m','parentesco'))
		
	else:
		data='No hay familia'
	return HttpResponse(data,content_type='application/json')

#Muestra si el estudiante esta previamente en el centro 
def ver_estudiante_rut(request):
	
	try:
		estudiante = Estudiante.objects.get(id=pk)

	except Estudiante.DoesNotExist:
		estudiante=None
	
	

	if request.method == 'POST':
		if estudiante == None:
			formulario= EstudianteVerForm
			formulario_rut=EstudianteFormVersinrut	

		else:
				
			formulario = EstudianteVerForm(request.POST or None, instance=pk)
			formulario_rut=EstudianteFormVersinrut(request.POST or None, instance=estudiante)
		if formulario.is_valid() and formulario_rut.is_valid():
				rut = formulario.instance
				solicitud.Estudiante = formulario_rut.save(commit=False)
				solicitud.Estudiante.rut=rut
				solicitud.save()
				return HttpResponseRedirect(self.get_success_url())
		else:
				return self.render_to_response(self.get_context_data(formulario=formulario, formulario_rut=formulario_rut))

		

				
	else:
		formulario= EstudianteVerForm
		formulario_rut=EstudianteFormVersinrut	
	
	
    #book_id=get_object_or_404(Book, pk=pk)
    
	return render(
	request,
        	'alumno/estudiante_rut.html',
        	context={'formulario':formulario,
        			'formulario_rut':formulario_rut,

        		'estudiante':estudiante_id,

        		 'mensaje':mensaje,
        		 
        		 
	})
	


#para traer a un estudiante
class EstudianteDetailView(DetailView):
    model = Estudiante 
    template_name = 'alumno/certificado.html'
   
def get_context_data(self, **kwargs):
        context = super(EstudianteDetailView, self).get_context_data(**kwargs)
       
        return context
# mostrar la familia de un estudiante dentro de una ficha de derivacion 

class FamiliaListView(ListView):
	"""docstring for FamiliaListView"""
	template_name='alumno/ver_ficha.html'
	model=Estudiante
def get(self, request,*args,**kwargs):
	name=request.GET['name']
	listado_estudiante=Parentesco.objects.get(Estudiante=name).order_by('id')
	familia=listado_estudiante.Parentesco.all()
	data=serializers.serialize('json',familia,fields=('nombre','apellido_p','apellido_m','parentesco'))
	return HttpResponse(data,content_type='application/json')
	
	
#para traer la ficha de un  estudiante desde la dupla
def FichaDetailView(request,pk):
	try:
		estudiante_id=Estudiante.objects.get(pk=pk)
		family=estudiante_id.Familia
		
		ficha_id=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
		
		parentesco_id=Parentesco.objects.filter(Familia=family).order_by('id')
		
		apoderado_id=apoderado.objects.filter(Familia=family)
		
	except Estudiante.DoesNotExist:
		raise Http404("Estudiante does not exist")

    #book_id=get_object_or_404(Book, pk=pk)
    
	return render(
	request,
	'alumno/ver_ficha.html',
	context={'estudiante':estudiante_id,
			'ficha':ficha_id,
			'parentesco':parentesco_id,
			'apoderado':apoderado_id, }
    )

# para ver ficha desde el centro 

def FichaCentroDetailView(request,pk):
	try:
		estudiante_id=Estudiante.objects.get(pk=pk)
		family=estudiante_id.Familia
		try:
			ficha_id=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
		except Ficha_derivacion.DoesNotExist:
			ficha_id=None
		
		
		try:
			parentesco_id=Parentesco.objects.filter(Familia=family).order_by('id')
		except Parentesco.DoesNotExist:
			parentesco_id=None
		
		try:
			apoderado_id=apoderado.objects.filter(Familia=family)
		except apoderado.DoesNotExist:
			apoderado_id=None
		
		

	except Estudiante.DoesNotExist:
		raise Http404("Estudiante does not exist")

    #book_id=get_object_or_404(Book, pk=pk)
    
	return render(
	request,
	'alumno/ver_ficha_centro.html',
	context={'estudiante':estudiante_id,
			'ficha':ficha_id,
			'parentesco':parentesco_id,
			'apoderado':apoderado_id, }
    )



#Ficha de un estudiante desde la dupla
def FichaEstudianteDetailView(request,pk):

	try:
		estudiante_id=Estudiante.objects.get(pk=pk)
		family=estudiante_id.Familia
		colegio=Escolaridad.objects.get(Estudiante__id=pk)
		
	except Estudiante.DoesNotExist:
		estudiante_id=None
	try:
		ficha_id=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
	except Ficha_derivacion.DoesNotExist:
		ficha_id=None		
		
	try:
		parentesco_id=Parentesco.objects.filter(Familia=family).order_by('id')
	except Parentesco.DoesNotExist:
		parentesco_id=None

	try:
		apoderado_id=apoderado.objects.filter(Familia=family)
        

	except apoderado.DoesNotExist:
		apoderado_id=None

		

    #book_id=get_object_or_404(Book, pk=pk)
	return render(
        request,
        'alumno/ver_grupo.html',
        context={'estudiante':estudiante_id,
        		 'ficha':ficha_id,
        		 'parentesco':parentesco_id,
        		 'apoderado':apoderado_id,
        		 'colegio':colegio	}
    )


#Ficha de un estudiante desde la dupla
def FichaEstudianteDetailView_supervisor(request,pk):

	try:
		estudiante_id=Estudiante.objects.get(pk=pk)
		family=estudiante_id.Familia
		colegio=Escolaridad.objects.get(Estudiante__id=pk)
		
	except Estudiante.DoesNotExist:
		estudiante_id=None
	try:
		ficha_id=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
	except Ficha_derivacion.DoesNotExist:
		ficha_id=None		
		
	try:
		parentesco_id=Parentesco.objects.filter(Familia=family).order_by('id')
	except Parentesco.DoesNotExist:
		parentesco_id=None

	try:
		apoderado_id=apoderado.objects.filter(Familia=family)
        

	except apoderado.DoesNotExist:
		apoderado_id=None

		

    #book_id=get_object_or_404(Book, pk=pk)
	return render(
        request,
        'alumno/ver_grupo_supervisor.html',
        context={'estudiante':estudiante_id,
        		 'ficha':ficha_id,
        		 'parentesco':parentesco_id,
        		 'apoderado':apoderado_id,
        		 'colegio':colegio	}
    )


def Reportedecaso(request,pk):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	ficha_id=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
	mensaje=""
	try:
		intervencion=Intervenidos.objects.get(Estudiante__id=pk)
		yo=intervencion.usuario
	except Intervenidos.DoesNotExist:
		intervencion=""
		yo=""
	try:
		evaluar=Diagnostico.objects.get(Estudiante__id=pk)
		mensaje="Estudiante ya cuenta con un informe de evaluación"
		
			
	except Diagnostico.DoesNotExist:
		evaluar=""
		form = DiagnosticoForm()

	try:
		#obje= get_object_or_404(objetivo_intervencion, Estudiante__id=pk)

		obje= objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
        #evaluacion=Diagnostico.objects.get(Estudiante__id=pk)
        #obj_id=objetivo_intervencion.objects.filter(Estudiante__id=pk)
	
	
		
		form = DiagnosticoForm(instance=evaluar or None)
		if request.method == 'POST':
			form = DiagnosticoForm(request.POST)
	        #codigo
	        if form.is_valid():
				instance = form.save(commit=False)
				x = datetime.date.today()
				instance.fecha=x
				instance.Estudiante=estudiante_id
				instance.usuario=request.user
				instance.save()
				return redirect('derivacion:intervencion_listar')
        	
	
	except objetivo_intervencion.DoesNotExist:
		mensaje="Estudiante sin asignación de objetivo"
		form = DiagnosticoForm(request.POST or None)
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
	
					
	return render(
        request,
        'alumno/reporte_caso.html',
        context={'formulario':form,
        		'estudiante':estudiante_id,
        		 'ficha':ficha_id,
        		 'objetivo':obje,
        		 'mensaje':mensaje,
        		 'valor':valor,
        		 'yo':yo,

	})


def ReportedecasoModificar(request,pk):

	estudiante_id=Estudiante.objects.get(pk=pk)
	ficha_id=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
	mensaje=""
	try:
		intervencion=Intervenidos.objects.get(Estudiante__id=pk)
		yo=intervencion.usuario
	except Intervenidos.DoesNotExist:
		intervencion=""
		yo=""
	try:
		evaluar=Diagnostico.objects.get(Estudiante__id=pk)
		mensaje="Estudiante cuenta con un informe de evaluación"
		form = DiagnosticoForm(request.POST or None, instance=evaluar)
		
			
	except Diagnostico.DoesNotExist:
		evaluar=""
		mensaje="No cuenta con informe de evaluación"
		form = DiagnosticoForm()

	try:
		#obje= get_object_or_404(objetivo_intervencion, Estudiante__id=pk)

		obje= objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
        #evaluacion=Diagnostico.objects.get(Estudiante__id=pk)
        #obj_id=objetivo_intervencion.objects.filter(Estudiante__id=pk)
		
	
	
		# if request is not post, initialize an empty form
		#form = form_class(request.POST or None) # Maybe Not 
		
		if request.method == 'POST':
			instance = DiagnosticoForm(request.POST)
			
	        #codigo
			if form.is_valid():
				
				instance = form.save(commit=False)
				instance.Estudiante=estudiante_id
				instance.usuario=request.user
				instance.save()
				#instance.save()
				return redirect('derivacion:modificar_informes')
		
		
        	
	
	except objetivo_intervencion.DoesNotExist:
		mensaje="Estudiante sin asignación de objetivo"
		form = DiagnosticoForm(request.POST or None)
		obje=""

    #Enviar un valor pasa saber si la persona que esta activa es la misma que hiso el informe
    # si valor es 0 el usuario que hiso el informe es el mismo que esta actualmente si el 1 no es el mismo
    
	if evaluar:
		valor=0
		mensaje ="Modificar informe"

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
	
					
	return render(
        request,
        'alumno/reporte_caso.html',
        context={'formulario':form,
        		'estudiante':estudiante_id,
        		 'ficha':ficha_id,
        		 'objetivo':obje,
        		 'mensaje':mensaje,
        		 'valor':valor,
        		 'yo':yo,

	})




class GrupoDetailView(DetailView):
    model = Parentesco
    template_name = 'alumno/ver_grupo.html'
	
def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
	context = super(GrupoDetailView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
	context['some_data'] = 'Esta es la información que necesito'
	return context
    
#def detail_ficha(request, pk):
#	Ficha = Ficha_derivacion.objects.get(Estudiante_id=pk)#
#	context = {'object':Ficha}
#	return render(request, 'alumno/ver_ficha.html', context)



#para traer a un estudiante
class AsistenciaDetailView(DetailView):
    model = Estudiante 
    template_name = 'alumno/certificado.html'
    

def get_context_data(self, **kwargs):
        context = super(AsistenciaDetailView, self).get_context_data(**kwargs)
        context['certifica'] = Estudiantes.nombres
        return context

# Create your views here.
def escuela(request):
	colegios= establecimiento.objects.exclude(Rbd=1)
	context={'colegios':colegios}

	return render(request, 'alumno/establecimiento.html', context)

def cabros(request):
	ninnos= Estudiante.objects.all()
	context={'ninnos':ninnos}


	return render(request, 'alumno/pupilo.html', context)	

def certifica(request, ):
	mascota = Estudiante.objects.get(id=id_Estudiante)
	if request.method == 'POST':
		form = MascotaRAForm(instance=mascota)
	else:
		form = MascotaRaForm(request.POST, instance=mascota)
		if form.is_valid():
			form.save()
		return redirect('secretaria:secretaria_listar')
	return render(request, 'secretaria/mascotara_form.html', {'form':form})

#Views las fichas de derivacion 

class EstudianteList(ListView):
	model =Estudiante
	template_name = 'alumno/estudiante_list.html'
	paginate_by = 100

	def get_queryset(self, *args, **kwargs):
		return Ficha_derivacion.objects.filter(usuario=self.request.user,estado=1)
	#def get_queryset(self, *args, **kwargs):
	#	return Ficha_derivacion.objects.filter(usuario=self.request.user,pasada=3)

#Listado de fichas de un profesional pie

class EstudianteListpie(ListView):
	model =Estudiante
	template_name = 'alumno/estudiante_list.html'
	paginate_by = 100

	def get_queryset(self, *args, **kwargs):
		return Ficha_derivacion.objects.filter(usuario=self.request.user,estado=1,pie='True')
	#def get_queryset(self, *args, **kwargs):
	#	return Ficha_derivacion.objects.filter(usuario=self.request.user,pasada=3)




#Mustra a todos los estudiantes ingresados por mi 

class EstudianteListEstablecimiento(ListView):
	model =Ficha_derivacion
	template_name = 'alumno/estudiante_list_establecimiento.html'

	def get_context_data(self, **kwargs):
	        # Llamamos ala implementacion primero del  context
			context = super(EstudianteListEstablecimiento, self).get_context_data(**kwargs)
			indice = self.kwargs.get('pk') # El mismo nombre que en tu URL
			print indice
			escuela=establecimiento.objects.get(pk=indice)
			print escuela
			try: 
				fichas=Ficha_derivacion.objects.filter(Q(estado=1) & Q(Estudiante__curso__establecimiento__nombre=escuela))
			except Ficha_derivacion.DoesNotExist:
				fichas=None
			context['fichas']=fichas
			return context
			
#Mustra a todos los estudiantes en el centro de binestar de un colegio en especial 

# ver familia de un estudiante
class FamiliaList(ListView):
	model = Estudiante
	template_name = 'alumno/ver_familia.html'
	paginate_by = 6

	def get_queryset(self, *args, **kwargs):
		#context = super(FamiliaList, self).get_context_data(**kwargs)
		queryset = super(FamiliaList, self).get_queryset()
		return queryset.filter(id='id')



#def get_queryset(self):
#        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class ConfirmacionList(ListView):
	model = Confirma
	template_name = 'alumno/confirma_estudiantes.html'
	paginate_by = 6

	def get_context_data(self,**kwargs):
        # Llamamos ala superclase
		context=super(ConfirmacionList,self).get_context_data(**kwargs)
		return context

class EstudianteDList(ListView):
	model = Ficha_derivacion
	template_name = 'alumno/estudiante_list.html'
	paginate_by = 6

class CertificadosList(ListView):
	model = Intervenidos
	template_name = 'alumno/certificados_estudiantes.html'
	paginate_by = 6

class CertificadosListCentro(ListView):
	model = Estudiante
	template_name = 'alumno/certificados_estudiantes.html'
	paginate_by = 6

class CertificadosAsistenciaList(ListView):
	model = Estudiante
	template_name = 'alumno/certificados_asistencia.html'
	paginate_by = 6	

class EstudianteCreate(CreateView):
	model = Estudiante
	form_class = EstudianteForm
	template_name = 'alumno/estudiante_form.html'
	success_url = reverse_lazy('alumno:profesinal_establecimiento_listar')


def EstudianteUpdate(request,pk,escuela):
#Realizar la modificación  de los datos de un estudiante
	
	dato = get_object_or_404(Estudiante, pk=pk)
	colegio = establecimiento.objects.get(pk=escuela)
	form = EstudianteFormVersinrut(instance=dato)


	if request.method=='POST':

		form = EstudianteFormVersinrut(request.POST,instance=dato)
		
 		if form.is_valid():
 			
 			instance = form.save(commit=False)
 			
			edad_formulario=instance.fecha_nacimiento
		
			diff = (datetime.date.today() - edad_formulario).days

			years = str(int(diff/365))	
			instance.edad=years
			instance.curso=dato.curso
			instance.rut=dato.rut
			instance.Familia=dato.Familia
			instance.save()

			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk':colegio.id })
			return HttpResponseRedirect(url)

	
		

	context = {
		"form": form,
		"dato": dato,
		"colegio": colegio,

		
		 }
	return render(request, 'alumno/estudiante_form_modificar.html', context)




class EstudianteDelete(DeleteView):
	model = Estudiante
	template_name = 'alumno/estudiante_delete.html'


	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(EstudianteDelete, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=Estudiante.objects.get(id=pk)

		context['estudiante']=estudiante
		return context




	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		

		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=Estudiante.objects.get(id=pk)
		escuela=estudiante.curso.establecimiento
	# Buscar la familia 
		family=estudiante.Familia

		
		sifamilia=Estudiante.objects.filter(Familia=family)
		cont=0
		for tengo_familia in sifamilia:
			cont=cont+1




		if cont > 1 :
			mensaje="La familia del estudiante no es borrada "
			# Retornamos el objeto
			estudiante.delete()
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url) 	
		else:
			parienetes=Parentesco.objects.filter(Familia=family)
			parienetes.delete()
			family.delete()
			estudiante.delete()
			# Retornamos el objeto
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)


		
	
class ParentescoList(ListView):
	model = Parentesco
	template_name = 'alumno/parentesco_list.html'
	
	def get_queryset(self, *args, **kwargs):
		#context = super(FamiliaList, self).get_context_data(**kwargs)
		queryset = super(ParentescoList, self).get_queryset()
		#return queryset.filter(id='id')
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ParentescoList, self).get_context_data(**kwargs)
		dato = Estudiante.objects.all()
		context['dato'] = dato
		return context


class asignar_familia(ListView):
	model = Parentesco
	template_name = 'alumno/parentesco_list_asignarfamilia.html'
	

	def get_queryset(self, *args, **kwargs):
		#context = super(FamiliaList, self).get_context_data(**kwargs)
		queryset = super(asignar_familia, self).get_queryset()
		#return queryset.filter(id='id')
		return queryset

	def get_context_data(self, **kwargs):
		context = super(asignar_familia, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		dato = Estudiante.objects.all()
		estudiante= Estudiante.objects.get(id=pk)
		context['dato'] = dato
		context['estudiante'] = estudiante
		return context
	
def agregar_familia(request,pk,familia):
	
	if request.method== 'GET':
		estudiante=Estudiante.objects.get(id=pk)
		family=Familia.objects.get(id=familia)
		estudiante.Familia=family	
		estudiante.save()
		
			
		#url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': estudiante.curso.establecimiento.id})
		#return HttpResponseRedirect('/alumno/parentescolistarest/')
		context={'estudiante':estudiante,}
		return render(request,'alumno/estudiante_asignado.html',context)
	
class ParentescoCreate(CreateView):

	model = Parentesco
	form_class = ParentescoForm
	template_name = 'alumno/parentesco_form.html'
	success_url = reverse_lazy('alumno:parentesco_listar')
    
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(ParentescoCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		context['dato']=Estudiante.objects.get(id=pk)
		return context

	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			solicitud = form.save(commit=False)
			solicitud.curso = 0
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			estudiante=Estudiante.objects.get(id=pk)
			family=estudiante.Familia

			solicitud.Familia=family
			
			solicitud.save()
			
			
			url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante.id })
			return HttpResponseRedirect(url)
		else:
			return self.render_to_response(self.get_context_data(form=form))
	
			


class ParentescoUpdate(UpdateView):
	model = Parentesco
	form_class = ParentescoForm
	template_name = 'alumno/parentesco_form.html'
	
	def get_queryset(self):
		queryset = super(ParentescoUpdate, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(ParentescoUpdate, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante') # El mismo nombre que en tu URL
		dato=Estudiante.objects.get(id=estudiante)
		context['dato']=dato
		context['escolar']=dato.curso.establecimiento.id
		return context	

	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			solicitud = form.save(commit=False)
			solicitud.curso = 0
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			pariente=Parentesco.objects.get(id=pk)
			family=pariente.Familia

			solicitud.Familia=family
			
			solicitud.save()
			estudiante=self.kwargs.get('estudiante')
			# Retornamos el objeto
			url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante })
			return HttpResponseRedirect(url)	


class ParentescoDelete(DeleteView):
	model = Parentesco
	template_name = 'alumno/parentesco_delete.html'

	        

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(ParentescoDelete, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante') # El mismo nombre que en tu URL
		dato=Estudiante.objects.get(id=estudiante)
		context['dato']=dato
		context['escolar']=dato.curso.establecimiento.id
		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(ParentescoDelete, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante')
		pariente=Parentesco.objects.get(pk=pk)
		pariente.delete()
		
        # Retornamos el objeto
		url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante })
		return HttpResponseRedirect(url)
		
		
# Ingresar apoderado 
class ApoderadoCreate(CreateView):

	model = apoderado
	form_class = ApoderadoForm
	template_name = 'alumno/parentesco_form.html'
	
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(ApoderadoCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		
		context['dato']=Estudiante.objects.get(id=pk)
		return context
		print context
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			solicitud = form.save(commit=False)
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			estudiante=Estudiante.objects.get(id=pk)
			family=estudiante.Familia

			solicitud.Familia=family
			solicitud.Estudiante=estudiante
			solicitud.save()
			
			
			url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante.id })
			return HttpResponseRedirect(url)	


		else:
			return self.render_to_response(self.get_context_data(form=form))

		
class ApoderadoList(ListView):
	model = apoderado
	template_name = 'alumno/apoderado_list.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(ApoderadoList, self).get_context_data(**kwargs)
		dato = Estudiante.objects.all()
		context['dato'] = dato
		return context



class ApoderadoUpdate(UpdateView):
	model = apoderado
	form_class = ApoderadoForm
	template_name = 'alumno/apoderado_form.html'

	

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(ApoderadoUpdate, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante') # El mismo nombre que en tu URL
		dato=Estudiante.objects.get(id=estudiante)
		context['dato']=dato
		context['escolar']=dato.curso.establecimiento.id
		return context	

	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			solicitud = form.save(commit=False)
			print form
			solicitud.curso = 0
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			pariente=Parentesco.objects.get(id=pk)
			family=pariente.Familia

			solicitud.Familia=family
			
			solicitud.save()
			estudiante=self.kwargs.get('estudiante')
			# Retornamos el objeto
			url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante })
			return HttpResponseRedirect(url)



class ApoderadoDelete(DeleteView):
	model = apoderado
	template_name = 'alumno/apoderado_delete.html'


	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(ApoderadoDelete, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante') # El mismo nombre que en tu URL
		dato=Estudiante.objects.get(id=estudiante)
		context['dato']=dato
		context['escolar']=dato.curso.establecimiento.id
		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(ApoderadoDelete, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante')
		pariente=Parentesco.objects.get(pk=pk)
		pariente.delete()
		
        # Retornamos el objeto
		url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante })
		return HttpResponseRedirect(url)

#termino del apoderado

#Incio acciones para el hermano
class HermanoList(ListView):
	model = hermano
	template_name = 'alumno/hermano_list.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(HermanoList, self).get_context_data(**kwargs)
		dato = Estudiante.objects.all()
		context['dato'] = dato
		return context


class HermanoCreate(CreateView):

	model = hermano
	form_class = HermanoForm
	template_name = 'alumno/hermano_form.html'
	success_url = reverse_lazy('alumno:hermano_listar')

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(HermanoCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		print pk
		context['dato']=Estudiante.objects.get(id=pk)
		return context
		print context
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			solicitud = form.save(commit=False)
			solicitud.curso = 0
			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			estudiante=Estudiante.objects.get(id=pk)
			family=estudiante.Familia

			solicitud.Familia=family
			
			solicitud.save()
			
			
			# Retornamos el objeto
			url = reverse(('alumno:familia'), kwargs={ 'pk': pk })
			return HttpResponseRedirect(url)
		else:
			return self.render_to_response(self.get_context_data(form=form))
	


class HermanoUpdate(UpdateView):
	model = hermano
	form_class = HermanoForm
	template_name = 'alumno/hermano_form.html'
	
	
	def get_queryset(self):
		queryset = super(HermanoUpdate, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(HermanoUpdate, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante') # El mismo nombre que en tu URL
		dato=Estudiante.objects.get(id=estudiante)
		context['dato']=dato
		context['escolar']=dato.curso.establecimiento.id
		return context	

	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		
		if form.is_valid():
			solicitud = form.save(commit=False)

			pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
			pariente=Parentesco.objects.get(id=pk)
			family=pariente.Familia

			solicitud.Familia=family
			
			solicitud.save()
			estudiante=self.kwargs.get('estudiante')
			# Retornamos el objeto
			url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante })
			return HttpResponseRedirect(url)

class HermanoDelete(DeleteView):
	model = hermano
	template_name = 'alumno/hermano_delete.html'

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(HermanoDelete, self).get_context_data(**kwargs)
		
		#pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante') # El mismo nombre que en tu URL
		dato=Estudiante.objects.get(id=estudiante)
		context['dato']=dato
		context['escolar']=dato.curso.establecimiento.id
		return context

	def post(self,request,*args,**kwargs):	        
		self.object=self.get_object

		object = super(HermanoDelete, self).get_object()
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		estudiante=self.kwargs.get('estudiante')
		pariente=Parentesco.objects.get(pk=pk)
		pariente.delete()
		
        # Retornamos el objeto
		url = reverse(('alumno:familia'), kwargs={ 'pk': estudiante })
		return HttpResponseRedirect(url)




# Acciones para el establecimiento



class EstablecimientoCreate(CreateView):
	model = establecimiento
	form_class = EstablecimientoForm
	template_name = 'alumno/establecimiento_form.html'
	success_url = reverse_lazy('alumno:establecimiento_listar')

	@method_decorator(permission_required('Establecimiento.add_Establecimiento',reverse_lazy('alumno:establecimiento')))
        def dispatch(self, *args, **kwargs):
                return super(EstablecimientoCreate, self).dispatch(*args, **kwargs)

class EstablecimientoUpdate(UpdateView):
	model = establecimiento
	form_class = EstablecimientoForm
	template_name = 'alumno/establecimiento_form.html'
	success_url = reverse_lazy('alumno:establecimiento_listar')


class EstablecimientoDelete(DeleteView):
	model = establecimiento
	template_name = 'alumno/establecimiento_delete.html'
	success_url = reverse_lazy('alumno:establecimiento_listar')	

#Mostrar establecimientos asignados a cada profesinal
class EstablecimientoList(ListView):
# en el acceso de las aciiones con los establecimientos 
# se establecen acciones exclusivas para el encargado de convivencia y se determina en base al tipo de
# cargo que tiene en el establecimiento y este es desde el numero 6 -7-8 -9	
	model = Cargo
	template_name = 'alumno/establecimiento_profesional.html'
	success_url = reverse_lazy('alumno:establecimiento_listar')	

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(EstablecimientoList, self).get_context_data(**kwargs)
		try:
			dup=Profesional.objects.get(usuario=self.request.user)
			context['profesional']=Cargo.objects.filter(profesional=dup)

		
			return context
		except Profesional.DoesNotExist:
			return context
		
#Mostrar los establecmientos creados al suprvisor
#Mostrar establecimientos asignados a cada profesinal
class EstablecimientoListsupervisor(ListView):
# en el acceso de las aciiones con los establecimientos 
# se establecen acciones exclusivas para el encargado de convivencia y se determina en base al tipo de
# cargo que tiene en el establecimiento y este es desde el numero 6 -7-8 -9	
	model = Cargo
	template_name = 'alumno/establecimiento_profesional_supervisor.html'
	success_url = reverse_lazy('alumno:establecimiento_listar')	

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(EstablecimientoListsupervisor, self).get_context_data(**kwargs)
		try:
			dup=Profesional.objects.get(usuario=self.request.user)
			context['profesional']=Cargo.objects.filter(profesional=dup)

		
			return context
		except Profesional.DoesNotExist:
			return context




#Mostrar establecimientos asignados a cada profesinal pie 
class EstablecimientoListPie(ListView):
# en el acceso de las aciiones con los establecimientos 
# se establecen acciones exclusivas para el encargado de convivencia y se determina en base al tipo de
# cargo que tiene en el establecimiento y este es desde el numero 6 -7-8 -9	
	model = Cargo
	template_name = 'alumno/establecimiento_profesional_pie.html'
	success_url = reverse_lazy('alumno:establecimiento_listar')	
	
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(EstablecimientoListPie, self).get_context_data(**kwargs)
		try:
			dup=Profesional.objects.get(usuario=self.request.user)
			context['profesional']=Cargo.objects.filter(profesional=dup)

		
			return context
		except Profesional.DoesNotExist:
			return context
		






#Mostrar todas las acciones asociadas a un establecimiento
class EstablecimientoaccList(ListView):
# en el acceso de las aciiones con los establecimientos 
# se establecen acciones exclusivas para el encargado de convivencia y se determina en base al tipo de
# cargo que tiene en el establecimiento y este es desde el numero 6 -7-8 -9	
	model = Cargo
	template_name = 'alumno/establecimiento_profesional.html'
	success_url = reverse_lazy('alumno:establecimiento_listar')	
	paginate_by = 6
	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(EstablecimientoList, self).get_context_data(**kwargs)
		try:
			dup=Profesional.objects.get(usuario=self.request.user)
			context['profesional']=Cargo.objects.filter(profesional=dup)

		
			return context
		except Profesional.DoesNotExist:
			return context		
		

#Listado de estudiantes por establecimiento- dado que cada profesional tiene asignados un grupo de establecimientos
def listar_estudiantes_establecimiento(request,pk):
		
	estudiando=Escolaridad.objects.filter(establecimiento__id=pk)
	escuela=establecimiento.objects.get(id=pk)
	ficha=Ficha_derivacion.objects.filter(Q(Estudiante__curso__establecimiento__id=pk) & Q(estado=1) )
	
	casos=Intervencion_casos.objects.filter(estudiante__curso__establecimiento__id=pk)
	

	contexto = {'estudiando':estudiando,
				'escuela':escuela,
				 'ficha':ficha,
				 'casos':casos,
				 }

	return render(request, 'alumno/estudiante_establecimiento.html', contexto)


# Listado del area de las duplas para el supervisor
#Listado de estudiantes por establecimiento- dado que cada profesional tiene asignados un grupo de establecimientos
def listar_estudiantes_establecimiento_supervisor(request,pk):
		
	estudiando=Escolaridad.objects.filter(establecimiento__id=pk)
	escuela=establecimiento.objects.get(id=pk)
	ficha=Ficha_derivacion.objects.filter(Q(Estudiante__curso__establecimiento__id=pk) & Q(estado=1) )
	
	casos=Intervencion_casos.objects.filter(estudiante__curso__establecimiento__id=pk)
	

	contexto = {'estudiando':estudiando,
				'escuela':escuela,
				 'ficha':ficha,
				 'casos':casos,
				 }

	return render(request, 'alumno/estudiante_establecimiento_supervisor.html', contexto)



def digito_verificador(rut):
	if rut.isdigit(): 
		reversed_digits = map(int, reversed(str(rut)))
		factors = cycle(range(2, 8))
		s = sum(d * f for d, f in zip(reversed_digits, factors))
		return (-s) % 11
	else:
		return(-1)	    



def ingresa_valida_rut(request,pk):
	form = EstudianteVerForm(request.POST or None)
	form2 = EstudianteForm(request.POST or None)
	form3 =EscolaridadForm(request.POST or None)
	escuela=establecimiento.objects.get(id=pk)
	template = 'alumno/ingresar_escolaridad.html'

	mensaje=""
	if request.method == 'POST':
		if form.is_valid() :

			estudiando = form.save(commit=False)
			valor=int(estudiando.rut)
			dig=rut(valor)
			print dig
			
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)
		else:
			mensaje="Error de formulario y/o Estudiante ya existe"	

	context = {
        "form": form,
        "form2":form2,
        "form3":form3,

        "escuela":escuela,
        "mensaje":mensaje

    }		
	return render(request, template, context)	
	
@requires_csrf_token
def search(request,pk):
	form = EstudianteForm(request.POST or None)
	form2 =EscolaridadForm(request.POST or None)
	#mensaje = []
	# Aqui modifique la asignacion de la escuela dado que no funciona
	escuela=establecimiento.objects.get(id=pk)	
	mensaje=""
	if 'rut' in request.GET:
		
		rut = request.GET['rut']
		digito=request.GET['dig']
		if rut>=0 or digito>= 0 or digito=='k' or digito=='K':	
			digito=str(digito)

			print ("Digito verificador %s" % ( digito) )

			digito_upper = digito.upper()
			print ("Dígito verificador %s" % ( digito_upper) )
			rut=str(rut)
			valor=digito_verificador(rut)
			print ("Rut %s" % ( rut) )
			if valor== 10:
				valor='K'
			if str(valor) == str(digito_upper):
				if str(rut) == '10':
					rut_p=str(rut)+str('-')+'K'
					
				else:	
					rut_p=str(rut)+str('-')+str(digito)
					
			else:
				#mensaje.append('Rut incorrecto ')
				mensaje="Rut incorrecto "
				rut_p=""
	
			if not rut:
				mensaje.append('Ingresar un rut ')
			elif len(rut) > 8:
				mensaje=('Rut extiene el máximo de carácteres')

			else:
				try:
					
					estudiante = Estudiante.objects.get(rut=rut_p)
					lugar=estudiante.curso.establecimiento
					escuela=estudiante.curso.establecimiento
					lugar_curso=estudiante.curso.numero
					lugar_letra=estudiante.curso.letra
					if lugar_curso == 0:
						estado=estudiante.curso.establecimiento.nombre+ "Curso : NT1"
					elif lugar_curso == 1 :
						estado=estudiante.curso.establecimiento.nombre+ "Curso : Kinder"
					elif lugar_curso == 2 or lugar_curso == 3 or lugar_curso == 4 or lugar_curso == 5 or lugar_curso == 6 or lugar_curso == 7 or lugar_curso == 8 or lugar_curso == 9:
						lugar_curso = lugar_curso - 1 
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+ str(lugar_curso) +"º"
					elif lugar_curso == 10:
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+"1ª Medio"
					elif lugar_curso == 11:
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+"2ª Medio"
					elif lugar_curso == 12:
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+"3ª Medio"
					elif lugar_curso == 13:
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+"4ª Medio"
					# Falta la letra del curso y asignar el curso 			
					if lugar_letra == 0:
						estado=estado+ " A"
					elif lugar_letra == 1:
						estado=estado+ " B"
					elif lugar_letra == 2:
						estado=estado+ " C"
					elif lugar_letra == 3:
						estado=estado+ " D"			


					escolaridad=Escolaridad.objects.get(Estudiante=estudiante)
					form = EstudianteForm(instance=estudiante)
					form2 =EscolaridadForm(instance=escolaridad)

					mensaje="Estudiante existe en la base de datos "+estado
				except Estudiante.DoesNotExist:
					
					estudiante=Estudiante()
					
					
					estudiante.rut=rut_p
					
					form = EstudianteForm(instance=estudiante)
					escuela=establecimiento.objects.get(id=pk)
					print ("Escuela %s" % ( escuela) )
					escolaridad=""
					

		else:
			mensaje="Rut sin puntos, ni guiones"			
			escuela=establecimiento.objects.get(id=pk)	
			return render(request, 'alumno/ingresar_escolaridad.html',
                      {'estudiante': estudiante, 'form':form,'form2':form2,'digito':digito,'mensaje':mensaje,'escuela':escuela})
			escuela=establecimiento.objects.get(id=pk)  
	

	return render(request,'alumno/ingresar_escolaridad.html', {'mensaje': mensaje,
    	'form':form,
    	'form2':form2,
    	'escuela':escuela,
    	
    	})

	if request.method == 'POST':

		if form2.is_valid() and form3.is_valid():
		
			estudiando = form2.save(commit=False)# estudiante
			print ("Estudiando form2  %s" % ( estudiando) )

			escolar=form3.save(commit=False)# Escolaridad 
			print ("Estudiando form3 %s" % ( escolar) )
			escuela=establecimiento.objects.get(id=pk)
			print ("Escuela  %s" % ( escuela) )
			#ir a buscar el curso
			#etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

			try:
				print ("escolar-curso 2 %s" % ( escolar.curso) )
				print ("escolar-letra 2 %s" % ( escolar.Letra) )
				print ("escuela 2 %s" % ( escuela) )
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

			except curso.DoesNotExist:
				
				curso.objects.create(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
	        #codigo
			family=Familia.objects.create(cantidad=1)
			estudiando.Familia=family
			estudiando.curso=etapa
			diff = (datetime.date.today() - estudiando.fecha_nacimiento).days
			years = str(int(diff/365))		
			estudiando.edad=years
			estudiando.save()
			x=datetime.datetime.today()
			y=x.year
			escolar.edad=y
			escolar.establecimiento=escuela
			escolar.Estudiante=estudiando
			escolar.save()


			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)
		else:
			
			if form3.is_valid():
				estudiando = form3.save(commit=False)
			

				valor=int(estudiando.rut)

				estudiar=Estudiante.objects.get(pk=valor)
				form = EstudianteForm(instance=estudiar)
			else:
				mensaje="Error en el  formulario y/o Estudiante ya existe"	


	context = {
        "form": form,
        "form2":form2,
        "form3":form3,

        "escuela":escuela,
        "mensaje":mensaje,
    }		
	return render(request, template, context)	
	
@requires_csrf_token
def ingresar_estudiantes_establecimiento(request,pk):
	form3 = EstudianteVerForm(request.POST or None)	
	form = EstudianteForm(request.POST or None)
	form2 =EscolaridadForm(request.POST or None)
	escuela=establecimiento.objects.get(id=pk)
	template = 'alumno/ingresar_escolaridad.html'
	
	mensaje=""
	if request.method == 'POST':
		if form.is_valid() and form2.is_valid() :

			estudiando = form.save(commit=False)# Estudiante
			#print ("estudiando  %s" % ( estudiando) )
			escolar=form2.save(commit=False)# escolaridad
			#print ("escolar  %s" % ( escolar.Letra) )
			#pesadilla=form3.save(commit=False)
			escuela=establecimiento.objects.get(id=pk)
			#ir a buscar el curso
			#etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

			try:
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

			except curso.DoesNotExist:

				
				curso.objects.create(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
	        
			family=Familia.objects.create(cantidad=1)
			
			estudiando.Familia=family

			estudiando.curso=etapa
			
			diff = (datetime.date.today() - estudiando.fecha_nacimiento).days
			
			years = str(int(diff/365))		
			
			estudiando.edad=years
			estudiando.save()
			
			x=datetime.datetime.today()
			
			y=x.year
			escolar.edad=y
			
			escolar.establecimiento=escuela
			
			escolar.Estudiante=estudiando
			escolar.save()


			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)
		else:
			
			if form.is_valid():
				estudiando = form.save(commit=False)
				
				valor1=estudiando[:12]
				largo=len(estudiando.rut)
				corte=largo - 2
				valor1=estudiando[:corte]
				valor= estudiando.rut
				
				try:
					persona=Estudiante.objects.get(rut=valor)
					estudiar=Estudiante.objects.get(pk=persona.id)
					form = EstudianteForm(instance=estudiar)
					mensaje="Error en el  formulario y/o Estudiante ya existe 1"	

				except Estudiante.DoesNotExist:
					persona=None
				

			else:
				mensaje="Error en el  formulario y/o Estudiante ya existe "	


	context = {
        "form": form,
        "form2":form2,
        "form3":form3,

        "escuela":escuela,
        "mensaje":mensaje
    }		
	return render(request, template, context)	
	




def actualizar_escolaridad(request,pk,escolari):
	
	
	escolar=Escolaridad.objects.get(Estudiante__id=pk)
	dato=Estudiante.objects.get(pk=pk)
	form = EscolaridadActualizaForm(request.POST or None, instance=escolar)
	
	template = 'alumno/actualiza_escolaridad_form.html'
	context = {
        "form": form,
        "dato":dato,
    }



	if request.method == 'POST':
		if form.is_valid():

			
			escolaridad=form.save(commit=False)
			
			estudiando=Estudiante.objects.get(pk=pk)
			escuela=escolaridad.establecimiento
			#ir a buscar el curso

			try:
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
			except curso.DoesNotExist:
				curso.objects.create(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

				
	        #codigo
		
			estudiando.curso=etapa
			estudiando.save()
		
			escolaridad.establecimiento=escuela
			escolaridad.Estudiante=estudiando
			escolar=Escolaridad.objects.get(Estudiante__id=pk)
			escolaridad.save()
			print escolar
			anno=escolar.anno
			fecha_inicio=escolar.fecha_inicio
			fecha_termino=escolar.fecha_termino
			rendimiento=escolar.rendimiento
			conducta=escolar.conducta
			nivel=escolar.curso
			Letra=escolar.Letra
			establecimiento=escolar.establecimiento
			escuela=escolar.establecimiento
			EscolaridadAnterior.objects.create(anno=anno,fecha_inicio=fecha_inicio,fecha_termino=fecha_termino,rendimiento=rendimiento,conducta=conducta,curso=nivel,Letra=Letra,establecimiento=establecimiento,Estudiante=dato)	
	

			
			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)

	return render(request, template, context)	

def ver_escolaridad(request,pk,escolari):
	
	
	escolar=Escolaridad.objects.get(Estudiante__id=pk)
	dato=Estudiante.objects.get(pk=pk)
	anterior=EscolaridadAnterior.objects.filter(Estudiante__id=pk)
	print anterior
	
	template = 'alumno/ver_escolaridad.html'
	context = {
        "escolar":escolar,
        "dato":dato,
        "anterior":anterior,
    }
	return render(request, template, context)	



def ver_escolaridad_supervisor(request,pk,escolari):
	
	
	escolar=Escolaridad.objects.get(Estudiante__id=pk)
	dato=Estudiante.objects.get(pk=pk)
	anterior=EscolaridadAnterior.objects.filter(Estudiante__id=pk)
	print anterior
	
	template = 'alumno/ver_escolaridad_supervisor.html'
	context = {
        "escolar":escolar,
        "dato":dato,
        "anterior":anterior,
    }
	return render(request, template, context)


def ver_escolaridad_centro(request,pk):
	
	
	escolar=Escolaridad.objects.get(Estudiante__id=pk)
	dato=Estudiante.objects.get(pk=pk)
	anterior=EscolaridadAnterior.objects.filter(Estudiante__id=pk)
	print anterior
	
	template = 'alumno/ver_escolaridad_centro.html'
	context = {
        "escolar":escolar,
        "dato":dato,
        "anterior":anterior,
    }
	return render(request, template, context)
# Mostrar el estado de los estudiantes del establecimiento intervenidos
#Listado de estudiantes por establecimiento- dado que cada profesional tiene asignados un grupo de establecimientos
def estado_estudiantes_establecimiento(request,pk):
		
	estudiando=Escolaridad.objects.filter(establecimiento__id=pk)

	escuela=establecimiento.objects.get(id=pk)
	
	contexto = {'estudiando':estudiando,
				'escuela':escuela,
				 }
	return render(request, 'alumno/estudiante_estado_establecimiento.html', contexto)

def actualizar_escolaridad_centro(request,pk):
	
	
	escolar=Escolaridad.objects.get(Estudiante__id=pk)
	dato=Estudiante.objects.get(pk=pk)
	form = EscolaridadActualizaFormCentro(request.POST or None, instance=escolar)
	template = 'alumno/actualiza_escolaridad_centro.html'
	context = {
        "form": form,
        "dato":dato,
        "escolar":escolar,

    }

	
	if request.method == 'POST':
		if form.is_valid():

			
			escolaridad=form.save(commit=False)
			
			estudiando=Estudiante.objects.get(pk=pk)
			escuela=escolaridad.establecimiento
			#ir a buscar el curso

			try:
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
			except curso.DoesNotExist:
				curso.objects.create(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

				
	        #codigo
		
			estudiando.curso=etapa
			estudiando.save()
		
			escolaridad.establecimiento=escuela
			escolaridad.Estudiante=estudiando
			escolar=Escolaridad.objects.get(Estudiante__id=pk)
			escolaridad.save()
			print escolar
			anno=escolar.anno
			fecha_inicio=escolar.fecha_inicio
			fecha_termino=escolar.fecha_termino
			rendimiento=escolar.rendimiento
			conducta=escolar.conducta
			nivel=escolar.curso
			Letra=escolar.Letra
			establecimiento=escolar.establecimiento
			escuela=escolar.establecimiento
			EscolaridadAnterior.objects.create(anno=anno,fecha_inicio=fecha_inicio,fecha_termino=fecha_termino,rendimiento=rendimiento,conducta=conducta,curso=nivel,Letra=Letra,establecimiento=establecimiento,Estudiante=dato)	

			
			url = reverse(('derivacion:intervencion_listar'))
			return HttpResponseRedirect(url)

	return render(request, template, context)	


def actualizar_escolaridad_supervisor(request,pk):
	
	
	escolar=Escolaridad.objects.get(Estudiante__id=pk)
	dato=Estudiante.objects.get(pk=pk)
	form = EscolaridadActualizaFormCentro(request.POST or None, instance=escolar)
	template = 'alumno/actualiza_escolaridad_supervisor.html'
	context = {
        "form": form,
        "dato":dato,
        "escolar":escolar,

    }

	
	if request.method == 'POST':
		if form.is_valid():

			
			escolaridad=form.save(commit=False)
			
			estudiando=Estudiante.objects.get(pk=pk)
			escuela=escolaridad.establecimiento
			#ir a buscar el curso

			try:
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
			except curso.DoesNotExist:
				curso.objects.create(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

				
	        #codigo
		
			estudiando.curso=etapa
			estudiando.save()
		
			escolaridad.establecimiento=escuela
			escolaridad.Estudiante=estudiando
			escolar=Escolaridad.objects.get(Estudiante__id=pk)
			escolaridad.save()
			print escolar
			anno=escolar.anno
			fecha_inicio=escolar.fecha_inicio
			fecha_termino=escolar.fecha_termino
			rendimiento=escolar.rendimiento
			conducta=escolar.conducta
			nivel=escolar.curso
			Letra=escolar.Letra
			establecimiento=escolar.establecimiento
			escuela=escolar.establecimiento
			EscolaridadAnterior.objects.create(anno=anno,fecha_inicio=fecha_inicio,fecha_termino=fecha_termino,rendimiento=rendimiento,conducta=conducta,curso=nivel,Letra=Letra,establecimiento=establecimiento,Estudiante=dato)	

			
			



	return render(request, template, context)	


# Busqueda de estudiantes por nombre 



def busqueda_estudiante(request):
	
	
	form = EstudiantebusquedaNombreForm(request.POST or None)

	
	if request.method == 'POST':
		if form.is_valid():
			
			instance=form.save(commit=False)
			
			nombre=instance.nombres
			firs_name=instance.nfirs_name
			last_name=instance.last_name
			
			#ir a buscar el curso

			try:
				estudiante=Estudiante.objects.filter(nombre=instance.nombre,firs_name=instance.firs_name,last_name=instance.last_name)
				ficha=Ficha_derivacion.objects.filter(estudiante=estudiante)
				caso=Intervencion_casos.objetivo.filter(Estudiante=estudiante)
			except Estudiante.DoesNotExist:
				estudiante=None
				
			url = reverse(('alumno:busqueda_estudiante'))
			return HttpResponseRedirect(url)

	template = 'alumno/busqueda_estudiante.html'
	context = {
        "form": form,
        "estudiante":estudiante,
        "ficha":ficha,
        "caso":caso,
    }

	return render(request, template, context)	

# Busqueda de estudiantes por nombre 

# seach de busqueda
@requires_csrf_token
def search_estudiante(request,pk):
	form = EstudianteForm(request.POST or None)
	form2 =EscolaridadForm(request.POST or None)
	#mensaje = []
	mensaje=""
	if 'rut' in request.GET:
		
		rut = request.GET['rut']
		digito=request.GET['dig']
		if rut>=0 or digito>= 0 or digito=='k' or digito=='K':	
			digito=str(digito)

			digito_upper = digito.upper()

			rut=str(rut)
			valor=digito_verificador(rut)

			if valor== 10:
				valor='K'
			if str(valor) == str(digito_upper):
				if str(rut) == '10':
					rut_p=str(rut)+str('-')+'K'
					
				else:	
					rut_p=str(rut)+str('-')+str(digito)
					
			else:
				#mensaje.append('Rut incorrecto ')
				mensaje="Rut incorrecto "
				rut_p=""
	
			if not rut:
				mensaje.append('Ingresar un rut ')
			elif len(rut) > 9:
				mensaje=('Rut extiene el máximo de carácteres')

			else:
				try:
					
					estudiante = Estudiante.objects.get(rut=rut_p)
					lugar=estudiante.curso.establecimiento
					lugar_curso=estudiante.curso.numero
					lugar_letra=estudiante.curso.letra
					if lugar_curso == 0:
						estado=estudiante.curso.establecimiento.nombre+ "Curso : NT1"
					elif lugar_curso == 1 :
						estado=estudiante.curso.establecimiento.nombre+ "Curso : Kinder"
					elif lugar_curso == 2 or lugar_curso == 3 or lugar_curso == 4 or lugar_curso == 5 or lugar_curso == 6 or lugar_curso == 7 or lugar_curso == 8 or lugar_curso == 9:
						lugar_curso = lugar_curso - 1 
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+ str(lugar_curso) +"º"
					elif lugar_curso == 10:
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+"1ª Medio"
					elif lugar_curso == 11:
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+"2ª Medio"
					elif lugar_curso == 12:
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+"3ª Medio"
					elif lugar_curso == 13:
						estado=estudiante.curso.establecimiento.nombre+" Curso :"+"4ª Medio"
					# Falta la letra del curso y asignar el curso 			
					if lugar_letra == 0:
						estado=estado+ " A"
					elif lugar_letra == 1:
						estado=estado+ " B"
					elif lugar_letra == 2:
						estado=estado+ " C"
					elif lugar_letra == 3:
						estado=estado+ " D"			


					escolaridad=Escolaridad.objects.get(Estudiante=estudiante)
					form = EstudianteForm(instance=estudiante)
					form2 =EscolaridadForm(instance=escolaridad)

					mensaje="Estudiante existe en la base de datos "+estado
				except Estudiante.DoesNotExist:
					
					estudiante=Estudiante()
					estudiante.rut=rut_p
					form = EstudianteForm(instance=estudiante)
					escuela=establecimiento.objects.get(id=pk)
					print escuela
					escolaridad=""
					

		else:
			mensaje="Rut sin puntos, ni guiones"			
			escuela=establecimiento.objects.get(id=pk)	
			return render(request, 'alumno/ingresar_escolaridad.html',
                      {'estudiante': estudiante, 'form':form,'form2':form2,'digito':digito,'mensaje':mensaje,'escuela':escuela})
	escuela=establecimiento.objects.get(id=pk)  
	

	
	return render(request,'alumno/ingresar_escolaridad.html', {'mensaje': mensaje,
    	'form':form,
    	'form2':form2,
    	'escuela':escuela,
    	
    	})

	if request.method == 'POST':

		if form.is_valid() and form2.is_valid():

			estudiando = form.save(commit=False)
			escolar=form2.save(commit=False)
			escuela=establecimiento.objects.get(id=pk)
			#ir a buscar el curso
			#etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

			try:
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

			except curso.DoesNotExist:
				curso.objects.create(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
				etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)
	        #codigo
			family=Familia.objects.create(cantidad=1)
			print family
			estudiando.Familia=family

			estudiando.curso=etapa
			print etapa
			diff = (datetime.date.today() - estudiando.fecha_nacimiento).days
			print diff
			years = str(int(diff/365))		
			print years
			estudiando.edad=years
			estudiando.save()
			
			x=datetime.datetime.today()
			print x
			y=x.year
			escolar.edad=y
			print y
			escolar.establecimiento=escuela
			print escuela
			escolar.Estudiante=estudiando
			escolar.save()


			url = reverse(('alumno:listar_estudiantes_establecimiento'), kwargs={ 'pk': escuela.id})
			return HttpResponseRedirect(url)
		else:
			
			if form3.is_valid():
				estudiando = form3.save(commit=False)
				print estudiando

				valor=int(estudiando.rut)
				print valor
				estudiar=Estudiante.objects.get(pk=valor)
				form = EstudianteForm(instance=estudiar)
			else:
				mensaje="Error en el  formulario y/o Estudiante ya existe"	


	context = {
        "form": form,
        "form2":form2,
        "form3":form3,

        "escuela":escuela,
        "mensaje":mensaje
    }		
	return render(request, template, context)

# Busqueda de un estudiante en base al rut
@requires_csrf_token
def buscar_estudiantes(request,pk):

	form3 = EstudianteVerForm(request.POST or None)	
	estudiante=None
	
	escuela=establecimiento.objects.get(id=pk)
	print escuela
	template = 'alumno/buscar_estudiante.html'
	
	mensaje="aqui pase"
	if request.method == 'POST':
		if form3.is_valid() :
			est=form3.save(commit=False)
			print est.rut	
			try: 
				estudiante=Estudiante.objects.get(rut=est.rut)
				print estudiante
				mensaje=" Estudiante encontrado "
				print mensaje
				escuela=establecimiento.objects.get(id=pk)
			except Estudiante.DoesNotExist:
				mensaje= " Estudiante no existe en los registros"
				estudiante=None
			#ir a buscar el curso
			#etapa=curso.objects.get(numero=escolar.curso,letra=escolar.Letra,establecimiento=escuela)

		else:
			
			mensaje="Error en el  formulario y/o Estudiante ya existe "	
	else:
		mensaje="Búsqueda de estudiantes "	

	context = {
    
        "form3":form3,
        "estudiante":estudiante,

        "escuela":escuela,
        "mensaje":mensaje
    }		
	return render(request, template, context)	
	
