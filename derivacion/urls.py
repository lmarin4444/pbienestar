from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from derivacion.views import listadousuarios, index, mascota_view, mascota_list, mascota_edit, mascota_delete, \
	MascotaList, MascotaCreate, MascotaUpdate, MascotaUpdate_centro, MascotaDelete,seguimientoListView,Modificarderivacion, \
    EsperaUpdateView,DerivadoUpdateView,listaesperaListView,SalirEsperaUpdateView,RetornoUpdateView,RetornoList, \
    IntervencionUpdateView,seguimientocentroListView,MascotaseguimientoList,EntradasBitacora,AsignarUpdateView, \
    BusquedaAjaxView,asignar_intervencion,EntradasFicha,gracias,EntradasList,EntradasOtrasList,EntradasRetornoDuplaList,historia_retorno, \
    ModificarFicha,RetornoDefinitivo,RetornoInstList,MascotaCreate_Prueba,MascotaUpdate_centro,ModificarRetornoDefinitivo, \
    ReporteIntervenidos
    

    

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^nuevo/(?P<pk>\d+)/(?P<establecimiento>\d+)$', login_required(MascotaCreate.as_view()), name='derivacion_crear'),
    url(r'^nuevo_prueba$', login_required(MascotaCreate_Prueba.as_view()), name='derivacion_crear_prueba'),

    url(r'^listar', login_required(MascotaList.as_view()), name='derivacion_listar'),
#listados de fichas de derivacion sin entrar al centro
    url(r'^centro_listar$',login_required(seguimientoListView.as_view()), name='centro_listar'),
#listados de fichas de derivacion 
    url(r'^intervencion_listar$',login_required(EntradasFicha.as_view()), name='intervencion_listar'),
    url(r'^intervencion_list$',login_required(EntradasList.as_view()), name='intervencion_list'),
    url(r'^intervencion_otrar$',login_required(EntradasOtrasList.as_view()), name='intervencion_otrar'),
    url(r'^intervencion_retorno$',login_required(EntradasRetornoDuplaList.as_view()), name='intervencion_retorno'),
#Listado de informes para su modificacion
    url(r'^modificar_informes$',login_required(ModificarFicha.as_view()), name='modificar_informes'),
    url(r'^espera_listar$',login_required(listaesperaListView.as_view()), name='espera_listar'),
    url(r'^salir_espera/(?P<pk>\d+)/$',login_required(SalirEsperaUpdateView.as_view()), name='salir_espera'),


    
    url(r'^editar/(?P<pk>\d+)/$', login_required(MascotaUpdate.as_view()), name='derivacion_editar'),
    # Aqui esta la que comente
    url(r'^editar_centro/(?P<pk>\d+)/$', login_required(MascotaUpdate_centro.as_view()), name='derivacion_editar_centro'),

    url(r'^centro_editar/(?P<pk>\d+)/$', login_required(MascotaUpdate_centro.as_view()), name='centro_derivacion_editar'),

    url(r'^eliminar/(?P<pk>\d+)/$', login_required(MascotaDelete.as_view()), name='derivacion_eliminar'),
    url(r'^enviar/(?P<pk>\d+)/$', login_required(MascotaDelete.as_view()), name='derivacion_eliminar'),
    
    url(r'^derivacion_centro/(?P<pk>\d+)/$',login_required(DerivadoUpdateView.as_view()), name='derivacion_centro'),
    url(r'^listado',login_required(listadousuarios), name="listado"),
    url(r'^modificar_derivacion/(?P<pk>\d+)/$',login_required(Modificarderivacion.as_view()), name="modificar_derivacion"),

    # patrones de paso de derivaciones
    url(r'^pasada_lista_espera/(?P<pk>\d+)/$', login_required(EsperaUpdateView.as_view()), name='derivacion_pasada_lista_espera'),

    #Retornos desde el centro a las duplas PsicoSociales 
    url(r'^retorno_pasada/(?P<pk>\d+)/$', login_required(RetornoUpdateView), name='derivacion_pasada_retorno'),
    url(r'^retorno', login_required(RetornoList.as_view()), name='retorno'),
    # Retorno a la dupla para otra instituion 
    url(r'^inst_retorno', login_required(RetornoInstList.as_view()), name='inst_retorno'),
    url(r'^sesion_actual/(?P<pk>\d+)/$', login_required(IntervencionUpdateView.as_view()), name='sesion'),
    url(r'^centrolistar', login_required(seguimientocentroListView.as_view()), name='listadocentro'),
    url(r'^inst/(?P<pk>\d+)/$', login_required(RetornoDefinitivo), name='derivacion_pasada_retorno_ints'),
    url(r'^modificar_inst/(?P<ficha>\d+)/(?P<pk>\d+)/$', login_required( ModificarRetornoDefinitivo), name='modificar_derivacion_pasada_retorno_ints'),


    #para ver el listado que tiene una dupla con respecto a sus derivaciones
    url(r'^centrolist', login_required(MascotaseguimientoList.as_view()), name='centrolistar'),    
    url(r'^bitacora', login_required(EntradasBitacora.as_view()), name='bitacora'),
    url(r'^asignar/(?P<pk>\d+)/$',login_required(AsignarUpdateView.as_view()), name='asignar'),
    url(r'^busqueda_ajax', login_required(BusquedaAjaxView.as_view()), name='busquedaajax'),

    #Grabar la primera intervencion
     url(r'^asignar_intervencion/(?P<pk>\d+)/$',login_required(asignar_intervencion.as_view()),name='asignar_intervencion'),
    #gracias por enviar la ficha de derivacion 
    url(r'^gracias', login_required(gracias), name="gracias"),
    #LIstado de la historia de los estudiantes 
    
    url(r'^listar_retorno/(?P<ficha>\d+)/(?P<pk>\d+)/$', login_required(historia_retorno), name='listar_retorno'),
    # Ver todos los intervenidos actuales 
    url(r'^ReporteIntervenidos', login_required(ReporteIntervenidos.as_view()), name='ReporteIntervenidos'),

]


