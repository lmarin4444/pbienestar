# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from alumno.views import escuela
from alumno.views import cabros

from alumno.views import EstablecimientoList, EstablecimientoCreate, EstablecimientoUpdate, EstablecimientoDelete, EstudianteCreate, \
    EstudianteList,EstudianteUpdate,EstudianteDelete, ParentescoList,ParentescoCreate,ParentescoUpdate,ParentescoDelete,CertificadosList,\
    EstudianteDetailView,ApoderadoCreate,ApoderadoList,ApoderadoUpdate,ApoderadoDelete,EstudianteDList, \
    CertificadosAsistenciaList,CertificadosList,CertificadosListCentro,FamiliaList,buscar_familia,FichaDetailView, \
    GrupoDetailView,FichaEstudianteDetailView,ver_familia,Reportedecaso,ConfirmacionList,ReportedecasoModificar, \
    HermanoList,HermanoCreate,HermanoUpdate,HermanoDelete,ver_estudiante_rut,EstablecimientoList,listar_estudiantes_establecimiento, \
    ingresar_estudiantes_establecimiento,actualizar_escolaridad,ver_escolaridad,ver_escolaridad_centro,actualizar_escolaridad_centro, \
    search,asignar_familia,agregar_familia,FichaCentroDetailView,estado_estudiantes_establecimiento,busqueda_estudiante, \
    buscar_estudiantes,search_estudiante,EstudianteListEstablecimiento,EstablecimientoListPie,EstudianteListpie, \
    EstablecimientoListsupervisor,listar_estudiantes_establecimiento_supervisor,FichaEstudianteDetailView_supervisor,ver_escolaridad_supervisor, \
    actualizar_escolaridad_supervisor,ver_familia_supervisor
   

