# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from multiselectfield import MultiSelectField
from django.db import models
from django.utils.timezone import get_current_timezone
from django.utils.functional import lazy
from django.utils.timezone import localtime, now
from datetime import datetime

from django.contrib.auth.models import User
from alumno.models import Estudiante
from profesional.models import Profesional
from derivacion.models import Ficha_derivacion



def get_timezone_aware_now_date():
    return localtime(now()).date()
# Create your models here.

TIPO_CHOICES = (
        (0, 'Estudiante'),
        (1, 'Adulto responsable'),
        (2, 'Estudiante - Mamá'),
        (3, 'Estudiante - Papá'),
        (4, 'Estudiante - Mamá y Papá o Padrastros'),
        (5, 'Estudiante - Hermano o Hermana'),
        (6, 'Estudiante - Tío o Tía'),
        (7, 'Estudiante - Abuelo o Abuela'),
        (8, 'Estudiante -  Otro'),
        (9, 'Reunión Adulto Responsable'),
        (10,'Reunión Profesionales (Dupla)'),
        (11,'Reunión Profesionales (Pie)'),
        
        (12, 'Reunión Profesionales Establecimiento (Profesores)'),
        (13, 'Reunión Profesionales Establecimiento'),
        
        (14, 'Reunión Profesionales Centro'),
        (15, 'Reunión Otros'),
        (16, 'Participación en Taller'),

        )

TIPO = (
        (0, 'Reunión '),
        (1, 'Visita domiciliaria'),
        (2, 'Conversación con el apoderado'),
        (3, 'Seguimiento personal'),

        
        )

MOTIVO = (
        (0, 'Se encuentra en proceso de evaluación'),
        (1, 'No ha terminado el proceso de intervención'),
        
        )

TIPO_HORARIO = (
        (0, '09:00'),
        (1, '09:10'),
        (2, '09:20'),
        (3, '09:30'),
        (4, '09:40'),
        (5, '09:50'),
        
        (6, '10:00'),
        (7, '10:10'),
        (8, '10:20'),
        (9, '10:30'),
        (10, '10:40'),
        (11, '10:50'),

        (12, '11:00'),
        (13, '11:10'),
        (14, '11:20'),
        (15, '11:30'),
        (16, '11:40'),
        (17, '11:50'),

        (18, '12:00'),
        (19, '12:10'),
        (20, '12:20'),
        (21, '12:30'),
        (22, '12:40'),
        (23, '12:50'),

        (24, '13:00'),
        (25, '13:10'),
        (26, '13:20'),
        (27, '13:30'),
        (28, '13:40'),
        (29, '13:50'),

        (30, '14:00'),
        (31, '14:10'),
        (32, '14:20'),
        (33, '14:30'),
        (34, '14:40'),
        (35, '14:50'),

        (36, '15:00'),
        (37, '15:10'),
        (38, '15:20'),
        (39, '15:30'),
        (40, '15:40'),
        (41, '15:50'),

        (42, '16:00'),
        (43, '16:10'),
        (44, '16:20'),
        (45, '16:30'),
        (46, '16:40'),
        (47, '16:50'),

        (48, '17:00'),
        (49, '17:10'),
        (50, '17:20'),
        (51, '17:30'),
        (52, '17:40'),
        (53, '17:50'),

        (54, '18:00'),
        (55, '18:10'),
        (56, '18:20'),
        (57, '18:30'),

        )



# Los tipos de seguimiento dado que el seguimiento es tanto para la derivación 
# al centro de Bienestar o los casos de las duplas
TIPO_SEGUIMIENTO    = (
            (0,'Centro de bienestar'),
            (1,'Derivación Salud Mental'),
            (2,'Derivación OPD.'),
            (3,'Derivación PPF.'),
            (4,'Derivación Posta '),
            (5,'Derivación Otro'),
          

            )



class tipo_sesion(models.Model):
	nombre 		= models.CharField(max_length=100)
	participantes 	= models.PositiveIntegerField(default = 0)
	observacion = models.CharField(max_length=100)

	def __unicode__(self):
		return '{}'.format(self.nombre)
