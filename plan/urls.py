# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
 
	
	url(r'^ingresar_plan/(?P<pk>\d+)/$', login_required(views.ingresar_plan.as_view()), name='ingresar_plan'),
#	Ingresar planes apoyo a la educacion
	url(r'^ingresar_plan_mineduc/(?P<pk>\d+)/', login_required(views.ingresar_plan_mineduc.as_view()), name='ingresar_plan_mineduc'),


	url(r'^modificar_plan/(?P<pk>\d+)/$', login_required(views.modificar_plan), name='modificar_plan'),
	url(r'^ActividadesListView/(?P<pk>\d+)/$', login_required(views.ActividadesListView), name='ActividadesListView'),
#Listado de plan por area: Dupla e encargado de convivencia


	url(r'^ActividadesDuplaListView/(?P<pk>\d+)/$', login_required(views.ActividadesDuplaListView), name='ActividadesDuplaListView'),
	url(r'^ActividadesConvivenciaListView/(?P<pk>\d+)/$', login_required(views.ActividadesConvivenciaListView), name='ActividadesConvivenciaListView'),
	url(r'^ingresar_hecho_actividades/(?P<agenda>\d+)/(?P<pk>\d+)/$', login_required(views.ingresar_hecho_actividades.as_view()), name='ingresar_hecho_actividades'),
	url(r'^justificar_hecho_actividades/(?P<agenda>\d+)/(?P<pk>\d+)/$', login_required(views.justificar_hecho_actividades.as_view()), name='justificar_hecho_actividades'),
	url(r'^reagendar_hecho_actividades/(?P<agenda>\d+)/(?P<pk>\d+)/$', login_required(views.reagendar_hecho_actividades.as_view()), name='reagendar_hecho_actividades'),
