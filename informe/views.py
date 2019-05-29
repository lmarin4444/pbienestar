# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from secretaria.forms import MascotaRAForm
from secretaria.models import MascotaRA
from alumno.models import Estudiante,Escolaridad
from derivacion.models import Ficha_derivacion
from sesion.models import Intervenidos,Diagnostico,objetivo_intervencion,Ficha_de_egreso,Reporte_continuidad
from usuario.models import Profile
#para realizar los informes
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import styles
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4

from reportlab.platypus import Table
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, Image 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT 
from reportlab.lib.units import cm, mm, inch 
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from django.shortcuts import render_to_response
from informe.models import formatos
from informe.forms import UploadForm
from historia.models import Historia,Intervenidos_historico,Diagnostico_historia,Ficha_de_egreso_historia,Reporte_continuidad_historia
from dupla.models import Ficha_derivacion_dupla,Entrevista_ingreso_dupla,Derivacion_Ficha_derivacion_dupla,Continuidad_dupla
from django.template import Template, Context
from datetime import datetime
from datetime import date
#from rlextra.rml2pdf import rml2pdf
import cStringIO
from cStringIO import StringIO
from django.views.generic import View
from django.conf import settings
import os
from PIL import Image, ImageDraw, ImageFont

def search_form(request):
    return render_to_response('search_form.html')


def getPDF(request):
    """Returns PDF as a binary stream."""

    if 'q' in request.GET:
            
        rml = getRML(request.GET['q'])  
    
        buf = cStringIO.StringIO()
        
        #create the pdf
        rml2pdf.go(rml, outputFileName=buf)
        buf.reset()
        pdfData = buf.read()
        
        #send the response
        response = HttpResponse(mimetype='application/pdf')
        response.write(pdfData)
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response

def getRML(name):
    """We used django template to write the RML, but you could use any other
    template language of your choice. 
    """
    t = Template(open('hello.rml').read())
    c = Context({"name": name})
    rml = t.render(c)
    #django templates are unicode, and so need to be encoded to utf-8
    return rml.encode('utf8')



class IndexView(ListView):
    template_name = "certificado.html"
    model = Estudiante
    context_object_name = "c"


def generar_pdf(request):
    print "Genero el PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "intervenidos.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado ", styles['Heading1'])


    clientes.append(header)
    headings = ('Rut', 'Nombres', 'Apellido Paterno', 'Apellido Materno', 'Establecimiento')
    allclientes = [(p.Estudiante.rut, p.Estudiante.nombres, p.Estudiante.firs_name, p.Estudiante.last_name,p.Estudiante.curso.establecimiento) for p in intervenido.objects.all()]
    print allclientes

    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response    