urlpatterns = [
    #url(r'^$', index, name='index'),
    #Listado de confirmaciones 
    url(r'^confirma', login_required(ConfirmacionList.as_view()), name='confirma'),
    url(r'^establecimiento$',escuela, name='establecimiento'),#lista los estableciientos en la paguina principal
    
    url(r'^pupilo$',cabros, name='pupilo'),
   # las url de establecimiento

    #url(r'^$', index, name='index'),
    
    url(r'^nuevo$', login_required(EstablecimientoCreate.as_view()), name='establecimiento_crear'),
    url(r'^listar$', login_required(EstablecimientoList.as_view()), name='establecimiento_listar'),
    url(r'^EstablecimientoListsupervisor$', login_required(EstablecimientoListsupervisor.as_view()), name='EstablecimientoListsupervisor'),

    url(r'^EstablecimientoListPie', login_required(EstablecimientoListPie.as_view()), name='EstablecimientoListPie'),

    url(r'^editar/(?P<pk>\d+)/$', login_required(EstablecimientoUpdate.as_view()), name='establecimiento_editar'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(EstablecimientoDelete.as_view()), name='establecimiento_eliminar'),
    #url(r'^listado', listadousuarios, name="listado"),

    #urls de alumnos
    url(r'^Estudiantelistar', login_required(EstudianteList.as_view()), name='estudiante_listar'),
   
   #urls de alumnos de pie
    url(r'^EstudianteListpie', login_required(EstudianteListpie.as_view()), name='EstudianteListpie'),
   
    # Listado de estudiantes derivados al centro de bienestar de un establecimiento en particular
    url(r'^EstudianteListEstablecimiento/(?P<pk>\d+)/$',login_required(EstudianteListEstablecimiento.as_view()),name='EstudianteListEstablecimiento'),


    url(r'^certificado/(?P<pk>\d+)/$',login_required(EstudianteDetailView.as_view()),name='certificado'),
    url(r'^Ficha_certificado/(?P<pk>\d+)/$',login_required(FichaDetailView),name='Ficha'),
    url(r'^Ficha_ver/(?P<pk>\d+)/$',login_required(FichaCentroDetailView),name='Ficha_centro'),
    url(r'^nuevoest$', login_required(EstudianteCreate.as_view(), login_url='/admin/'), name='estudiante_crear'),
    # Ingresar un estudiante que ya existe anteriormente
    url(r'^ver_estudiante_rut',login_required(ver_estudiante_rut),name='ver_estudiante_rut'),
    #para actualizar la escolaridad de un estudiante
    url(r'^actuescolaridad/(?P<pk>\d+)/(?P<escolari>\d+)$', login_required(actualizar_escolaridad), name='actualizar_escolaridad'),
    url(r'^ver_escolaridad/(?P<pk>\d+)/(?P<escolari>\d+)$', login_required(ver_escolaridad), name='ver_escolaridad'),
    url(r'^ver_escolaridad_supervisor/(?P<pk>\d+)/(?P<escolari>\d+)$', login_required(ver_escolaridad_supervisor), name='ver_escolaridad_supervisor'),

    #Ver la escolaridad para el centro
    url(r'^ver_escolaridad_centro/(?P<pk>\d+)/$', login_required(ver_escolaridad_centro), name='ver_escolaridad_centro'),
    url(r'^actualizar_escolaridad_centro/(?P<pk>\d+)/$', login_required( actualizar_escolaridad_centro), name=' actualizar_escolaridad_centro'),
    url(r'^escolaridad_supervisor/(?P<pk>\d+)/$', login_required( actualizar_escolaridad_supervisor), name='escolaridad_supervisor'),

    url(r'^search/(?P<pk>\d+)/$',login_required(search),name='search'),
    url(r'^search_estudiante/(?P<pk>\d+)/$',login_required(search_estudiante),name='search_estudiante'),
    
    
    # Buscar estudiantes por rut
    url(r'^buscar_estudiantes/(?P<pk>\d+)/$',login_required(buscar_estudiantes),name='buscar_estudiantes'),



    #informes de secretaria
    url(r'^Certificadoslistar', login_required(CertificadosList.as_view()), name='certificados_listar'),
    # informes para el centro
    url(r'^CentroCertificadoslistar', login_required(CertificadosListCentro.as_view()), name='certificados_centro'),
    # ceritifcado de asistencia
    url(r'^CentroCertificadosasistencia', login_required(CertificadosAsistenciaList.as_view()), name='certificados_asistencia'),
    
    url(r'^editarest/(?P<pk>\d+)/(?P<escuela>\d+)/$', login_required(EstudianteUpdate), name='estudiante_editar'),
    url(r'^eliminarest/(?P<pk>\d+)/$', login_required(EstudianteDelete.as_view()), name='estudiante_eliminar'),
    
    #urls de parentesco

    url(r'^parentesconuevo/(?P<pk>\d+)/$', login_required(ParentescoCreate.as_view()), name='parentesco_crear'),
    url(r'^parentescolistarest', login_required(ParentescoList.as_view()), name='parentesco_listar'),
    url(r'^asignar_familia/(?P<pk>\d+)/$', login_required(asignar_familia.as_view()), name='asignar_familia'),
    

    url(r'^agregar_familia/(?P<pk>\d+)/(?P<familia>\d+)/$', login_required(agregar_familia), name='agregar_familia'),


    url(r'^editarparentesco/(?P<pk>\d+)/(?P<estudiante>\d+)/$',login_required(ParentescoUpdate.as_view()), name='parentesco_editar'),
    url(r'^eliminarparentesco/(?P<pk>\d+)/(?P<estudiante>\d+)/$', login_required(ParentescoDelete.as_view()), name='parentesco_eliminar'),

    #Hermanos del estudiante dentro de la famlia
    url(r'^hermanonuevo/(?P<pk>\d+)/$', login_required(HermanoCreate.as_view()), name='hermano_crear'),
    url(r'^hermanolistarest', login_required(HermanoList.as_view()), name='hermano_listar'),
    url(r'^hermanoeditarest/(?P<pk>\d+)/(?P<estudiante>\d+)/$', login_required(HermanoUpdate.as_view()), name='hermano_editar'),
    url(r'^hermanoeliminarest/(?P<pk>\d+)/(?P<estudiante>\d+)/$', login_required(HermanoDelete.as_view()), name='hermano_eliminar'),

    url(r'^apoderadonuevo/(?P<pk>\d+)/$', login_required(ApoderadoCreate.as_view()), name='apoderado_crear'),
    url(r'^apoderadolistarest', login_required(ApoderadoList.as_view()), name='apoderado_listar'),
    url(r'^apoderadoeditarest/(?P<pk>\d+)/(?P<estudiante>\d+)/$', login_required(ApoderadoUpdate.as_view()), name='apoderado_editar'),
    url(r'^apoderadoeliminarest/(?P<pk>\d+)/(?P<estudiante>\d+)/$', login_required(ApoderadoDelete.as_view()), name='apoderado_eliminar'),
    # listar a todos los estudiantes derivados
    url(r'^DerivadosCentro', login_required(EstudianteDList.as_view()), name='derivados_centro'),
    #ver a la familia de un estudiante
    url(r'^VerFamilia/(?P<pk>\d+)/$',login_required(FamiliaList.as_view()), name='ver_familia'),
    url(r'^VerGrupo/(?P<pk>\d+)/$',login_required(GrupoDetailView.as_view()), name='ver_grupo'),
    
    
    #vista que nos permite ver la familia de un estudiante dentro de su ficha
    url(r'^buscar_familia$',buscar_familia, name='buscar_familia'),#lista los estableciientos en la paguina principal
    #url(r'^buscar_familia$',detail_ficha , name='detalle_familia'),
    url(r'^Ver_ficha/(?P<pk>\d+)/$',login_required(FichaEstudianteDetailView), name='ver_ficha'),
    url(r'^FichaEstudianteDetailView_supervisor/(?P<pk>\d+)/$',login_required(FichaEstudianteDetailView_supervisor), name='FichaEstudianteDetailView_supervisor'),



    #Mostrar la familia de un estudiate 
    url(r'^familia/(?P<pk>\d+)/$',login_required(ver_familia), name='familia'),
    url(r'^ver_familia_supervisor/(?P<pk>\d+)/$',login_required(ver_familia_supervisor), name='ver_familia_supervisor'),
    # informes 
    url(r'^reporte_caso/(?P<pk>\d+)/$',login_required(Reportedecaso), name='reporte_caso'),
    url(r'^reporte_caso_modificar/(?P<pk>\d+)/$',login_required(ReportedecasoModificar), name='reporte_caso_modificar'),

    # asignacion de establecimientos a cada una de las duplas o pie
    
    url(r'^estableciprofe', login_required(EstablecimientoList.as_view()), name='profesinal_establecimiento_listar'),
    url(r'^estudianteestable/(?P<pk>\d+)/$', login_required(listar_estudiantes_establecimiento), name='listar_estudiantes_establecimiento'),
    url(r'^listar_estudiantes_establecimiento_supervisor/(?P<pk>\d+)/$', login_required(listar_estudiantes_establecimiento_supervisor), name='listar_estudiantes_establecimiento_supervisor'),
    url(r'^estado_estudiantes_establecimiento/(?P<pk>\d+)/$', login_required(estado_estudiantes_establecimiento), name='estado_estudiantes_establecimiento'),

    url(r'^ingestudianteestable/(?P<pk>\d+)/$', login_required(ingresar_estudiantes_establecimiento), name='ingresar_estudiantes_establecimiento'),
    #Para realizar proceso de bisqueda por medio de un formulario
    url(r'^busqueda_estudiante', login_required(busqueda_estudiante), name='busqueda_estudiante'),



]
