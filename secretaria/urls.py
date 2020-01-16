# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nuevo$', login_required(views.MascotaCreate.as_view()), name='secretaria_crear'),
    url(r'^nueva_pregunta$', login_required(views.MascotaCreate.as_view()), name='secretaria_crear'),
    
    url(r'^listar', login_required(views.VistaListarPregunta.as_view()), name='secretaria_listar'),
    url(r'^Estudiantelistar', login_required(views.EstudianteList.as_view()), name='secretaria_listar_estudiante'),
    url(r'^editar/(?P<pk>\d+)/$', login_required(views.MascotaUpdate.as_view()), name='secretaria_editar'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(views.MascotaDelete.as_view()), name='secretaria_eliminar'),
    #url(r'^listado', listadousuarios, name="listado"),
    url(r'^listadoObs', views.mascota_list_obs, name="secretaria_listar_obs"),
    # urls para agenda 
    url(r'^Agendalistar', login_required(views.VistaListarPregunta.as_view()), name='secretaria_listar'),
    url(r'^AgendaCalendario/(?P<pk>\d+)/(?P<fecha>\d+)/$', login_required(views.VistaCrearAgendaCalendario.as_view()), name='secretaria_listar_calendario'),

    url(r'^agregar/(?P<pk>\d+)/$',views.VistaCrearPregunta.as_view(), name='agregar'),
    url(r'^apuntar/(?P<dia>\d+)/(?P<mes>\d+)/(?P<anio>\d+)/$',login_required(views.VistaCrearAgenda.as_view()), name='agendar'),
    url(r'^apuntarcentro',views.VistaCrearAgendaEspera.as_view(), name='agendarcentro'),
    url(r'^Entradas/(?P<year>\d{4})/(?P<month>\d{2})/$',login_required(views.EntradasMes.as_view()), name='entradas_mes'),
    
    url(r'^DiasEntradas/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$',login_required(views.EntradasDia.as_view()), name='entradas_dia'),
    url(r'^fechas/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$',login_required(views.EntradasDias), name='entradas_dias'),
    url(r'^Calendario', views.cal_mes, name="calendario"),
    url('<int:year>/week/<int:week>/',views.ArticleWeekArchiveView.as_view(),name="archive_week"),

    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$',views.EntradasDia.as_view(), name='entradas'),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/$',views.EntradasMes.as_view(), name='entrada_mes'),
    #Listar a todos los intervenidos
    url(r'^intervenidos', login_required(views.IntervenidossecreList.as_view()), name='intervenidos'),
    url(r'^salvacion', login_required(views.salvacion), name='salvacion'),
    url(r'^ver_escuela', views.ver_escuela, name='ver_escuela'),
    #Para ingresar confirmacion de asistencia
    url(r'^confirmacion/(?P<pk>\d+)/$', login_required(views.Confirmacion), name='confirmar'),
    url(r'^buscar_agenda/(?P<pk>\d+)/$', login_required(views.buscar_agenda), name='buscar_agenda'),
    
    

    

    #para crear el registro de confirmacion de horario

    url(r'^confirmacion_crea/(?P<pk>\d+)/(?P<age>\d+)$', login_required(views.ConfirmacionCreate), name='confirmacion_crear'),
    url(r'^modificarconfirmacion/(?P<pk>\d+)/(?P<age>\d+)$', login_required(views.ConfirmacionModificar), name='confirmacion_modificar'),
    url(r'^confirmacion_eliminar/(?P<pk>\d+)/(?P<age>\d+)$', login_required(views.Confirmacion_Delete), name='Confirmacion_eliminar'),
    url(r'^ver_dia', login_required(views.ver_dia), name='ver_dia'),


    url(r'^ver_semana', login_required(views.ver_semana), name='ver_semana'),
    url(r'^ver_impresa$', login_required(views.ver_impresa), name='ver_impresa'),
    url(r'^ver_impresa_proxima$', login_required(views.ver_impresa_proxima), name='ver_impresa_proxima'),
    url(r'^ver_impresa_profesional/(?P<pk>\d+)$', login_required(views.ver_impresa_profesional), name='ver_impresa_profesional'),
    

    #Para ver los apoderados  de cada estudiante 
    url(r'^VerApoderado/(?P<pk>\d+)/(?P<fami>\d+)$',login_required(views.ver_apoderado), name='ver_apoderado'),
    # Ver un calendario por mes
    url(r'^ver_calandario_mes', login_required(views.ver_calandario_mes), name='ver_calandario_mes'),
    # Ver las sesiones de un estudiante 
    #url(r'^Intervenidos_sesiones_secretaria/(?P<pk>\d+)/$', login_required(views.Intervenidos_sesiones_secretaria), name='Intervenidos_sesiones_secretaria'),
    url(r'^Intervenidos_sesiones/(?P<pk>\d+)/$', login_required(views.Intervenidos_sesiones), name='Intervenidos_sesiones'),
    ]


