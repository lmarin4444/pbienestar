# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
 
	url(r'^Ficha_derivacion_dupla/(?P<pk>\d+)/(?P<establecimiento>\d+)$', login_required(views.Ficha_derivacion_duplas.as_view()), name='derivacion_dupla_crear'),
	#Modificar ficha derivacion dupla
	url(r'^FichaderivacionduplaUpdate/(?P<pk>\d+)/$',login_required(views.FichaderivacionduplaUpdate), name='FichaderivacionduplaUpdate'),
	
	url(r'^Ver_Ficha_derivacion_dupla/(?P<pk>\d+)/$',login_required(views.FichaDuplaDetailView), name='dupla_ver_ficha'),
	url(r'^Estudiante_listar_fichas_duplas/(?P<pk>\d+)/$', login_required(views.Estudiante_listar_fichas_duplas.as_view()), name='Estudiante_listar_fichas_duplas'),
	url(r'^entrevista_ingreso_dupla/(?P<pk>\d+)/$', login_required(views.entrevista_ingreso_dupla.as_view()), name='entrevista_ingreso_dupla'),
	# Ver la entrevista de ingreso 
	url(r'^Ver_entrevista_ingreso/(?P<pk>\d+)/$', login_required(views.Ver_entrevista_ingreso), name='Ver_entrevista_ingreso'),
	# Modificar entrevista de ingreso
	url(r'^FichaingresonduplaUpdate/(?P<pk>\d+)/$', login_required(views.FichaingresonduplaUpdate), name='FichaingresonduplaUpdate'),
	# Elememntos de convivencia escolar 
	url(r'^eliminar_mediacion/(?P<pk>\d+)/$', login_required(views.eliminar_mediacion.as_view()), name='eliminar_mediacion'),


	url(r'^ingresar_diagnostico/(?P<pk>\d+)/$', login_required(views.ingresar_diagnostico.as_view()), name='ingresar_diagnostico'),
	url(r'^indicador_auto/$', login_required(views.indicador_auto.as_view()), name='indicador_auto'),
	url(r'^DiagnosticoListView/(?P<pk>\d+)/$', login_required(views.DiagnosticoListView), name='DiagnosticoListView'),
	url(r'^DiagnosticoListViewTodos/(?P<pk>\d+)/$', login_required(views.DiagnosticoListViewTodos), name='DiagnosticoListViewTodos'),

	url(r'^DiagnosticoListView_Ver_todos/(?P<pk>\d+)/(?P<anio>\d+)$', login_required(views.DiagnosticoListView_Ver_todos), name='DiagnosticoListView_Ver_todos'),

	url(r'^modificar_diagnostico/(?P<pk>\d+)/$', login_required(views.modificar_diagnostico), name='modificar_diagnostico'),
	
	url(r'^Intervencion_casosCrear/(?P<pk>\d+)/(?P<colegio>\d+)$', login_required(views.Intervencion_casosCrear.as_view()), name='Intervencion_casosCrear'),
	#Modificar un plan de casos
	url(r'^PlanCasosUpdate/(?P<pk>\d+)/$', login_required(views.PlanCasosUpdate), name='PlanCasosUpdate'),
	# Listado de infirmacion de un plan de casos
	url(r'^Dupla_casos/(?P<pk>\d+)/$', login_required(views.Dupla_casos), name='Dupla_casos'),

	#Mostrar la situacion de intervencion de un estudiante desde el centro de Bienestar

	url(r'^Dupla_casos_centro/(?P<pk>\d+)/$', login_required(views.Dupla_casos_centro), name='Dupla_casos_centro'),
	

	#Modificar Derivacion ficha derivacion dupla
	url(r'^ModificarRetornoDefinitivo/(?P<pk>\d+)/$',login_required(views.ModificarRetornoDefinitivo), name='ModificarRetornoDefinitivo'),

	url(r'^IntervencionCasosDetailView/(?P<pk>\d+)/$',login_required(views.IntervencionCasosDetailView), name='IntervencionCasosDetailView'),
	url(r'^SesionDuplaUpdate/(?P<pk>\d+)/(?P<colegio>\d+)$',login_required(views.SesionDuplaUpdate), name='SesionDuplaUpdate'),
	url(r'^ModificarCita/(?P<pk>\d+)/(?P<colegio>\d+)$',login_required(views.ModificarCita), name='ModificarCita'),
	url(r'^eliminar_cita/(?P<pk>\d+)/$', login_required(views.eliminar_cita.as_view()), name='eliminar_cita'),

	url(r'^listar_convivencia_escolar/(?P<pk>\d+)/$', login_required(views.listar_convivencia_escolar), name='listar_convivencia_escolar'),
	url(r'^indicador_convivencia/(?P<pk>\d+)/$', login_required(views.indicador_convivencia.as_view()), name='indicador_convivencia'),
	url(r'^indicador_convivencia_mediacion/(?P<pk>\d+)/$', login_required(views.indicador_convivencia_mediacion.as_view()), name='indicador_convivencia_mediacion'),
	
	# Creacion de contingencia. de un curso en particular 
	url(r'^indicador_convivencia_curso/(?P<pk>\d+)/$', login_required(views.indicador_convivencia_curso.as_view()), name='indicador_convivencia_curso'),
	#creacion de convivencia para los estudiantes
	
	
	#Realizacion de la derivacion a otra institucion o sale de la intervencion
	url(r'^RetornoDefinitivo/(?P<pk>\d+)/$', login_required(views.RetornoDefinitivo), name='RetornoDefinitivo'),

	url(r'^EntradasDerivadas/(?P<pk>\d+)/$', login_required(views.EntradasDerivadas.as_view()), name='EntradasDerivadas'),
	url(r'^ListarCasos/(?P<pk>\d+)/$', login_required(views.ListarCasos.as_view()), name='ListarCasos'),
	

	url(r'^EntradasDerivadasIntitucion/(?P<pk>\d+)/$', login_required(views.EntradasDerivadasIntitucion.as_view()), name='EntradasDerivadasIntitucion'),

	url(r'^ListarEstablecimientos', login_required(views.ListarEstablecimientos.as_view()), name='ListarEstablecimientos'),