# certificado de asistencia en pdf
class ReporteEstudiantePDF(View):

    def cabecera(self,pdf):
            archivo_imagen = settings.MEDIA_ROOT+'/imagenes/logo.png'
            archivo_imagen2 = settings.MEDIA_ROOT+'/imagenes/logo_cabildo.jpg'
            #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
            pdf.drawImage(archivo_imagen, 50, 750, 70, 70,preserveAspectRatio=True)
            pdf.drawImage(archivo_imagen2, 330, 750, 220, 90,preserveAspectRatio=True)

            #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
            pdf.setFont("Helvetica", 11)

            #Dibujamos una cadena en la ubicación X,Y especificada
            pdf.drawString(200, 20, u"bienestardemCabildo@gmail.com")

            #Dibujamos una cadena en la ubicación X,Y especificada
            pdf.setFont("Helvetica", 16)
            pdf.drawString(200, 750, u"Listado Estudiantes")

            pdf.setFont("Helvetica", 11)    
            pdf.drawString(240, 40, u"Centro de Bienestar")
            pdf.line(195,18,370,18)



    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla

        encabezados = ('rut', 'Nombres', 'A. Paterno', 'A. Materno ','Establecimiento')
        #Creamos una lista de tuplas que van a contener a las personas

        detalles = [(estudiante.rut, estudiante.nombres[0:20], estudiante.firs_name[0:10], estudiante.last_name[0:10],estudiante.curso.establecimiento.nombre[0:30]) for estudiante in Estudiante.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        cm=17
        detalle_orden = Table([encabezados] + detalles, colWidths=[4 * cm, 6 * cm, 4 * cm, 4 * cm,11 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
        [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)

    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 400
        self.tabla(pdf, y)
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

class ReporteEstudiantePDF_certificado(View):

    def cabecera(self,pdf):
            #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
           
            
            
            archivo_imagen=Image(settings.MEDIA_ROOT + '/logo.png')
            #archivo_imagen2=Image(settings.MEDIA_ROOT + '/encabezadocabildo.jpg', width=550, height=30)


            #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
            pdf.drawImage(archivo_imagen, 50, 750, 70, 70,preserveAspectRatio=True)
            #pdf.drawImage(archivo_imagen2, 330, 750, 220, 90,preserveAspectRatio=True)

            #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
            pdf.setFont("Helvetica", 11)
            #Dibujamos un
            #a cadena en la ubicación X,Y especificada
            pdf.drawString(200, 20, u"bienestardemCabildo@gmail.com")

            pdf.drawString(240, 40, u"Centro de Bienestar")
            pdf.line(195,18,370,18)
            
        
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        temp=StringIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        encabezados=('Informe de asistencia ')
        #Creamos una lista de tuplas que van a contener a las personas
        pk = self.kwargs.get('pk')
        estudiante=Estudiante.objects.get(id=pk)
        escolar=Escolaridad.objects.get(Estudiante__id=pk)
        profesional=Intervenidos.objects.get(Estudiante__id=pk)
        detalles =  estudiante.nombres
         # Create the PDF object, using the BytesIO object as its "file."
        
        response = HttpResponse(content_type='application/pdf')
        filename="Informe de evaluacion_"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
        response['Content-Disposition']='attachment; filename="%s"' % filename
        
        
        
        # Observa que ahora en vez de usar el nombre del archivo usamos el response

        #p = canvas.Canvas(buffer,pagesize=A4)
        p = canvas.Canvas(temp,pagesize=A4)


        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.setLineWidth(.3)
        p.setFont('Helvetica', 12)
        p.drawString(153, 680, u"CERTIFICADO DE ATENCIÓN CENTRO DE BIENESTAR")
        
        p.line(100,675,500,675)

        p.drawString(60,580,"Por medio de este certificado, se acredita la participación de :") 
        
        p.setFont('Helvetica', 12)
        p.drawString(60,540,"ESTUDIANTE") 
        p.drawString(240,540,":") 
        p.drawString(250,540,estudiante.nombres)
        p.drawString(320,540,estudiante.firs_name)
        p.drawString(400,540,estudiante.last_name)

        p.drawString(60,520,"RUT")
        p.drawString(240,520,":")  
        p.drawString(250,520,estudiante.rut)
       
       
        p.drawString(60,500,"ESTABLECIMIENTO")
        p.drawString(240,500,":")  
        p.drawString(250,500,estudiante.curso.establecimiento.nombre)
        p.drawString(60,480,"PROFESIONAL QUE ATIENDE ")
        p.drawString(240,480,":")
        
        p.drawString(250,480,profesional.Profesional)
        p.drawString(60,460,"Quién esta realizando proceso de intervención Psicoológica a partir del mes de")
        mes=profesional.fecha_intervencion.month
        if mes==1:
            nombre_mes="Enero"
        elif mes==2:
            nombre_mes="Febrero"
        elif mes==3:
            nombre_mes="Marzo"
        elif mes==4:
            nombre_mes="Abril"
        elif mes==5:
            nombre_mes="Mayo"
        elif mes==6:
            nombre_mes="Junio"
        elif mes==7:
            nombre_mes="Julio"
        elif mes==8:
            nombre_mes="Agosto"
        elif mes==9:
            nombre_mes="Septiembre"
        elif mes==10:
            nombre_mes="Octubre"
        elif mes==11:
            nombre_mes="Noviembre"
        else :
            nombre_mes="Diciembre"            
        anio=profesional.fecha_intervencion.year
        p.drawString(60,440,nombre_mes)
        p.drawString(60+len(nombre_mes)+40,440,"del")
        p.drawString(60+len(nombre_mes)+60,440,str(anio))
        p.drawString(60,410,"Quién(es) se presenta(n) a esta prestación es la/el mencionado, junto a su")
        
        p.drawString(252,390,"la Sr.(a) ")
        p.line(60,390,250,390)
        p.line(300,390,480,390)
        p.drawString(60,370,"Utilícese este documento sólo  con un fin infomativo y no para uso particular.")

        p.line(200,160,380,160)
        p.drawString(240,150,"Firma encargado")

          #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(p)
        y = 250
        
        #Con show page hacemos un corte de página para pasar a la siguiente
        p.showPage()
        p.save()
        
        #try:
        #    from StringIO import StringIO
        #except ImportError:
        #    from io import StringIO
        #temp = StringIO()
        #p = buffer.getvalue()
        #buffer.close()
        #response.write(p)
        response.write(temp.getvalue())
        return response

def ver_calendario(request):
     return render (request,"informe/Calendario_fechas.html",{})

class FormatosList(ListView):
    model = formatos
    template_name = 'informe/formato_listar.html' 
    paginate_by = 10



class FormatosDelete(DeleteView):
    model = formatos
    template_name = 'informe/formatos_delete.html'
    success_url = reverse_lazy('informe:formatos_listar')  



def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():

            instance = form.save(commit=False)
            x = date.today()
            instance.fecha_subida=x
            instance.docfile1=request.FILES['docfile1']
            instance.usuario=request.user
            instance.save()
            return redirect('informe:formatos_listar')
            
    else:
        form = UploadForm()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'informe/upload.html', {'form': form})


# Crear informe en pdf de cada uno de los informes 

# certificado de asistencia en pdf
class ReporteEvaluacionPDF(View):

    def cabecera(self,pdf):
            archivo_imagen = settings.MEDIA_ROOT+'/imagenes/logo.png'
            archivo_imagen2 = settings.MEDIA_ROOT+'/imagenes/logo_cabildo.jpg'
            #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
            pdf.drawImage(archivo_imagen, 50, 750, 70, 70,preserveAspectRatio=True)
            pdf.drawImage(archivo_imagen2, 330, 750, 220, 90,preserveAspectRatio=True)

            #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
            pdf.setFont("Helvetica", 11)

            #Dibujamos una cadena en la ubicación X,Y especificada
            pdf.drawString(200, 20, u"bienestardemCabildo@gmail.com")

            #Dibujamos una cadena en la ubicación X,Y especificada
            pdf.setFont("Helvetica", 14)
            pdf.drawString(130, 720, u"REPORTE BREVE DE PROCESO DE EVALUACIÓN")

            pdf.setFont("Helvetica", 11)    
            pdf.drawString(240, 40, u"Centro de Bienestar")
            pdf.line(195,18,370,18)



    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla

        encabezados = ('Motivo derivación')
        #Creamos una lista de tuplas que van a contener a las personas

        detalles = [(estudiante.rut, estudiante.nombres, estudiante.firs_name, estudiante.last_name) for estudiante in Estudiante.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        cm=20
        detalle_orden = Table([encabezados] + detalles, colWidths=[6 * cm, 6 * cm, 6 * cm, 6 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
        [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)

    def get(self, request, *args, **kwargs):
         
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        encabezados=('Reporte de Evaluación ')
        #Creamos una lista de tuplas que van a contener a las personas
        pk = self.kwargs.get('pk')
        estudiante=Estudiante.objects.get(id=pk)
        escolar=Escolaridad.objects.get(Estudiante__id=pk)
        nivel=escolar.get_curso()
        letra=escolar.get_Letra()
        ficha=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
        profesional=Intervenidos.objects.get(Estudiante__id=pk)
        try:
            evaluado=Diagnostico.objects.get(Estudiante__id=pk)
        except Diagnostico.DoesNotExist:
            evaluado=None
            mensaje="No existe documento de Evaluación"
        try:
            obj=objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
        except objetivo_intervencion.DoesNotExist:
            obj=None

        
         # Create the PDF object, using the BytesIO object as its "file."
        
        p = canvas.Canvas(buffer,pagesize=A4)


        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        contenido = []
        p.setLineWidth(.3)
        p.setFont('Helvetica', 11)
                
        
        p.drawString(60,690,"ESTUDIANTE") 
        p.drawString(240,690,":") 

        p.drawString(250,690,estudiante.nombres)
        p.drawString(320,690,estudiante.firs_name)
        p.drawString(400,690,estudiante.last_name)

    
        p.drawString(60,677,"ESTABLECIMIENTO")
        p.drawString(240,677,":")  
        p.drawString(250,677,estudiante.curso.establecimiento.nombre)



        p.drawString(60,665,"EDAD")
        p.drawString(240,665,":")  
        p.drawString(250,665,str(estudiante.edad))

        p.drawString(60,652,"CURSO")
        p.drawString(240,652,":")  
        p.drawString(250,652,nivel)
        
        
        p.drawString(60,639,"LETRA")
        p.drawString(240,639,":")  
        p.drawString(250,639,letra)
        



        p.drawString(60,626,"FECHA DEL INFORME")
        p.drawString(240,626,":")  
        p.drawString(250,626,str(evaluado.fecha.strftime('%d/%m/%Y')))

        p.drawString(60,613,"PROFESIONAL QUE DERIVA")
        p.drawString(240,613,":")  
        p.drawString(250,613,ficha.usuario.first_name)
        p.drawString(320+len(str(ficha.usuario.first_name))+10,613,ficha.usuario.last_name)        

        p.drawString(60,600,"MOTIVO DE LA DERIVACIÓN")
        p.drawString(240,600,":") 
        pos=613
        for motivo in ficha.Motivo_derivacion.all():

            p.drawString(250,pos-13,"-") 
            p.drawString(255,pos-13,motivo.nombre) 
            pos=pos-13       
        
        p.drawString(60,pos-15,"FASE DE LA INTERVENCIÓN ")
        p.drawString(240,pos-15,":")
        p.drawString(250,pos-15,'Término de Fase de evaluación')                        

        p.drawString(60,pos-28,"SITUACION ACTUAL")
        p.drawString(240,pos-28,":")
        estilo = getSampleStyleSheet()
        parrafo=Paragraph(evaluado.situacion_actual, estilo['Normal'])

        ancho, alto = 400, 400
        ancho_aux, alto_aux = parrafo.wrap(ancho, alto)

        #Reducimos la altura, si es necesario (si es así mandamos el flowable al canvas).

        if ancho_aux <= ancho and alto_aux <= alto:  
          # Reducimos la altura. 
          ancho = ancho - ancho_aux 
          # Mandamos el Flowable al canvas.  
          parrafo.drawOn(p,0,alto_aux) 
          # Salvamos el canvas. 
          p.save()
        else: 
          raise ValueError, "No hay suficiente espacio" 
                
        
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf, y)

          #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(p)
        y = 250
        
        #Con show page hacemos un corte de página para pasar a la siguiente
        p.showPage()
        p.save()
        p = buffer.getvalue()
        buffer.close()
        
        response.write(p)
        return response#Indicamos el tipo de contenido a devolver, en este caso un pdf
        


def informe1_pdf_report(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    Title = "INFORME DE EVALUACIÓN"
    pageinfo = "Departamento de Educación, Centro de Bienestar  Correo electónico: bienestardemcabildo@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))


    
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    ficha=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
    profesional=Intervenidos.objects.get(Estudiante__id=pk)
    try:
        evaluado=Diagnostico.objects.get(Estudiante__id=pk)
    except Diagnostico.DoesNotExist:
        evaluado=None
        mensaje="No existe documento de Evaluación"
    try:
        obj=objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
    except objetivo_intervencion.DoesNotExist:
        obj=None
    Elements = []
    #doc = SimpleDocTemplate(response)

    filename="Informe de evaluacion_"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    # Observa que ahora en vez de usar el nombre del archivo usamos el response
    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Informe de evaluación",
    author="Centro de Bienestar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    Elements.append(Spacer(0,8))
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/encabezadocabildo.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))



    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    
    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    if evaluado:
        data.append((
        Paragraph('<font size=10>%s</font>' % "Fecha:", estilo['Normal']), 
        Paragraph('<font size=10>%s</font>' % evaluado.fecha.strftime('%d/%m/%Y'), estilo['Normal']),
        ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional que deriva:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))



    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Motivo de la derivación:", estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % " Listado motivos indicados en Ficha derivación", estilo['Normal']),   
    ))

    for motivo in ficha.Motivo_derivacion.all():

        data.append((
        Paragraph('<font size=10>%s</font>' % " ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % motivo.nombre, estilo['Normal']),
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fase de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % "Término de fase de Evaluación", estilo['Normal']),   
    ))


    if evaluado:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Situación Actual:", estilo_centrado['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.situacion_actual, estilo_centrado['Normal']),   
    ))
    if obj:        

        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Objetivo de la intervención:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % obj.objetivo_particular, estilo['Normal']),   
        ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Derivación (Institución  y/o Especialista):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.Red_apoyo, estilo['Normal']),   
    ))
    if evaluado:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Observaciones:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.observaciones, estilo['Normal']),   
        ))

        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Sugerencias a la Familia:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.familia, estilo['Normal']),   
        ))



    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)

    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response

