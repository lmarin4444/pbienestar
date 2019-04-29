from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from informe.views import generar_pdf
from informe.views import ver_calendario,FormatosDelete,FormatosList, \
    ReporteEstudiantePDF,ReporteEstudiantePDF_certificado,upload_file,ReporteEvaluacionPDF, \
    informe1_pdf_report,informe3_pdf_report,informe2_pdf_report,informe1_pdf_report_historico,informe3_pdf_report_historia, \
    informe2_pdf_report_historia,fichaderivacion_pdf_report,fichaderivacion_pdf_report_historica,fichaderivacion_dupla_pdf_report, \
    entrevistaingreso_dupla_pdf_report,fichaegreso_dupla_pdf_report,fichacontinuidad_dupla_pdf_report, fichaderivacionegresodupla_pdf_report, \
    hello_pdf



urlpatterns = [
    #Para template en pdf

    url(r'^generar_pdf/$', generar_pdf, name='pdf'),
    url(r'^generar_pdf_certificado/$', login_required(ReporteEstudiantePDF.as_view()), name='pdf_certificado'),
    url(r'^generar_pdf_asistencia//(?P<pk>\d+)/$', login_required(ReporteEstudiantePDF_certificado.as_view()), name='pdf_asistencia'),
    url(r'^Calendario_fechas/$',ver_calendario, name='calendario'),

    
    url(r'^listar', login_required(FormatosList.as_view()), name='formatos_listar'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(FormatosDelete.as_view()), name='formatos_eliminar'),
    url(r'^upload_file$', login_required(upload_file), name='upload_file'),

    #Informes en pdf evaluacion
    url(r'^generar_pdf_evaluacion/(?P<pk>\d+)/$', login_required(ReporteEvaluacionPDF.as_view()), name='pdf_evaluacion'),
    url(r'^generar_pdf1/(?P<pk>\d+)/$', login_required(informe1_pdf_report), name='pdf_evaluacion1'),
    url(r'^generar_pdf2/(?P<pk>\d+)/(?P<indice>\d+)/$', login_required(informe2_pdf_report), name='pdf_evaluacion2'),
    url(r'^generar_pdf3/(?P<pk>\d+)/$', login_required(informe3_pdf_report), name='pdf_evaluacion3'),
    
    #Informes en pdf para la historia
    url(r'^generar_pdf1_historia/(?P<pk>\d+)/(?P<historia>\d+)/$', login_required(informe1_pdf_report_historico ), name='pdf_evaluacion1_historia'),
    url(r'^generar_pdf2_historia/(?P<pk>\d+)/(?P<continuidad>\d+)/(?P<historia>\d+)/$', login_required(informe2_pdf_report_historia ), name='pdf_evaluacion2_historia'),
    url(r'^generar_pdf3_historia/(?P<pk>\d+)/(?P<historia>\d+)/$', login_required(informe3_pdf_report_historia ), name='pdf_evaluacion3_historia'),

    #Informe de ficha de derivacion
    url(r'^fichaderivacion_pdf_report/(?P<pk>\d+)/$', login_required(fichaderivacion_pdf_report), name='fichaderivacion_pdf_report'),
    url(r'^fichaderivacion_dupla_pdf_report/(?P<pk>\d+)/$', login_required(fichaderivacion_dupla_pdf_report), name='fichaderivacion_dupla_pdf_report'),
    url(r'^fichaderivacion_pdf_report_historica/(?P<pk>\d+)/$', login_required(fichaderivacion_pdf_report_historica), name='fichaderivacion_pdf_report_historica'),
    url(r'^entrevistaingreso_dupla_pdf_report/(?P<pk>\d+)/$', login_required(entrevistaingreso_dupla_pdf_report), name='entrevistaingreso_dupla_pdf_report'),
    url(r'^fichaegreso_dupla_pdf_report/(?P<pk>\d+)/$', login_required(fichaegreso_dupla_pdf_report), name='fichaegreso_dupla_pdf_report'),
    url(r'^fichacontinuidad_dupla_pdf_report/(?P<pk>\d+)/$', login_required(fichacontinuidad_dupla_pdf_report), name='fichacontinuidad_dupla_pdf_report'),
    url(r'^fichaderivacionegresodupla_pdf_report/(?P<pk>\d+)/$', login_required(fichaderivacionegresodupla_pdf_report), name='fichaderivacionegresodupla_pdf_report'),

    url(r'^hello_pdf', login_required(hello_pdf), name='hello_pdf'),


]