class pruebas(models.Model):
	nombre 			= models.CharField(max_length=100)
	caracteristicas = models.CharField(max_length=100)
	observacion 	= models.CharField(max_length=100)
	def __unicode__(self):
		return self.nombre	

class Tematicas(models.Model):
	nombre 			= models.CharField(max_length=100)
	descripcion 	= models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.nombre

class sesion(models.Model):
	numero			= models.IntegerField(default=0)
	
	horario_i       = models.IntegerField(choices=TIPO_HORARIO)
	fecha 			= models.DateField()
	publico 		= models.TextField(blank=True,null=True)
	privado			= models.TextField(blank=True,null=True)
	observacion 	= models.TextField(blank=True,null=True)
	#participantes = models.CharField(max_length=50, choices=TIPO_CHOICES, blank=True, null=True)
	participantes 	= models.PositiveIntegerField('Tipo_choices',choices=TIPO_CHOICES, default = 0)
	#participantes = models.IntegerField(choices=TIPO_CHOICES, blank=True, null=True)
	pruebas			= models.ForeignKey(pruebas,default="No aplica pruebas")	
	tipo_sesion 	= models.ForeignKey(tipo_sesion)
	usuario 		= models.ForeignKey(User)
	Estudiante 		= models.ForeignKey(Estudiante)
	
	def __unicode__(self):
		return '{} {} {}'.format(self.Estudiante,self.observacion,self.publico)
	
	def get_participantes(self):
		return u'%s' % TIPO_CHOICES[self.participantes][1]
	def get_horario_i(self):
		return u'%s' % TIPO_HORARIO[self.horario_i][1]		

class Seguimiento(models.Model):
	
	fecha 			 		= models.DateField()
	observacion 			= models.CharField(max_length=100,blank = True)
	#participantes = models.CharField(max_length=50, choices=TIPO_CHOICES, blank=True, null=True)
	tipo_seg 				= models.PositiveIntegerField('Tipo_choices',choices=TIPO, default = 0)
	#participantes = models.IntegerField(choices=TIPO_CHOICES, blank=True, null=True)
	tipo_s 					= models.PositiveIntegerField('Tipo_choices',choices=TIPO_SEGUIMIENTO)
	usuario 				= models.ForeignKey(User)
	Estudiante 				= models.ForeignKey(Estudiante)
	
	def __unicode__(self):
		return '{} {} '.format(self.Estudiante,self.observacion)
	
	def get_tipo_seg(self):
		return u'%s' % TIPO[self.tipo_seg][1]
	def get_tipo_s(self):
		return u'%s' % TIPO_SEGUIMIENTO[self.tipo_s][1]	

class Diagnostico(models.Model):
	"""docstring for Diagnostico"""

	Estudiante 						= models.OneToOneField(Estudiante)
	fecha 							= models.DateField()
	situacion_actual		    	= models.TextField()
	observaciones		    		= models.TextField()
	familia				    		= models.TextField()
	usuario 						= models.ForeignKey(User)
	
	
	def __unicode__(self):
		return '{} {} '.format(self.Estudiante.nombres, self.fecha)
		
class Reporte_continuidad(models.Model):
	"""docstring for Diagnostico"""

	Estudiante 						= models.ForeignKey(Estudiante)
	fecha 							= models.DateField()
	motivo 							= models.PositiveIntegerField('Tipo_choices',choices=MOTIVO, default = 0)
	antecedentes		    		= models.TextField()
	observaciones					= models.TextField()
	sugerencias						= models.TextField()
	usuario 						= models.ForeignKey(User)
	
	
	def __unicode__(self):
		return '{} {} {} '.format(self.id,self.Estudiante.nombres, self.fecha)	
	def get_motivo(self):
		return u'%s' % MOTIVO[self.motivo][1]

class Motivo_egreso(models.Model):
	
	nombre						= models.TextField()
	descripcion					= models.TextField()
	
	
	def __unicode__(self):
			return self.nombre