def informe1_pdf_report_historico(request,pk,historia):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    Title = "INFORME DE EVALUACIÓN"
    pageinfo = "Departamento de Educación, Centro de Bienestar  Correo electónico: bienestardemcabildo@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))
    
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    history=Historia.objects.get(pk=historia)
    ficha=history.Ficha_derivacion
    
    profesional=Intervenidos_historico.objects.get(Historia=history)
    try:
        evaluado=Diagnostico_historia.objects.get(Historia=history)
    except Diagnostico_historia.DoesNotExist:
        evaluado=None
        mensaje="No existe documento de Evaluación"
    obj=history.objetivo_intervencion   
    Elements = []
    #doc = SimpleDocTemplate(response)

    filename="Informe_de_evaluacion_historica"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    # Observa que ahora en vez de usar el nombre del archivo usamos el response
    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Informe de evaluación historico",
    author="Centro de Bienestar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    Elements.append(Spacer(0,8))
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/encabezadocabildo.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))



    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    
    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    if evaluado:

        data.append((
        Paragraph('<font size=10>%s</font>' % "Fecha de entrega:", estilo['Normal']), 
        Paragraph('<font size=10>%s</font>' % evaluado.fecha.strftime('%d/%m/%Y'), estilo['Normal']),
        ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional que deriva:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))



    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Motivo de la derivación:", estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % " Listado motivos indicados en Ficha derivación", estilo['Normal']),   
    ))

    for motivo in ficha.Motivo_derivacion.all():

        data.append((
        Paragraph('<font size=10>%s</font>' % " ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % motivo.nombre, estilo['Normal']),
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fase de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % "Término de fase de Evaluación", estilo['Normal']),   
    ))
    if evaluado:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Situación Actual:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.situacion_actual, estilo['Normal']),   
        ))

    if obj:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Objetivo de la intervención:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % obj.objetivo_particular, estilo['Normal']),   
        ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Derivación (Institución  y/o Especialista):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.Red_apoyo, estilo['Normal']),   
    ))
    if evaluado:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Observaciones:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.observaciones, estilo['Normal']),   
        ))

    
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Sugerencias a la Familia:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.familia, estilo['Normal']),   
        ))




    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)

    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response




def informe2_pdf_report(request,pk,indice):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    Title = "INFORME DE CONTINUIDAD"
    pageinfo = "Departamento de Educación, Centro de Bienestar  Correo electónico: bienestardemcabildo@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]


    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))


    
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    reporte=Reporte_continuidad.objects.get(pk=indice)
    try:
        objetivo=objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
    except objetivo_intervencion.DoesNotExist:
        objetivo=None
    
    Elements = []
    #doc = SimpleDocTemplate(response)

    filename="Informe_de_continuidad_"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    # Observa que ahora en vez de usar el nombre del archivo usamos el response


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Informe de continuidad",
    author="Centro de Bienestar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)

    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    Elements.append(Spacer(0,8))
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/encabezadocabildo.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))



    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Nombre:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
     

    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))


    if reporte:
        
        data.append((
        Paragraph('<font size=10>%s</font>' % "Fecha:", estilo['Normal']), 
        Paragraph('<font size=10>%s</font>' % reporte.fecha.strftime('%d/%m/%Y'), estilo['Normal']),
        ))
    

        data.append((
        Paragraph('<font size=10>%s</font>' % "Motivo  ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % reporte.get_motivo(), estilo['Normal']),
        ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fase de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % "Continuidad", estilo['Normal']),   
    ))
    if objetivo:
        data.append((
              
            Paragraph('<font size=10>%s</font>' % "Objetivo de la intervención:", estilo['Normal']),
            Paragraph('<font size=10>%s</font>' % objetivo.objetivo_particular, estilo['Normal']),   
            ))
    if reporte: 
        data.append((
             
        Paragraph('<font size=10>%s</font>' % "Antecedentes:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % reporte.antecedentes, estilo['Normal']),   
        ))

    
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Observaciones:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % reporte.observaciones, estilo['Normal']),   
        ))
    
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Sugerencias:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % reporte.sugerencias, estilo['Normal']),   
        ))


    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)

    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response