# Para realizar la busqueda de un estudiante 
	 url(r'^proyecto/busqueda/(?P<pk>\d+)/$',login_required(views.RBMidentificadorListView.as_view()), name='busqueda'), 
	 url(r'^BuscarConvivencia/(?P<pk>\d+)/$', login_required(views.BuscarConvivencia), name='BuscarConvivencia'),


# Mostar una paguina de errror 
	url(r'^Fallaconvivencia/', login_required(views.Fallaconvivencia), name='Fallaconvivencia'),

# Asignar estudiantes a un evento de convivencia 
	url(r'^mover/(?P<idAsignado>\d+)/(?P<idcolegio>\d+)/', login_required(views.mover), name='mover'),

#Mostrar toda la historia de un estudiante 
	url(r'^historia_dupla/(?P<pk>\d+)/$', login_required(views.historia_dupla), name='historia_dupla'),
#Registrar la asistencia de una sesion para un estudiante en particular
	url(r'^IntervencionCasosRegistar/(?P<pk>\d+)/', login_required(views.IntervencionCasosRegistar), name='IntervencionCasosRegistar'),
#Mostrar los estudiantes por un establecimiento o por un curso
	url(r'^listar_curso_convivencia_escolar/(?P<pk>\d+)/(?P<evento>\d+)/(?P<letra>\d+)/(?P<numero>\d+)/$', login_required(views.listar_curso_convivencia_escolar), name='listar_curso_convivencia_escolar'),
# seguimiento de los estudiantes intervenidos por la dupla PsicoSocial de cada establecimiento
	url(r'^listar_estudiantes_seguimiento/(?P<pk>\d+)/', login_required(views.listar_estudiantes_seguimiento), name='listar_estudiantes_seguimiento'),
	url(r'^CrearSeguimiento/(?P<pk>\d+)/', login_required(views.CrearSeguimiento), name='CrearSeguimiento'),
	url(r'^ListarSeguimiento/(?P<pk>\d+)/', login_required(views.ListarSeguimiento.as_view()), name='ListarSeguimiento'),
	url(r'^SeguimientoUpdate/(?P<pk>\d+)/', login_required(views.SeguimientoUpdate), name='SeguimientoUpdate'),
	url(r'^SeguimeintoDelete/(?P<pk>\d+)/', login_required(views.SeguimeintoDelete.as_view()), name='SeguimeintoDelete'),
# Modificar las mediaciones de lo encargados de convivencia
	url(r'^MediciacionUpdate/(?P<pk>\d+)/', login_required(views.MediciacionUpdate), name='MediciacionUpdate'),
# Mostrar toda la informacion de un plan de accion y de convivencia escolar


	url(r'^PlanesMostrarEscuelaListView/(?P<pk>\d+)/', login_required(views.PlanesMostrarEscuelaListView), name='PlanesMostrarEscuelaListView'),
	url(r'^PlanesMostrarEscuelaConvivenciaescolarListView/(?P<pk>\d+)/', login_required(views.PlanesMostrarEscuelaConvivenciaescolarListView), name='PlanesMostrarEscuelaConvivenciaescolarListView'),
	
# Borrar un caso de intervencion
	url(r'^eliminar_caso_dupla/(?P<pk>\d+)/', login_required(views.eliminar_caso_dupla.as_view()), name='eliminar_caso_dupla'),
#Crear continuidad de un estudiante
	url(r'^CrearContinuidad/(?P<pk>\d+)/', login_required(views.CrearContinuidad), name='CrearContinuidad'),
#Proceso de envio de estudiante de caso a hostoria
	url(r'^EntradasRetornoCasoDuplaList/(?P<pk>\d+)/', login_required(views.EntradasRetornoCasoDuplaList.as_view()), name='EntradasRetornoCasoDuplaList'),
#Proceso para ver los planes anteriores 
url(r'^PlanesAntiguoMostrarEscuelaListView/(?P<pk>\d+)/(?P<fecha>\d+)/', login_required(views.PlanesAntiguoMostrarEscuelaListView), name='PlanesAntiguoMostrarEscuelaListView'),
# ver la ficha de derivacion de un estudiante
    url(r'^FichaEstudianteegresoDetailView/(?P<pk>\d+)/$',login_required(views.FichaEstudianteegresoDetailView), name='FichaEstudianteegresoDetailView'),

    ]