# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
 
	
	url(r'^show/calendar/$',login_required(views.show_calendar),name='calendar-ano-mes'),
	
	url(r'^show/calendar/(?P<ano>\d+)/(?P<mes>\d+)/$',login_required(views.show_calendar_personal),name='personal'),
	url(r'^show/calendar/(?P<ano>\d+)/(?P<mes>\d+)/$',login_required(views.show_calendar),name='calendar2'),

	
	url(r'^show/calendar/$',login_required(views.show_calendar),name='calendar-ano-mes'),
	
	url(r'^bitacora/(?P<pk>\d+)/',login_required(views.BitacoraCreate.as_view()), name='bitacora_crear'), 
	url(r'^listar', login_required(views.BitacoraList.as_view()), name='bitacora_listar'),
	url(r'^buscar/(?P<dia>\d+)/(?P<mes>\d+)/$',login_required(views.buscar_fechas),name='fechas'),
	url(r'^buscar_planes_externos/(?P<dia>\d+)/(?P<mes>\d+)/(?P<plan>\d+)/$',login_required(views.buscar_planes_externos),name='buscar_planes_externos'),
    
    
    # Listado de las fechas programadas para los planes externos 
    url(r'^PlanesExternoListView/(?P<pk>\d+)/$', login_required(views.PlanesExternoListView), name='PlanesExternoListView'),
    # Listado de fechas de programas externos por establecimiento
    url(r'^PlanesExternoEscuelaListView/(?P<pk>\d+)/(?P<colegio>\d+)/$', login_required(views.PlanesExternoEscuelaListView), name='PlanesExternoEscuelaListView'),
    # Listado de planes externos dentro de la aplicacion para un colegio establecimio
    url(r'^Planes_externosEstablecimientoList/(?P<pk>\d+)/$', login_required(views.Planes_externosEstablecimientoList), name='Planes_externosEstablecimientoList'),

    url(r'^modificar_contingencia/(?P<pk>\d+)/$', login_required(views.modificar_contingencia), name='modificar_contingencia'),
    # Eliminar una contingencia 
    url(r'^eliminar_contingencia/(?P<pk>\d+)/$', login_required(views.eliminar_contingencia.as_view()), name='eliminar_contingencia'),
    # Ingresar la asistencia de una sesion ya planificada 
    url(r'^RegistrarSesionUpdate/(?P<pk>\d+)/$', login_required(views.RegistrarSesionUpdate.as_view()), name='RegistrarSesionUpdate'),
    url(r'^anular_sesion/(?P<pk>\d+)/$', login_required(views.anular_sesion), name='anular_sesion'),
    # Ver suceso de contingencia 
    url(r'^ver_sucesos/(?P<pk>\d+)/$',login_required(views.ver_sucesos), name='ver_sucesos'),
    



    ]



    