#Reporte historico del numero 2
def informe2_pdf_report_historia(request,pk,continuidad,historia):

    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    Title = "INFORME DE CONTINUIDAD"
    pageinfo = "Departamento de Educación, Centro de Bienestar  Correo electónico: bienestardemcabildo@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))
    
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    
    reporte=Reporte_continuidad_historia.objects.get(pk=continuidad)
    objetivo_h=reporte.Historia
    objetivo_pk=objetivo_h.objetivo_intervencion
    history=Historia.objects.get(pk=historia)

    try:
        objetivo=objetivo_intervencion.objects.get(pk=objetivo_pk.id)
    except objetivo_intervencion.DoesNotExist:
        objetivo=None
    Elements = []
    #doc = SimpleDocTemplate(response)

    filename="Informe_de_continuidad_historica"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    # Observa que ahora en vez de usar el nombre del archivo usamos el response
    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Informe de egreso historico",
    author="Centro de Bienestar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    Elements.append(Spacer(0,8))
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/encabezadocabildo.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))



    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    
    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    

    if reporte:
        
        data.append((
        Paragraph('<font size=10>%s</font>' % "Fecha:", estilo['Normal']), 
        Paragraph('<font size=10>%s</font>' % reporte.fecha.strftime('%d/%m/%Y'), estilo['Normal']),
        ))
        

        data.append((
        Paragraph('<font size=10>%s</font>' % "Motivo  ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % reporte.get_motivo(), estilo['Normal']),
        ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fase de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % "Continuidad", estilo['Normal']),   
    ))
    if objetivo:
        data.append((
              
            Paragraph('<font size=10>%s</font>' % "Objetivo de la intervención:", estilo['Normal']),
            Paragraph('<font size=10>%s</font>' % objetivo.objetivo_particular, estilo['Normal']),   
            ))
    if reporte:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Antecedentes:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % reporte.antecedentes, estilo['Normal']),   
        ))

    
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Observaciones:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % reporte.observaciones, estilo['Normal']),   
        ))
    
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Sugerencias:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % reporte.sugerencias, estilo['Normal']),   
        ))


    
    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)

    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response


# Imprimir informes historicos de egreso para los estudiantes ya egresados del centro
def informe3_pdf_report_historia(request,pk,historia):

    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    Title = "INFORME DE EGRESO"
    pageinfo = "Departamento de Educación, Centro de Bienestar  Correo electónico: bienestardemcabildo@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))
    
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    history=Historia.objects.get(pk=historia)
    ficha=history.Ficha_derivacion
    
    profesional=Intervenidos_historico.objects.get(Historia=history)
    try:
        evaluado=Ficha_de_egreso_historia.objects.get(Historia=history)
    except Ficha_de_egreso_historia.DoesNotExist:
        evaluado=None
        mensaje="No existe documento de egreso"
    

    obj=history.objetivo_intervencion 
    Elements = []
    #doc = SimpleDocTemplate(response)

    filename="Informe_de_egreso_historica"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    # Observa que ahora en vez de usar el nombre del archivo usamos el response
    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Informe de egreso historico",
    author="Centro de Bienestar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    Elements.append(Spacer(0,8))
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/encabezadocabildo.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))



    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    
    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    

    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional que deriva:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))



    if evaluado:
       
        data.append((
        Paragraph('<font size=10>%s</font>' % "Fecha:", estilo['Normal']), 
        Paragraph('<font size=10>%s</font>' % evaluado.fecha_egreso.strftime('%d/%m/%Y'), estilo['Normal']),
        ))


    

        data.append((
        Paragraph('<font size=10>%s</font>' % "Motivo de egreso ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % evaluado.Motivo_egreso, estilo['Normal']),
        ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fase de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % "Término de la intervención", estilo['Normal']),   
    ))
    if obj:
        data.append((
              
            Paragraph('<font size=10>%s</font>' % "Objetivo de la intervención:", estilo['Normal']),
            Paragraph('<font size=10>%s</font>' % obj.objetivo_particular, estilo['Normal']),   
            ))

    if evaluado:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Síntesis:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.sintesis, estilo['Normal']),   
        ))

    
    
    
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Sugerencias:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.sugerencias, estilo['Normal']),   
        ))

    





    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)

    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response


    
def informe3_pdf_report(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()

    Title = "INFORME DE EGRESO"
    pageinfo = "Departamento de Educación, Centro de Bienestar  Correo electónico: bienestardemcabildo@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]


    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))


    
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    ficha=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
    profesional=Intervenidos.objects.get(Estudiante__id=pk)
    try:
        evaluado=Ficha_de_egreso.objects.get(Estudiante__id=pk)
    except Ficha_de_egreso.DoesNotExist:
        evaluado=None
        mensaje="No existe documento de egreso"
    try:
        obj=objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
    except objetivo_intervencion.DoesNotExist:
        obj=None
    
    Elements = []
    #doc = SimpleDocTemplate(response)

    filename="Informe_de_egreso_"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    # Observa que ahora en vez de usar el nombre del archivo usamos el response


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Informe de Egreso",
    author="Centro de Bienestar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)

    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    Elements.append(Spacer(0,8))
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/encabezadocabildo.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))



    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Nombre:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
     

    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))


   

    if evaluado:
       
        data.append((
        Paragraph('<font size=10>%s</font>' % "Fecha de egreso:", estilo['Normal']), 
        Paragraph('<font size=10>%s</font>' % evaluado.fecha_egreso.strftime('%d/%m/%Y'), estilo['Normal']),
        )) 

        data.append((
        Paragraph('<font size=10>%s</font>' % "Motivo de egreso ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % evaluado.Motivo_egreso, estilo['Normal']),
        ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fase de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % "Término de la intervención", estilo['Normal']),   
    ))
    if obj:
        data.append((
              
            Paragraph('<font size=10>%s</font>' % "Objetivo de la intervención:", estilo['Normal']),
            Paragraph('<font size=10>%s</font>' % obj.objetivo_particular, estilo['Normal']),   
            ))
    if evaluado:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Síntesis:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.sintesis, estilo['Normal']),   
        ))

    
    
    
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Sugerencias:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % evaluado.sugerencias, estilo['Normal']),   
        ))



    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)

    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response


