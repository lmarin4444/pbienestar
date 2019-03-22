# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from sesion.views import listadousuarios, SesionList,SesionCreate,SesionDelete,SesionUpdate,index, \
	DiagnosticoList,DiagnosticoUpdate,DiagnosticoDelete, \
    DiagnosticoCreate,CasoDetailView,tipo_sesionList,tipo_sesionCreate,tipo_sesionUpdate,tipo_sesionDelete, \
    intervencionesList,IntervenidosList,CrearCita,Intervenidos_sesiones,tematicaCreate,tematicaList,tematicaUpdate, \
    tematicaDelete,ObjetivoIntervencionCreate,cambio_objetivo,CambioObjetivoListview,buscar_citas,AgendaDelete, \
    ModificarCita,crear_Sesion,Crear_Registro,Reportecontinuidad,Ficha_egreso,Motivo_egresoCreate,Motivo_egresoUpdate, \
    Motivo_egresoDelete,Motivo_egresoList,historia,historia_dupla,VerObjetivo,VerObjetivohistorico,Ficha_egresoModificar, \
    ReportecontinuidadModificar,CrearSeguimiento,ListarSeguimiento,ver_registro,ModificarRegistro,confirma_ver, \
    confirma_modificar,SeguimeintoDelete,SeguimientoUpdate,VerReportecontinuidad,ReportecontinuidadModificar, \
    Reportecontinuidad_solo

 

