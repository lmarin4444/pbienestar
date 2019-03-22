from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    #url(r'^$', index, name='index'),
    #Listado de confirmaciones 
    url(r'^historia/(?P<pk>\d+)/$', login_required(views.ir_historia), name='ir_historia'),
    url(r'^ir_historia_dupla/(?P<pk>\d+)/$', login_required(views.ir_historia_dupla), name='ir_historia_dupla'),

    url(r'^registro_historico', login_required(views.registro_historico.as_view()), name='registro_historico'),
    url(r'^ver_historia_objetivos/(?P<pk>\d+)/(?P<estudiante>\d+)/$', login_required(views.ver_historia_objetivos), name='ver_historia_objetivos'),
    url(r'^ver_historia_ficha_derivacion/(?P<pk>\d+)/(?P<estudiante>\d+)/$', login_required(views.ver_historia_ficha_derivacion), name='ver_historia_ficha_derivacion'),
    url(r'^ver_historia_sesiones/(?P<pk>\d+)/(?P<estudiante>\d+)/$', login_required(views.ver_historia_sesiones), name='ver_historia_sesiones'),
    #Listado de informes hostoricos
    url(r'^Diagnostico_historia/(?P<pk>\d+)/(?P<historia>\d+)/$', login_required(views.evaluacion_historia), name='evaluacion_historia'),
    url(r'^final_historia/(?P<pk>\d+)/(?P<historia>\d+)/$', login_required(views.final_historia), name='final_historia'),
    url(r'^Ver_Reporte_continuidad_historia/(?P<pk>\d+)/(?P<historia>\d+)/$', login_required(views.VerReportecontinuidad_historia), name='ver_reporte_continuidad_historia'),
    url(r'^Reporte_cont_hist/(?P<pk>\d+)/(?P<continuidad>\d+)/(?P<historia>\d+)/$', login_required(views.ReportecontinuidadModificar_historia), name='listar_continuidad_historia'),
    url(r'^Reporte_EstudiantevsTematicas', login_required(views.EstudiantevsTematicas.as_view()), name='listar_EstudiantevsTematicas'),
   url(r'^Reporte_Listadointervenidos', login_required(views.Listadointervenidos.as_view()), name='listar_Listadointervenidos'),
  

]
