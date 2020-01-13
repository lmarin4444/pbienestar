from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from profesional.views import ProfesionalList,ProfesionalCreate,ProfesionalUpdate,ProfesionalDelete, \
	ProfesionalUpdate,CambioCreateView,ProfesionalListCentro,AccionesProfesionalList,AccionProfesional, \
    SeguimientoProfesionalList,AccionExternaDelete,ListarSeguimiento,AccionProfesionalCentro,AccionesProfesionaCentrolList, \
    ProfesionalList,ProfesionalListDirector

	
urlpatterns = [
   
    #urls de profesinal
    url(r'^Profesionallistar/$',login_required(ProfesionalList.as_view()), name='profesional_listar'),
    #Listado de profesionales para cada director
    url(r'^ProfesionalList/$',login_required(ProfesionalList.as_view()), name='ProfesionalList'),
    url(r'^ProfesionalListDirector/$',login_required(ProfesionalListDirector.as_view()), name='ProfesionalListDirector'),
    
    

    url(r'^ProfesionalListCentro',login_required(ProfesionalListCentro.as_view()), name='profesional_listar_Centro'),
    url(r'^ModificarProfesional/(?P<pk>\d+)/$', login_required(ProfesionalUpdate.as_view()), name='profesional_editar'),
    url(r'^eliminarProfesional/(?P<pk>\d+)/$', login_required(ProfesionalDelete.as_view()), name='profesional_eliminar'),
    url(r'^nuevoprofesional$', login_required(ProfesionalCreate.as_view()), name='profesional_crear'),
    # cambio de profesional
    
    url(r'^cambioprofesional/(?P<pk>\d+)/$', login_required(CambioCreateView), name='profesional_cambiar'),
    # Acciones particulares extras de cada profesional 
    url(r'^AccionesProfesionalList$', login_required(AccionesProfesionalList.as_view()), name='AccionesProfesionalList'),
    url(r'^AccionesProfesionaCentrolList$', login_required(AccionesProfesionaCentrolList.as_view()), name='AccionesProfesionaCentrolList'),
    url(r'^AccionProfesional$', login_required(AccionProfesional.as_view()), name='AccionProfesional'),
    url(r'^AccionProfesionalCentro$', login_required(AccionProfesionalCentro.as_view()), name='AccionProfesionalCentro'),

    url(r'^SeguimientoProfesionalList$', login_required(SeguimientoProfesionalList.as_view()), name='SeguimientoProfesionalList'),
    url(r'^AccionExternaDelete/(?P<pk>\d+)/$', login_required(AccionExternaDelete.as_view()), name='AccionExternaDelete'),
    # Listar los seguimientos selccionados
    url(r'^ListarSeguimiento/(?P<pk>\d+)/$', login_required(ListarSeguimiento.as_view()), name='ListarSeguimiento'),





]