def fichaderivacion_pdf_report(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)

        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()


    
    Title = "FICHA DE DERIVACIÓN"
    pageinfo = "Centro de Bienestar     Correo electónico: bienestardemcabildo@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))



    # Set up HttpResponse object
    #response = HttpResponse(mimetype='application/pdf')
   
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    ficha=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
    

    filename="Ficha_derivacion_"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    
    Elements = []
    #doc = SimpleDocTemplate(response)


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Ficha de derivación",
    author="Centro de Bienestar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    
    #imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/encabezadocabildo.jpg',width=490,height=40)

    #Elements.append(imagen_logo)
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,24))
    Elements.append(Spacer(0,24))

    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))




    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    

    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional que deriva:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))



    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Motivo de la derivación:", estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % " Listado motivos indicados en Ficha derivación", estilo['Normal']),   
    ))
    




    for motivo in ficha.Motivo_derivacion.all():

        data.append((
        Paragraph('<font size=10>%s</font>' % " ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % motivo.nombre, estilo['Normal']),
    ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fecha de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.fecha_derivacion.strftime('%d/%m/%Y'), estilo['Normal']),   
    ))


    


    if ficha.pie == "True":
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "¿Pertence al programa P.I.E.?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "Sí", estilo['Normal']),   
        ))
    else:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "¿Pertence al programa P.I.E.?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "No", estilo['Normal']),   
        ))      
      
    if ficha.anio_pie == 0:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Año de pertencia programa P.I.E.?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "No registra año. ", estilo['Normal']),   
        ))
    else:
         data.append((
          
        Paragraph('<font size=10>%s</font>' % "Año de pertencia programa P.I.E.?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % ficha.anio_pie, estilo['Normal']),   
        )) 

    if ficha.habilidades == "True":         
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "¿Pertence al programa H.P.V?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "Sí", estilo['Normal']),   
        ))
    else:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "¿Pertence al programa H.P.V?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "No", estilo['Normal']),   
        ))

    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "IV. APRECIACIÓN DEL EQUIPO RESPECTO DE MOTIVO DE CONSULTA", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.cuatro, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "V. SEÑALE Y DESCRIBA LAS INTERVENCIONES PREVIAS FRENTE AL MOTIVO CONSULTA", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.cinco, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "CONDUCTA (elementos más destacables positivos y negativos)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.conducta, estilo['Normal']),   
    ))


    data.append((
      
    Paragraph('<font size=10>%s</font>' % "RENDIMIENTO (área de mayor y menos dificultad, repitencias)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.rendimiento, estilo['Normal']),   
    ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "ÁREA DE RESPONSABILIDAD( asistencia, cumplimiendo de deberes)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.area_responsabilidad, estilo['Normal']),   
    ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Composición de la Familia (Genograma y tipo de relaciones)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.antecedentes_familiares, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Historia familiar (Antecedentes relevantes - Comportamiento figura de cuidado del estudiante - Situación social ej: vulneración de derecho, VIF, Presencia de  alcohol y/o droga )", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.seis, estilo['Normal']),   
    ))
   # if ficha.observacion != "Sin observación":
   #     data.append((
          
   #     Paragraph('<font size=10>%s</font>' % "Petición de información", estilo['Normal']),
   #     Paragraph('<font size=10>%s</font>' % ficha.observacion, estilo['Normal']),   
   #     ))
   # else:
   #     data.append((
          
   #     Paragraph('<font size=10>%s</font>' % "Petición de información", estilo['Normal']),
   #     Paragraph('<font size=10>%s</font>' % "Sin petición de información adicional", estilo['Normal']),   
   #     ))



    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Establecimiento (Ficha)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.establecimiento, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Curso (Ficha):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.curso+" "+ficha.letra, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Edad (Ficha):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.edad, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Derivación (Institución  y/o Especialista):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.Red_apoyo, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Observación red apoyo", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.Red_apoyo_obs, estilo['Normal']),   
    ))

    


    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)
   

    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     

    
    
    
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response

def fichaderivacion_pdf_report_historica(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)

        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Centro de Bienestar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "bienestardemcabildo@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()


    
    Title = "FICHA DE DERIVACIÓN"
    pageinfo = "Centro de Bienestar     Correo electónico: bienestardemcabildo@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))



    # Set up HttpResponse object
    #response = HttpResponse(mimetype='application/pdf')
    history=Historia.objects.get(pk=pk)
    ficha=history.Ficha_derivacion
    estudiante=ficha.Estudiante

    escolar=Escolaridad.objects.get(Estudiante__id=estudiante.id)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    
    

    filename="Ficha_derivacion_historica"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    
    Elements = []
    #doc = SimpleDocTemplate(response)


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Ficha de derivación",
    author="Centro de Bienestar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/encabezadocabildo.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))




    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    

    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional que deriva:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))



    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Motivo de la derivación:", estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % " Listado motivos indicados en Ficha derivación", estilo['Normal']),   
    ))

    for motivo in ficha.Motivo_derivacion.all():

        data.append((
        Paragraph('<font size=10>%s</font>' % " ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % motivo.nombre, estilo['Normal']),
    ))
   
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fecha de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.fecha_derivacion.strftime('%d/%m/%Y'), estilo['Normal']),   
    ))


    if ficha.pie:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "¿Pertence al programa P.I.E.?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "Sí", estilo['Normal']),   
        ))
    else:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "¿Pertence al programa P.I.E.?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "No", estilo['Normal']),   
        ))      
      
    if ficha.anio_pie==0:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "Año de pertencia programa P.I.E.?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "No registra año. ", estilo['Normal']),   
        ))
    else:
         data.append((
          
        Paragraph('<font size=10>%s</font>' % "Año de pertencia programa P.I.E.?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % ficha.anio_pie, estilo['Normal']),   
        )) 

    if ficha.habilidades:          
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "¿Pertence al programa H.P.V?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "Sí", estilo['Normal']),   
        ))
    else:
        data.append((
          
        Paragraph('<font size=10>%s</font>' % "¿Pertence al programa H.P.V?:", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "No", estilo['Normal']),   
        ))

    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "IV. APRECIACIÓN DEL EQUIPO RESPECTO DE MOTIVO DE CONSULTA", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.cuatro, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "V. SEÑALE Y DESCRIBA LAS INTERVENCIONES PREVIAS FRENTE AL MOTIVO CONSULTA", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.cinco, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "CONDUCTA (elementos más destacables positivos y negativos)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.conducta, estilo['Normal']),   
    ))


    data.append((
      
    Paragraph('<font size=10>%s</font>' % "RENDIMIENTO (área de mayor y menos dificultad, repitencias)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.rendimiento, estilo['Normal']),   
    ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "ÁREA DE RESPONSABILIDAD( asistencia, cumplimiendo de deberes)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.area_responsabilidad, estilo['Normal']),   
    ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Composición de la Familia (Genograma y tipo de relaciones)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.antecedentes_familiares, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Historia familiar (Antecedentes relevantes - Comportamiento figura de cuidado del estudiante - Situación social ej: vulneración de derecho, VIF, Presencia de  alcohol y/o droga )", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.seis, estilo['Normal']),   
    ))
   # if ficha.observacion != "Sin observación":
   #     data.append((
          
   #     Paragraph('<font size=10>%s</font>' % "Petición de información", estilo['Normal']),
   #     Paragraph('<font size=10>%s</font>' % ficha.observacion, estilo['Normal']),   
   #     ))
   # else:
   #     data.append((
          
   #     Paragraph('<font size=10>%s</font>' % "Petición de información", estilo['Normal']),
   #     Paragraph('<font size=10>%s</font>' % "Sin petición de información adicional", estilo['Normal']),   
   #     ))



    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Establecimiento (Ficha)", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.establecimiento, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Curso (Ficha):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.curso+" "+ficha.letra, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Edad (Ficha):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.edad, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Derivación (Institución  y/o Especialista):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.Red_apoyo, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Observación red apoyo", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.Red_apoyo_obs, estilo['Normal']),   
    ))

    


    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)
    
    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )
    
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response

