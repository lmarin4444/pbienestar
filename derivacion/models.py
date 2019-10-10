# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from alumno.models import Estudiante
from alumno.models import curso 
from alumno.models import establecimiento
from alumno.models import Profesor
from profesional.models import Profesional
from alumno.models import Parentesco

from django.contrib.auth.models import User

BOOL_CHOICES = (
        ('True', 'Si'),
        ('False', 'No'),        
        )
OPCION = (
        (0, 'Si'),
        (1, 'No'),        
        )
# Los tipos de estado de un estudiante dentro del centro
ESTADO    = (
            (0,'Derivado'),
            (1,'Evaluación'),
            (2,'Lista de espera'),
            (3,'Intervención'),
            (4,'Derivado a otra institución'),
            (5,'Dado de alta'),
            (6,'Retornado a dupla'),
            (7,'Abandona la intervención por iniciativa propia'),
            (8,'Otro'),

            )

#Motivos de termino de una intervencion 
MOTIVO_TERMINO   = (
            (0,'Apoderado deserta de la atención'),
            (1,'No asiste regularmente'),
            (2,'Se cambia de institución '),
            (3,'Estudiante desvinculado por motivos personales '),
			(4,'Estudiante derivado a otra institución '), 
			(5,'Egresa del Centro de Bienestar '), 
			(6,'No cumple con el perfil '), 


            )
# Create your models here.	
class intervencion(models.Model):

	fecha 		=models.DateField(auto_now_add=True)
	observacion =models.CharField(max_length=100)
	Estudiante  =models.ForeignKey(Estudiante)
	atiende 	=models.ForeignKey(User)
	def __unicode__(self):
		return '{}'.format(self.Estudiante)

# Create your models here.
class Area_derivacion(models.Model):
	nombre 		= models.CharField(max_length=200)
	observacion = models.CharField(max_length=100)
	def __unicode__(self):
		return self.nombre	

class Motivo_derivacion(models.Model):
	nombre			= models.CharField(max_length=200)
	observacion 	= models.CharField(max_length=100)
	Area_derivacion = models.ForeignKey(Area_derivacion)
	def __unicode__(self):
		return self.nombre	

class Red_apoyo(models.Model):
	nombre 		= models.CharField(max_length=50)
	observacion = models.CharField(max_length=50)
	def __unicode__(self):
		return self.nombre	


class Ficha_derivacion(models.Model):
	
	fecha_derivacion 		= models.DateField()
	pie  			 		= models.CharField(max_length=20, choices=BOOL_CHOICES, blank=True, null=True)
	anio_pie				= models.IntegerField(default=0)
#Preguntas abiertas de la ficha de derivacion	


	habilidades		 		= models.CharField(max_length=20, choices=BOOL_CHOICES, blank=True, null=True)
	derivado     	 		= models.IntegerField(default=1)
	pasada 					= models.IntegerField(default=1)
	edad					= models.IntegerField(blank=True, null=True)
	edad_f					= models.IntegerField(blank=True, null=True)
#Preguntas abiertas de la ficha de derivacion	
	cuatro					= models.TextField()
	cinco					= models.TextField()
	conducta 				= models.TextField()
	rendimiento 			= models.TextField()
	area_responsabilidad	= models.TextField()
	antecedentes_familiares = models.TextField()
	seis					= models.TextField()
	observacion 			= models.TextField(default="Sin observación")
# datos que indican escolaridad del estudiante al momento de realizar la ficha de derivacion 
	establecimiento 		= models.CharField(max_length=50,blank=True, null=True)
	curso			 		= models.CharField(max_length=10,blank=True, null=True)
	letra			 		= models.CharField(max_length=2,blank=True, null=True)
# enlaces a los otros  modelos
	Estudiante 				= models.ForeignKey(Estudiante)	
	Motivo_derivacion		= models.ManyToManyField(Motivo_derivacion)
	usuario 				= models.ForeignKey(User)
	Red_apoyo 				= models.ForeignKey(Red_apoyo)
	Red_apoyo_obs			= models.TextField(default="Sin red de apoyo")
# Fecha de ingreso a lista de espera s
	fecha_espera			=models.DateField('Fecha de creacion',blank=True,null=True)