class Ficha_de_egreso(models.Model):
	"""docstring for Diagnostico"""

	Estudiante 						= models.OneToOneField(Estudiante)
	fecha 							= models.DateField(auto_now=True)
	fecha_informe					= models.DateField()
	fecha_egreso 					= models.DateField()
	Motivo_egreso 					= models.ForeignKey(Motivo_egreso)
	sintesis 			    		= models.TextField()
	sugerencias						= models.TextField()
	usuario 						= models.ForeignKey(User)
	
	
	def __unicode__(self):
		return '{} {} '.format(self.Estudiante.nombres, self.fecha)	
	



class Intervenidos(models.Model):
	"""docstring for Intervenidos"""
	Estudiante 						= models.OneToOneField(Estudiante)
	fecha 							= models.DateTimeField('Fecha de creación',auto_now=True)
	fecha_intervencion				= models.DateField(blank=True,null=True)
	
	estado 							= models.TextField()
	sintesis				    	= models.TextField()
	usuario 						= models.ForeignKey(User)
	#datos de la derivacion
	fecha_derivacion				= models.DateField(blank=True,null=True)
	dia 							= models.CharField(max_length=2,blank = True)
	mes 							= models.CharField(max_length=2,blank = True)
	anno 							= models.CharField(max_length=4,blank = True)
#numero que indica si el PsicoloTratante es el iniicla 1 si es 2 sino
	numero 							= models.IntegerField(default=1)
#numero que indica si un estudiante esta activo o no, dado que cuando se derive a otra institucion
# no estara disponible en la bandeja de cada una de las profesionales
# pero si debe estar hasta que se decida egresar. 1:activo 2 : derivado a otra institucion 	
	activo							= models.IntegerField(default=1)
	Profesional 					= models.CharField(max_length=100,blank=True,null=True)		
	

	

	def __unicode__(self):
		return '{} {} {} {}'.format(self.Estudiante.nombres, self.fecha,self.estado,self.usuario)

class Pasos_intervencion(models.Model):
	Intervenidos 						= models.ForeignKey(Intervenidos)
	usuario 							= models.ForeignKey(User)
	fecha 								= models.DateTimeField('Fecha de creación',auto_now=True)
	fecha_pasos							= models.DateField(blank=True,null=True)
	observacion 						= models.TextField(blank=True,null=True)
	que_paso							= models.TextField(blank=True,null=True)

	def __unicode__(self):
			return '{} {} {}'.format(self.Intervenidos.Estudiante.nombres, self.fecha,self.observacion)

class objetivo_intervencion(models.Model):
	fecha 						= models.DateTimeField('Fecha de creacion',auto_now=True)
	fecha_creacion 				= models.DateField(blank=True)
	objetivo_particular			= models.TextField(blank=True,null=True)
	Tematicas 					= models.ManyToManyField(Tematicas)
	Estudiante					= models.ForeignKey(Estudiante)
	usuario 					= models.ForeignKey(User)
	#valor que indica si el objetivo esta activo o no
	activo						= models.IntegerField(default=1)
	
	def __unicode__(self):
		
		return '{} {} '.format(self.Estudiante, self.objetivo_particular)
#Para la construcciond de los informes 


#Para la historia Cambios en el objetivo de intervencion
class objetivo_intervencionhistoria(models.Model):
	fecha 						= models.DateTimeField('Fecha de creacion',auto_now=True)
	fecha_creacion 				= models.DateField(blank=True,null=True)
	objetivo_particular			= models.TextField(blank=True,null=True)
	Tematicas 					= models.TextField(blank=True,null=True)
	Estudiante					= models.ForeignKey(Estudiante)
	usuario 					= models.ForeignKey(User)

	
	def __unicode__(self):
			return self.objetivo_particular
class Estado(models.Model):
	Estado 						= models.TextField()
	Estudiante					= models.ForeignKey(Estudiante)
	fecha 						= models.DateTimeField('Fecha de creacion',auto_now=True)
	fecha_estado				= models.DateField(blank=True,null=True)

		