# impresiones de la ficha de derivacion de las duplas es decir interna dentro del establecimiento
def fichaderivacion_dupla_pdf_report(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Equipo de formación y convivencia escolar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)

        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Equipo de formación y convivencia escolar ")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()


    
    Title = "FICHA DE DERIVACIÓN INTERNA"
    pageinfo = "Convivencia     Correo electónico: convivenciaescolar@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))



    # Set up HttpResponse object
    #response = HttpResponse(mimetype='application/pdf')
   
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    ficha=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk)
    

    filename="Ficha_derivacion_interna"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    
    Elements = []
    #doc = SimpleDocTemplate(response)


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Ficha de derivación interna",
    author="Convivencia Escolar ",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
        
    #imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/logo_formacion_convivencia.jpg',width=490,height=40)
    
    #Elements.append(imagen_logo)
    # cambie para el proceso del logo
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)    
    
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))






    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    

    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional dupla:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional derivante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.quien_deriva, estilo['Normal']),
    ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesor jefe:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.profe_jefe, estilo['Normal']),
    ))



    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Motivo de la derivación:", estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % " Listado motivos indicados en Ficha derivación", estilo['Normal']),   
    ))

    for motivo in ficha.Motivo_derivacion_dupla.all():

        data.append((
        Paragraph('<font size=10>%s</font>' % " ", estilo['Normal']),    
        Paragraph('<font size=10>%s</font>' % motivo.nombre, estilo['Normal']),
    ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fecha de la derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.fecha_derivacion.strftime('%d/%m/%Y'), estilo['Normal']),   
    ))

    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "¿ LA CONDUCTA IDENTIFICADA, AFECTA EL PROCESO DE ENSEÑANZA-APRENDIZAJE DEL ESTUDIANTE", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.conducta, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "¿COMO AFECTA?", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.afecta, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "¿ DESDE CUÁNDO SE REITERA LA CONDUCTA?", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.reiterada, estilo['Normal']),   
    ))


    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Observación General", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.observacion, estilo['Normal']),   
    ))
   

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Inasistencias Marzo/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.marzo+" ", estilo['Normal']), 

    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Inasistencias Abril/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.abril+" ", estilo['Normal']), 

    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Inasistencias Mayo/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.mayo+" ", estilo['Normal']), 

    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Inasistencias Junio/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.junio+" ", estilo['Normal']), 

    ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Inasistencias Julio/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.julio+" ", estilo['Normal']), 

    ))

    data.append((
      
    Paragraph('<font size=8>%s</font>' % "Inasistencias Agosto/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % ficha.agosto+" ", estilo['Normal']), 

    ))

    data.append((
      
    Paragraph('<font size=8>%s</font>' % "Inasistencias Septiembre/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % ficha.septiembre+" ", estilo['Normal']), 

    ))

    data.append((
      
    Paragraph('<font size=8>%s</font>' % "Inasistencias Octubre/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % ficha.octubre+" ", estilo['Normal']), 

    ))

    data.append((
      
    Paragraph('<font size=8>%s</font>' % "Inasistencias Noviembre/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % ficha.noviembre+" ", estilo['Normal']), 

    ))

    data.append((
      
    Paragraph('<font size=8>%s</font>' % "Inasistencias Dicembre/"+str(int(ficha.fecha_derivacion.year)), estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % ficha.diciembre+" ", estilo['Normal']), 

    ))

    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)
    Elements.append(Spacer(0,15))
    data = [ [ 'Profesional'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 1 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     

    
    

        
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response



# ----------- Entrevista de engreso 

# impresiones de la ficha de derivacion de las duplas es decir interna dentro del establecimiento
def entrevistaingreso_dupla_pdf_report(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Convivencia escolar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)

        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Formación y Convivencia ")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()


    
    Title = "ENTREVISTA DE INGRESO"
    pageinfo = "Convivencia     Correo electónico: convivenciaescolar@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))



    # Set up HttpResponse object
    #response = HttpResponse(mimetype='application/pdf')
   
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    
    ficha_dupla=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk,estado=1)
    ficha=Entrevista_ingreso_dupla.objects.get(ficha_derivacion_dupla=ficha_dupla)
    filename="Entrevista_Ingreso"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    
    Elements = []
    #doc = SimpleDocTemplate(response)


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Entrevista de ingreso",
    author="Convivencia Escolar ",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    
    #imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/logo_formacion_convivencia.jpg',width=490,height=40)

    #Elements.append(imagen_logo)
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))




    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
        
    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional dupla:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional derivante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha_dupla.quien_deriva, estilo['Normal']),
    ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesor jefe:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha_dupla.profe_jefe, estilo['Normal']),
    ))


    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fecha Entrevista de ingreso:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.fecha_derivacion.strftime('%d/%m/%Y'), estilo['Normal']),   
    ))

    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "I. ANTEDECENTES FAMILIARES - Composición de la Familia( Genograma y tipo de relaciones", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.familia, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "II. PROBLEMATICA -  Apreciación de la posible problemática de análisis ( Posibles causas o factores, indicadores presenres y ámbitos afectados  - social - educacional - familiar", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.problematica, estilo['Normal']),   
    ))

    
  
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)
    Elements.append(Spacer(0,15))
    data = [ [ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     

    
    

        
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response    

# Ficha de egreso estudiante dupla
# impresiones de la ficha de derivacion de las duplas es decir interna dentro del establecimiento
def fichaegreso_dupla_pdf_report(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(200, inch, "Convivencia escolar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)

        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(200, inch, "Convivencia escolar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()


    
    Title = "FICHA DE EGRESO"
    pageinfo = "Convivencia     Correo electónico: convivenciaescolar@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))



    # Set up HttpResponse object
    #response = HttpResponse(mimetype='application/pdf')
   
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    ficha=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk,estado=1)
    egreso=Derivacion_Ficha_derivacion_dupla.objects.get(ficha_derivacion_dupla=ficha,estado=1)
    

    filename="Ficha_egreso"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    
    Elements = []
    #doc = SimpleDocTemplate(response)


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Ficha de derivación interna",
    author="Convivencia Escolar ",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)

    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    #imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/logo_formacion_convivencia.jpg',width=490,height=40)
    #Elements.append(imagen_logo)
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))


    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    

    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional dupla:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fecha:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % egreso.fecha_derivacion.strftime('%d/%m/%Y'), estilo['Normal']),   
    ))

    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Observaciones", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % egreso.observacion_termino, estilo['Normal']),   
    ))
    
    data.append((
    
    Paragraph('<font size=10>%s</font>' % "Motivo ", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % egreso.motivo, estilo['Normal']),   
    ))

    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)
    Elements.append(Spacer(0,15))
    data = [ [ 'Meses'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )          
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response

    # Ficha de egreso estudiante dupla
# impresiones de la ficha de derivacion de las duplas es decir interna dentro del establecimiento
def fichacontinuidad_dupla_pdf_report(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(200, inch, "Formación y convivencia escolar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)

        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(200, inch, "Formación y convivencia escolar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()


    
    Title = "FICHA CONTINUIDAD"
    pageinfo = "Convivencia     Correo electónico: convivenciaescolar@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))



    # Set up HttpResponse object
    #response = HttpResponse(mimetype='application/pdf')
   
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    ficha=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk,estado=1)
    continuidad=Continuidad_dupla.objects.get(ficha_derivacion_dupla=ficha)
    

    filename="Ficha_continuidad"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    
    Elements = []
    #doc = SimpleDocTemplate(response)


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Ficha continuidad",
    author="Convivencia Escolar ",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/logo_formacion_convivencia.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))

    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
                
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    

    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional dupla:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % ficha.usuario.first_name+" "+ficha.usuario.last_name, estilo['Normal']),
    ))

    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fecha derivación:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % ficha.fecha_derivacion.strftime('%d/%m/%Y'), estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Fecha continuidad:", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % continuidad.fecha.strftime('%d/%m/%Y'), estilo['Normal']),   
    ))

    data.append((
        
        Paragraph('<font size=10>%s</font>' % "", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % "Motivo de la continuidad ", estilo['Normal']),
        
        ))
    for motivo in continuidad.motivo_continuidad.all():      
        data.append((
        
        Paragraph('<font size=10>%s</font>' % "", estilo['Normal']),
        Paragraph('<font size=10>%s</font>' % motivo.nombre, estilo['Normal']),   
        ))
    
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Observación (Especifique motivo) ", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % continuidad.observacion, estilo['Normal']),   
    ))
    
    
    

    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)
    Elements.append(Spacer(0,15))
    data = [ [ 'Meses'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     
        
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response

# Informe de derivacion de duplas ficha de derivacion
def fichaderivacionegresodupla_pdf_report(request,pk):
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]

    styles = getSampleStyleSheet()

    #Definimos las caracteristicas fijas de la primera página
    def myFirstPage(canvas, doc):
        canvas.saveState()
        #canvas.setFont('Times-Roman', 9)
        #canvas.drawString(inch, 0.75 * inch, "%s  %s" %(doc.page,pag))
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 108, Title)
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Convivencia escolar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)

        canvas.restoreState()

    #Definimos disposiciones alternas para las caracteristicas de las otras páginas
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
       # canvas.drawString(inch, 0.75 * inch, " %d  %s" %(doc.page, pageinfo))
        canvas.drawString(230, inch, "Convivencia escolar")
        canvas.setFont('Times-Bold', 12)
        canvas.drawString(200,  inch-12, "convivenciaescolar@gmail.com")
        canvas.line(100, inch+10 ,500,inch+10)
        canvas.restoreState()


    
    Title = "FICHA DE DERIVACIÓN"
    pageinfo = "Convivencia escolar     Correo electónico: convivenciaescolar@gmail.com. "
    #Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate("test.pdf")
    #Iniciamos el story para los registros
    Elements = [Spacer(0, 80)]

    estilo_centrado=getSampleStyleSheet()
    estilo_centrado.add(ParagraphStyle(name = "ejemplo",  alignment=TA_CENTER, fontSize=12,
           fontName="Helvetica-BoldOblique"))



    # Set up HttpResponse object
    #response = HttpResponse(mimetype='application/pdf')
   
   
    estudiante=Estudiante.objects.get(id=pk)
    escolar=Escolaridad.objects.get(Estudiante__id=pk)
    nivel=escolar.get_curso()
    letra=escolar.get_Letra()
    ficha=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk,estado=1)
    deriva=Derivacion_Ficha_derivacion_dupla.objects.get(ficha_derivacion_dupla=ficha)
    print deriva
    filename="Ficha_derivacion_dupla_y-oegreso"+estudiante.nombres+"_"+estudiante.firs_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    
    Elements = []
    #doc = SimpleDocTemplate(response)


    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    showBoundary=0,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch,
    allowSplitting=1,
    title="Ficha de derivación y/o egreso",
    author="Convivencia escolar",
    onPage='encabezado',  # Por lo general es usado como encabezado
    onPageEnd='pie',  # Por lo general es usado como pie de página


)


    estilo = getSampleStyleSheet()
    estiloHoja = getSampleStyleSheet()
    cabecera = estiloHoja['Heading4']
    
    imagen_logo = Image(settings.MEDIA_ROOT+'/imagenes/logo_formacion_convivencia.jpg',width=490,height=40)

    Elements.append(imagen_logo)
    
    
    parrafo = Paragraph("",cabecera)
    Elements.append(parrafo)
   
    Elements.append(Spacer(0,8))
    Elements.append(Spacer(0,8))




    # Registros
    data=[]
    data.append((
    Paragraph('<font size=10>%s</font>' % "Estudiante:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.nombres.capitalize()+" "+estudiante.firs_name.capitalize()+" "+estudiante.last_name.capitalize(), estilo['Normal']),
    
            
            ))

    data.append((
    Paragraph('<font size=10>%s</font>' % "Establecimiento:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.establecimiento, estilo['Normal']),
    ))
    data.append((
    Paragraph('<font size=10>%s</font>' % "Curso:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.curso.get_numero()+" "+estudiante.curso.get_letra(), estilo['Normal']),
    ))
    

    data.append((
    Paragraph('<font size=10>%s</font>' % "Edad:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % estudiante.edad, estilo['Normal']),
    ))

    
    data.append((
    Paragraph('<font size=10>%s</font>' % "Profesional que deriva:", estilo['Normal']), 
    Paragraph('<font size=10>%s</font>' % deriva.usuario.first_name+" "+deriva.usuario.last_name, estilo['Normal']),
    ))



    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Motivo de la derivación:", estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % deriva.get_motivo_termino(), estilo['Normal']),   
    ))

    data.append((
          
    Paragraph('<font size=10>%s</font>' % "Motivo ", estilo['Normal']),
    Paragraph('<font size=8>%s</font>' % deriva.motivo, estilo['Normal']),       ))
 
    data.append((

      
    Paragraph('<font size=10>%s</font>' % "Fecha de derivación", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % deriva.fecha_derivacion, estilo['Normal']),   
    ))
    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Observación", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % deriva.observacion_termino, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "File 1 Nombre", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % deriva.filename1, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "File 2 Nombre", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % deriva.filename2, estilo['Normal']),   
    ))

    data.append((
      
    Paragraph('<font size=10>%s</font>' % "File 3 Nombre", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % deriva.filename3, estilo['Normal']),   
    ))


    data.append((
      
    Paragraph('<font size=10>%s</font>' % "Derivación (Institución  y/o Especialista):", estilo['Normal']),
    Paragraph('<font size=10>%s</font>' % deriva.Red_apoyo, estilo['Normal']),   
    ))

    
    table = Table(
        data,
        #colWidths=250 # Valor del ancho de las columnas
        colWidths=[130,390]
    )
    table.setStyle(
        TableStyle([
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
    )


    Elements.append(table)
   

    Elements.append(Spacer(0,15))
    data = [ [ 'PSICÓLOGO'+" "+ request.user.first_name+" "+request.user.last_name , 'FIRMA'   ] ,
        
        
        [ 'NOMBRE / QUIEN RECIBE EL INFORME' , 'FIRMA'   ] ,
  ] 
    t = Table ( data,30 * [ 3.599 * inch ] , 2 * [ 0.6 * inch ] ) 
    t. setStyle ( TableStyle ( [ ( 'VALIGN' , ( 1 , 1 ) , ( -2 , -2 ) , 'TOP' ) ,
                        ( 'VALIGN' , ( 0 , 0 ) , ( -1 , -1 ) , 'TOP' ) ,
                        ( 'TEXTCOLOR' , ( 0 , 0 ) , ( 0 , -1 ) , colors.black) ,
                        
                        
                        
                       
                        ( 'INNERGRID' , ( 0 , 0 ) , ( -1, -1 ) , 0.25 , colors.black ) ,
                        ( 'BOX' , ( 0 , 0 ) , ( -1 , -1 ) , 0.25 , colors.black ) ,
                        ] ) )
 
    Elements. append ( t )     

    
    
    
    Elements.append(Spacer(0,60))
    #Elements.append(table2)
    Elements.append(Spacer(0,20))
    doc.build(Elements, onFirstPage = myFirstPage, onLaterPages = myLaterPages)
    return response

# estructura reportalab hola mundo
def hello_pdf(request):
   


    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Certificado_para_escribir.pdf'

    temp = StringIO()

    # Create the PDF object, using the StringIO object as its "file."
    p = canvas.Canvas(temp)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")
    p.drawString(100, 100, "Hello world.")
    p.drawString(100, 100, "Hello world.")
    p.drawString(100, 100, "Hello world.")
    for var in Asl.objects.filter(generales=True):
        # creo variable p para guardar la descripcion
        p=Paragraph(var.descripcion, styles['Normal'])
        # añado a la lista la llave primaria de acl y ademas la descripcion contenida en p
        lista_acl.append((var.pk, p))
        detalle_orden=Table([encabezados] + lista_acl,colWidths=[70,400])

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the StringIO buffer and write it to the response.
    response.write(temp.getvalue())
    return response   

def pdf_export(request):
    id_cont=request.GET['id']
    filename="Contrato de CubanCloud_"+request.user.first_name+"_"+request.user.last_name+".pdf"
    # Creamos el response
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="%s"' % filename
    # Observa que ahora en vez de usar el nombre del archivo usamos el response
    doc=SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=2,
        bottomMargin=18,
    )
    Story=[]
    im=Image(settings.MEDIA_ROOT + '/logo.png', width=550, height=70)
    Story.append(im)
    styles=getSampleStyleSheet()
    datos1=Paragraph('NOMBRE Y APELLIDO(S) DEL CLIENTE: '+request.user.first_name+' '+request.user.last_name,styles['Normal'])
    datos2=Paragraph('NOMBRE DE USUARIO: '+request.user.username,styles['Normal'])
    Story.append(datos1)
    Story.append(datos2)
    datos3=Paragraph('E-MAIL: '+request.user.email,styles['Normal'])
    Story.append(datos3)
    noContrato=Paragraph('NO. CONTRATO: '+str(id_cont),styles['Normal'])
    Story.append(noContrato)
    p=Image(settings.MEDIA_ROOT+'/logo.png',width=550, height=30)
    Story.append(p)
    encabezados=('Servicios Contratados', 'ID.Servicio', 'Plan', 'Precio')
    lista_nombres=[]
    for var in agenda.objects.all():
        lista_nombres.append((var.fecha, var.pk, str(var.plazo) + " p", var.precio))
    lista_nombres.reverse()
    detalle_orden=Table([encabezados] + lista_nombres,colWidths=[170,100,100,100])
    # Aplicamos estilos a las celdas de la tabla
    detalle_orden.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            # # La primera fila(encabezados) va a estar centrada
            # ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            # # Los bordes de todas las celdas serán de color negro y con un grosor de 1
            # ('GRID', (0, 0), (-1, -1), 0, colors.transparent),
            # # El tamaño de las letras de cada una de las celdas será de 10
            # ('FONTSIZE', (0, 0), (0, 0), 10),

        ]
    ))
    Story.append(detalle_orden)
    p=Image(settings.MEDIA_ROOT + '/espacioPDF.png', width=550, height=30)
    Story.append(p)
    p=Paragraph('ACUERDOS DE NIVEL DE SERVICIOS',styles['Normal'])
    Story.append(p)
    encabezados=['No.', 'AsL']
    lista_acl=[]
    for var in Asl.objects.filter(generales=True):
        lista_acl.append((var.pk, var.descripcion))
    lista_acl.reverse()
    detalle_orden=Table([encabezados] + lista_acl,colWidths=[70,400,0])
    # Aplicamos estilos a las celdas de la tabla
    detalle_orden.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            # # La primera fila(encabezados) va a estar centrada
            # ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            # # Los bordes de todas las celdas serán de color negro y con un grosor de 1
            # ('GRID', (0, 0), (-1, -1), 0, colors.transparent),
            # # El tamaño de las letras de cada una de las celdas será de 10
            # ('FONTSIZE', (0, 0), (0, 0), 10),

        ]
    ))
    Story.append(detalle_orden)
    doc.build(Story)
    return response