#estado indica si la ficha es actual o no estado=1 ficha activa otro valor ficha ya egresada
	estado 					= models.IntegerField(default=1)
#Imagen de la familia
	Imagen = models.ImageField(upload_to='imagenes/%Y/%m/%d',blank=True, null=True)
	def __unicode__(self):
		return '{} {} {}  '.format(self.id,self.fecha_derivacion,self.pie)	
	
	

class Motivo_Retorno_Ficha_derivacion(models.Model):

	motivo_termino 			= models.IntegerField(choices=MOTIVO_TERMINO)
	fecha_derivacion 		= models.DateField(auto_now_add=True)
	fecha_retorno			= models.DateField(blank=True, null=True)
	observacion_termino 	= models.TextField(blank=True, null=True)
	
	opcion1		 			= models.IntegerField(choices=OPCION,default=1)
	filename1 				= models.CharField(max_length=100,blank=True, null=True)
 	docfile1 				= models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
 	
 	opcion2		 			= models.IntegerField(choices=OPCION,default=1)
 	filename2 				= models.CharField(max_length=100,blank=True, null=True)
 	docfile2 			    = models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
 						   	
 	opcion3		 			= models.IntegerField(choices=OPCION,default=1)
 	filename3 				= models.CharField(max_length=100,blank=True, null=True)
 	docfile3 				= models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
 	
 	Ficha_derivacion 		= models.ForeignKey(Ficha_derivacion)
 	Red_apoyo				= models.ForeignKey(Red_apoyo,blank=True,null=True)
 	estado 					= models.IntegerField(default=1)

	

	def docfile1_link(self):
		if self.docfile1:
			return "<a href='%s'>download</a>" % (self.docfile1.url,)
		else:
			return "No attachment"

		docfile1.allow_tags = True
		
	def docfile2_link(self):
		if self.docfile2:
			return "<a href='%s'>download</a>" % (self.docfile2.url,)
		else:
			return "No attachment"

		docfile2.allow_tags = True

	def docfile3_link(self):
		if self.docfile3:
			return "<a href='%s'>download</a>" % (self.docfile3.url,)
		else:
			return "No attachment"

		docfile3.allow_tags = True
	

	def get_motivo_termino(self):
		return u'%s' % MOTIVO_TERMINO[self.motivo_termino][1]

	def __unicode__(self):
		return '{} {} {} '.format(self.id,self.Ficha_derivacion.Estudiante,self.observacion_termino)	
	

class Bitacora(models.Model):
	Estudiante 		= models.ForeignKey(Estudiante)
	fecha_bitacora	= models.DateField(auto_now_add=True)
	estado 			= models.IntegerField(choices=ESTADO, blank=True, null=True)
	tiposesion		= models.CharField(max_length=60,blank=True, null=True)
	nsesion			= models.IntegerField(blank=True, null=True)
	campo1			= models.CharField(max_length=60,blank=True, null=True)
	campo2			= models.CharField(max_length=60,blank=True, null=True)
	campo3			= models.CharField(max_length=60,blank=True, null=True)
	campo4			= models.CharField(max_length=60,blank=True, null=True)
	usuario 		= models.ForeignKey(User)
	
	#campos de detalle 
	def __unicode__(self):
		return '{} {} {} '.format(self.Estudiante, self.fecha_bitacora, self.estado)

	def get_estado(self):
		return u'%s' % ESTADO[self.estado][1]
	
class Tipo_atencion(models.Model):
	nombre 			 = models.CharField(max_length=12)
	observacion 	 = models.CharField(max_length=50)
	Ficha_derivacion = models.ForeignKey(Ficha_derivacion)

	
	def __unicode__(self):
		return self.nombre

class Retorno(models.Model):
	motivo_termino= models.IntegerField(choices=MOTIVO_TERMINO, blank=True, null=True)
	fecha_derivacion=models.DateField()
	observacion_termino=models.CharField(max_length=100)
	Ficha_derivacion = models.ForeignKey(Ficha_derivacion)

def get_motivo_termino(self):
		return u'%s' % MOTIVO_TERMINO[self.motivo_termino][1]

#Historia

#cambios de pie o de habilidadaes+ FICHA

#cambios en el establecimiento de los estudiantes ESTABLECIMIENTO




#cambios. en el profesional que los atiende 