urlpatterns = [
    
    #sesiones desde la salida de una cita 
    url(r'^agregarcitanuevo/(?P<id_Estudiante>\d+)/$',login_required(CrearCita), name='nuevoagregar_cita'),


   # sesiones 
    url(r'^$', index, name='index'),
	url(r'^nueva_sesion$',login_required(SesionCreate.as_view()), name='sesion_crear'),
    url(r'^listar', login_required(SesionList.as_view()), name='sesion_listar'),
    #url(r'^listar_dos/(?P<pk>\d+)/$', login_required(SesionList2.as_view()), name='sesion_listar_dos'),
    # las sesiones de un estudiante en particular
    
    # Una vez que la sesion este echa mostar los detalles de la confirmacion
    url(r'^confirma_ver/(?P<pk>\d+)/(?P<age>\d+)$', login_required(confirma_ver), name='confirma_ver'),
    url(r'^confirma_modificar/(?P<pk>\d+)/(?P<age>\d+)$', login_required(confirma_modificar), name='confirma_modificar'),
    


    # funciones que resileven las consultas 
    
    url(r'^sesiones_listar/(?P<pk>\d+)/$', login_required(Intervenidos_sesiones), name='intervencion_listar'),
    url(r'^editar/(?P<pk>\d+)/$', login_required(SesionUpdate.as_view()), name='sesion_editar'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(SesionDelete.as_view()), name='sesion_eliminar'),
    
    
    
#Definicion de los objetivos de intervencion
    url(r'^objetivo_intervencion/(?P<pk>\d+)/$', login_required(ObjetivoIntervencionCreate), name='objetivo_intervencion'),
    url(r'^cambio_objetivo/(?P<pk>\d+)/(?P<objetivo>\d+)/$', login_required(cambio_objetivo), name='cambio_objetivo'),
    url(r'^listadoCambioObjetivo', login_required(CambioObjetivoListview.as_view()), name='listado_cambio_objetivo'),
    url(r'^VerObjetivo/(?P<pk>\d+)/$', login_required(VerObjetivo), name='VerObjetivo'),
    url(r'^VerObjetivoH/(?P<pk>\d+)/$', login_required(VerObjetivohistorico), name='historia_objetivo'),

 
# Acciones con tematicas
    url(r'^nuevo_tematica$', login_required(tematicaCreate.as_view()), name='tematica_crear'),
    url(r'^tematica_listar', login_required(tematicaList.as_view()), name='tematica_listar'),
    url(r'^tematica_editar/(?P<pk>\d+)/$', login_required(tematicaUpdate.as_view()), name='tematica_editar'),
    url(r'^eliminar_tematica/(?P<pk>\d+)/$', login_required(tematicaDelete.as_view()), name='tematica_eliminar'),


# Acciones con los tipos de sesion 
    url(r'^nuevo_tipo_sesion$', login_required(tipo_sesionCreate.as_view()), name='tipo_sesion_crear'),
    url(r'^tipo_sesion_listar', login_required(tipo_sesionList.as_view()), name='tipo_sesion_listar'),
    url(r'^editar_tipo_sesion/(?P<pk>\d+)/$', login_required(tipo_sesionUpdate.as_view()), name='tipo_sesion_editar'),
    url(r'^eliminar_tipo_sesion/(?P<pk>\d+)/$', login_required(tipo_sesionDelete.as_view()), name='tipo_sesion_eliminar'),

# acciones con los registros de sesiones para el usuario actual
    
    url(r'^listar_intervencion$', login_required(intervencionesList.as_view()), name='listar_intervenciones'),    
#Realizar seguimiento de un estudiante sobre la derivacion  a otra institucion

    url(r'^seguimiento/(?P<pk>\d+)/$',login_required(CrearSeguimiento), name='seguimiento'),
    url(r'^seguimiento_listar/(?P<pk>\d+)/$',login_required(ListarSeguimiento.as_view()), name='seguimiento_listar'),
    url(r'^eliminar_seguimiento/(?P<pk>\d+)/$',login_required(SeguimeintoDelete.as_view()), name='seguimiento_eliminar'),
    url(r'^update_seguimiento/(?P<pk>\d+)/$',login_required(SeguimientoUpdate.as_view()), name='seguimiento_modificar'),

#acciones con las Diagnosticos

    url(r'^diagnostico_nuevo$', login_required(DiagnosticoCreate.as_view()), name='diagnostico_crear'),
    url(r'^diagnostico_listar', login_required(DiagnosticoList.as_view()), name='diagnostico_listar'),
    url(r'^diagnostico_editar/(?P<pk>\d+)/$', login_required(DiagnosticoUpdate.as_view()), name='diagnostico_editar'),
    url(r'^diagnostico_eliminar/(?P<pk>\d+)/$', login_required(DiagnosticoDelete.as_view()), name='diagnostico_eliminar'),

    #acciones con los estudiantes intervenidos
    
    url(r'^intervenido', login_required(IntervenidosList.as_view()), name='intervenido'),
 	url(r'^listado', listadousuarios, name="listado"),
    #acciones para ver el seguimiento de un estudiante
    url(r'^Ficha_caso/(?P<pk>\d+)/$',login_required( CasoDetailView.as_view()),name='Caso'),
    # mostrar el listado de sesiones de un estudiante en particular 
    
    #Listado de citas en la agenda para un estudiante
    url(r'^buscar_citas/(?P<pk>\d+)/$', login_required(buscar_citas), name='buscar_citas'),
    url(r'^eliminar_citas/(?P<pk>\d+)/$', login_required( AgendaDelete.as_view()), name='eliminar_citas'),
    url(r'^modificar_citas/(?P<pk>\d+)/(?P<age>\d+)$', login_required(ModificarCita), name='modificar_citas'),
    # Manejo de informacion para las sesiones
    url(r'^crear_Sesion/(?P<age>\d+)/(?P<pk>\d+)$', login_required(crear_Sesion), name='crear_sesion'),
       
    # Manejo de informacion para las sesiones
    url(r'^crear_registro/(?P<age>\d+)/(?P<pk>\d+)$', login_required(Crear_Registro), name='crear_registro'),
    url(r'^ver_registro/(?P<age>\d+)/(?P<pk>\d+)$', login_required(ver_registro), name='ver_registro'),
    url(r'^modificar_registro/(?P<pk>\d+)$', login_required(ModificarRegistro), name='modificar_registro'),
    
    # construccion del informe de continuidad

    url(r'^Reporte_continuidad/(?P<pk>\d+)/$', login_required( Reportecontinuidad), name='reporte_continuidad'),
    url(r'^Reporte_continuidad_solo/(?P<pk>\d+)/$', login_required(Reportecontinuidad_solo), name='reporte_continuidad_solo'),
    url(r'^VerReporte_continuidad/(?P<pk>\d+)/$', login_required(VerReportecontinuidad), name='ver_reporte_continuidad'),
    url(r'^Reportecontinuidadmd/(?P<pk>\d+)/$', login_required(ReportecontinuidadModificar), name='ReportecontinuidadModificar'),

   
    #url(r'^Reporte_continuidad_modificar/(?P<pk>\d+)/$', login_required( ReportecontinuidadModificar), name='reporte_continuidad_modificar'),
   
   #construccion de la ficha de egreso
    url(r'^Ficha_egreso/(?P<pk>\d+)/$', login_required(Ficha_egreso), name='Ficha_egreso'),
    url(r'^Ficha_egreso_modificar/(?P<pk>\d+)/$', login_required(Ficha_egresoModificar), name='Ficha_egreso_modificar'),

    
    #manejo de informacion para el registro de los motivos de egreso   
    url(r'^Motivo_egreso_nuevo$', login_required(Motivo_egresoCreate.as_view()), name='Motivo_egreso_crear'),
    url(r'^Motivo_egreso_list', login_required(Motivo_egresoList.as_view()), name='Motivo_egreso_list'),
    url(r'^Motivo_egreso_editar/(?P<pk>\d+)/$', login_required(Motivo_egresoUpdate.as_view()), name='Motivo_egreso_editar'),
    url(r'^Motivo_egreso_eliminar/(?P<pk>\d+)/$', login_required(Motivo_egresoDelete.as_view()), name='Motivo_egreso_eliminar'),
    url(r'^historia_centro/(?P<ficha>\d+)/(?P<pk>\d+)/$', login_required(historia), name='historia'),
    url(r'^historia_dupla/(?P<ficha>\d+)/(?P<pk>\d+)/$', login_required(historia_dupla), name='historia_dupla'),

    
]