# REGISTRAR UNA ACCION CUANDO ESTA FUERA DE PLAZO
url(r'^justificar_hecho_actividades_fueradeplazo/(?P<agenda>\d+)/(?P<pk>\d+)/$', login_required(views.justificar_hecho_actividades_fueradeplazo.as_view()), name='justificar_hecho_actividades_fueradeplazo'),

	url(r'^ver_plancillo/(?P<pk>\d+)/(?P<base>\d+)/$', login_required(views.ver_plancillo.as_view()), name='ver_plancillo'),
	url(r'^ingresar_plancillo/(?P<pk>\d+)/(?P<base>\d+)/$', login_required(views.ingresar_plancillo.as_view()), name='ingresar_plancillo'),
	url(r'^modificar_plancillo/(?P<pk>\d+)/$', login_required(views.modificar_plancillo), name='modificar_plancillo'),
	url(r'^eliminar_plancillo/(?P<pk>\d+)/$', login_required(views.eliminar_plancillo.as_view()), name='eliminar_plancillo'),
	


	url(r'^ingresar_indicador/(?P<pk>\d+)/(?P<colegio>\d+)/$', login_required(views.ingresar_indicador.as_view()), name='ingresar_indicador'),
	url(r'^modificar_indicador/(?P<pk>\d+)/$', login_required(views.modificar_indicador), name='modificar_indicador'),
	url(r'^eliminar_indicador/(?P<pk>\d+)/$', login_required(views.eliminar_indicador.as_view()), name='eliminar_indicador'),

	url(r'^ingresar_acciones/(?P<pk>\d+)/(?P<colegio>\d+)/$', login_required(views.ingresar_acciones.as_view()), name='ingresar_acciones'),

	url(r'^ingresar_Actividad/(?P<pk>\d+)/', login_required(views.ingresar_Actividad.as_view()), name='ingresar_Actividad'),
	url(r'^eliminar_actividad/(?P<pk>\d+)/$', login_required(views.eliminar_actividad.as_view()), name='eliminar_actividad'),
	#Ingresar una actividad en el plan solo la medular

	url(r'^ingresar_Actividad_plan/(?P<pk>\d+)/', login_required(views.ingresar_Actividad_plan.as_view()), name='ingresar_Actividad_plan'),
	

	url(r'^modificar_actividad_plan/(?P<pk>\d+)/', login_required(views.modificar_actividad_plan), name='modificar_actividad_plan'),
	
	url(r'^modificar_actividad_plan_dos/(?P<pk>\d+)/', login_required(views.modificar_actividad_plan_dos), name='modificar_actividad_plan_dos'),
	
	url(r'^ActividadUpdate_plan/(?P<pk>\d+)/', login_required(views.ActividadUpdate_plan.as_view()), name='ActividadUpdate_plan'),
	
	url(r'^modificar_actividad_planificada/(?P<pk>\d+)/', login_required(views.modificar_actividad_planificada), name='modificar_actividad_planificada'),

	url(r'^ver_actividades/(?P<pk>\d+)/$', login_required(views.ver_actividades.as_view()), name='ver_actividades'),

	url(r'^ver_bases/(?P<pk>\d+)/$', login_required(views.ver_bases.as_view()), name='ver_bases'),
	url(r'^modificar_base/(?P<pk>\d+)/$', login_required(views.modificar_base), name='modificar_base'),
	url(r'^eliminar_base/(?P<pk>\d+)/$', login_required(views.eliminar_base.as_view()), name='eliminar_base'),

	url(r'^IndicadorListView/(?P<pk>\d+)/$', login_required(views.IndicadorListView), name='IndicadorListView'),
	url(r'^PlanListView/(?P<pk>\d+)/$', login_required(views.PlanListView), name='PlanListView'),
	
	url(r'^PlancilloListView/(?P<pk>\d+)/(?P<base>\d+)/$', login_required(views.PlancilloListView), name='PlancilloListView'),
	
	url(r'^AccionesListView/(?P<pk>\d+)/$', login_required(views.AccionesListView), name='AccionesListView'),
	url(r'^modificar_accion/(?P<pk>\d+)/$', login_required(views.modificar_accion), name='modificar_accion'),
	url(r'^eliminar_accion/(?P<pk>\d+)/$', login_required(views.eliminar_accion.as_view()), name='eliminar_accion'),
	#Para planificar las actividades dentro de cada mes
	url(r'^PlanificacionListView/(?P<pk>\d+)/$', login_required(views.PlanificacionListView), name='PlanificacionListView'),
	url(r'^PlanificacionEncargadoListView/(?P<pk>\d+)/$', login_required(views.PlanificacionEncargadoListView), name='PlanificacionEncargadoListView'),


	url(r'^PlanificacionDuplaListView/(?P<pk>\d+)/(?P<mes>\d+)/$', login_required(views.PlanificacionDuplaListView), name='PlanificacionDuplaListView'),
    url(r'^PlanificacionEncargadoConvivenciaListView/(?P<pk>\d+)/(?P<mes>\d+)/$', login_required(views.PlanificacionEncargadoConvivenciaListView), name='PlanificacionEncargadoConvivenciaListView'),

	# Mostrar todos los planes de años anteriores
	url(r'^PlanListViewTodos/(?P<pk>\d+)/', login_required(views.PlanListViewTodos), name='PlanListViewTodos'),
	url(r'^PlanListViewTodos_supervisor/(?P<pk>\d+)/', login_required(views.PlanListViewTodos_supervisor), name='PlanListViewTodos_supervisor'),

	url(r'^PlanListViewMineduc/(?P<pk>\d+)/', login_required(views.PlanListViewMineduc), name='PlanListViewMineduc'),

	#Modificar plan del año actual
	url(r'^modificar_plan/(?P<pk>\d+)/', login_required(views.modificar_plan), name='modificar_plan'),
	# Ver actividades presente en la bitacora
    url(r'^ver_bitacora_actividad/(?P<pk>\d+)/$', login_required(views.ver_bitacora_actividad.as_view()), name='ver_bitacora_actividad'),
    url(r'^ver_actividades_bitacora/(?P<pk>\d+)/$', login_required(views.ver_actividades_bitacora.as_view()), name='ver_actividades_bitacora'),

    # Ver planes externos 

    url(r'^PlanmineducListView/(?P<pk>\d+)/$', login_required(views.PlanmineducListView), name='PlanmineducListView'),
    #Duplicar un plan 
    url(r'^duplicar_plancillo/(?P<pk>\d+)/(?P<base>\d+)/(?P<plancillo>\d+)/$', login_required(views.duplicar_plancillo.as_view()), name='duplicar_plancillo'),

    url(r'^duplicar_Actividad_plan/(?P<pk>\d+)/', login_required(views.duplicar_Actividad_plan.as_view()), name='duplicar_Actividad_plan'),
    url(r'^modificar_duplicar_Actividad_plan/(?P<pk>\d+)/', login_required(views.modificar_duplicar_Actividad_plan.as_view()), name='modificar_duplicar_Actividad_plan'),
    


    ]
