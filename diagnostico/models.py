# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from alumno.models import establecimiento
from dupla.models import Dimensiones
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.
AMBITO = (

        (0,'DIAGNOSTICO'),
        (1,'PLAN DE GESTION'),
		(2,'TALLER'), 
        (3,'ATENCION DE CASOS'),               
        (4,'CONTINGENCIA'),               
        )

TIPO_ACTIVIDAD   = (
        
        (0,'PLANIFICACION'),
        (1,'APLICACION DE ENCUESTAS'),
        (2,'FOCUS GROUP'),
        (3,'EJECUTAR'),
        (4,'ANALIZAR'),
        (5,'CONFECCIONAR'),
        (6,'PLANIFICACION ANUAL'),
        (7,'PLANIFICACION MENSUAL'),
        (8,'EJECUCION'),
        (9,'CREAR FICHA DERIVACION INTERNA'),
        (10,'CREAR FICHA DERIVACION CENTRO DE BIENESTAR'),
        (11,'CREAR ENTREVISTA DE INGRESO'),
        (12,'ENTREVISTA  APODERADO'),
        (13,'ENTREVISTA  PROFESOR'),
        (14,'ENTREVISTA  DIRECTIVO'),
        (15,'REUNION ESTABLECIMIENTO'),
        (16,'REUNION CENTRO BIENESTAR'),
        (17,'REUNION ENTIDAD EXTERNA'),
        (18,'ACCION PROPIA DEL ESTABLECIMIENTO'),
            )
        
PARTICIPANTES = (

        (1,'PSICOLOGO'),
        (2,'TRABAJADOR SOCIAL'),   
        (3,'EQUIPO DE FORMACION Y CONVIVENCIA ESCOLAR'),
        (4,'APODERADO'),
        (5,'ESTUDIANTE '),
        (6,'ESTUDIANTE - APODERAD0'),

        (7,'EQUIPO PSICOSOCIAL'),
        (8,'EQUIPO PSICOSOCIAL - ESTUDIANTE'),
        (9,'EQUIPO PSICOSOCIAL - APODERADO'),

        (10,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO'),
        (11,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO - PROFESOR JEFE'),
        (12,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO - PROFESOR '),
        
        (13,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO -DIRECTOR'),
        (14,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO -DIRECTOR PROFESOR JEFE'),
        (15,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO -DIRECTOR PROFESOR'),

        (16,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO -DIRECTIVOS'),
        (17,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO -DIRECTIVOS - PROFESOR JEFE'),
        (18,'EQUIPO PSICOSOCIAL - ESTUDIANTE - APODERADO -DIRECTIVOS - PROFESOR'),

        (19,'ENCARGADO DE CONVIVENCIA'),
        (20,'PSICOLOGO'),
        (21,'TRABAJADOR SOCIAL'),
        (22,'ENCARGADO DE CONVIVENCIA - PSICOLOGO'),
        (23,'ENCARGADO DE CONVIVENCIA - TRABAJADOR SOCIAL'),

        (24,'ENCARGADO DE CONVIVENCIA - PSICOLOGO - ESTUDIANTE'),
        (25,'ENCARGADO DE CONVIVENCIA - TRABAJADOR SOCIAL - ESTUDIANTE'),

        (26,'ENCARGADO DE CONVIVENCIA - PSICOLOGO - APODERADO'),
        (27,'ENCARGADO DE CONVIVENCIA - TRABAJADOR SOCIAL - APODERADO'),

        (28,'ENCARGADO DE CONVIVENCIA - PSICOLOGO - ESTUDIANTE - APODERADO'),
        (29,'ENCARGADO DE CONVIVENCIA - TRABAJADOR SOCIAL - ESTUDIANTE - APODERADO'),

        (30,'PROFESOR JEFE'),
        (31,'PROFESOR JEFE - ESTUDIANTE'),
        (32,'PROFESOR JEFE - APODERADO'),
        (33,'PROFESOR JEFE - ESTUDIANTE - APODERADO'),
        (34,'PROFESOR JEFE - ESTUDIANTE'),

        (35,'PROFESOR '),
        (36,'PROFESOR  - APODERADO'),
        (37,'PROFESOR  - ESTUDIANTE - APODERADO'),
        (38,'PROFESOR  - ESTUDIANTE - APODERADO -DIRECTOR'),
        (39,'PROFESOR  - ESTUDIANTE - APODERADO -DIRECTIVOS'),

        (40,'DIRECTOR'),
        (41,'DIRECTOR - PROFESOR JEFE'),
        (42,'DIRECTOR - PROFESOR'),
		(43,'DIRECTIVO'),
        (44,'ASISTENTE DE LA EDUCACION'),
        (45,'INSPECTOR '),
        (46,'INSPECTOR - ESTUDIANTE '),
        (47,'INSPECTOR - APODERADO'),
        (48,'INSPECTOR - ESTUDIANTE - APODERADO'),


		)

CURSO	 = (
        (0, 'NT1'),
        (1, 'KINDER (NT2)'),
        (2, '1º'),
        (3, '2º'),
        (4, '3º'),
        (5, '4º'),
        (6, '5º'),
        (7, '6º'),
        (8, '7º'),
        (9, '8º'),
        (10, '1 MEDIO'),
        (11, '2 MEDIO'),
        (12, '3 MEDIO'),
        (13, '4 MEDIO'),
        (14, 'MULTIGRADO'),


        )

TIPO_LETRAS = (
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D'),
        (4, 'E'),

        )

HORARIO = (

        (0,'08:00'),
        (1,'08:15'),
        (2,'08:30'),
        (3,'08:45'),
        (4,'09:00'),
        (5,'09:15'),
        (6,'09:30'),
        (7,'09:45'),
        (8,'10:00'),
        (8,'1O:15'),
        (10,'10:30'),
        (11,'10:45'),
        (12,'11:00'),
        (13,'11:15'),
        (14,'11:30'),
        (15,'11:45'),
        (16,'12:00'),
        (17,'12:15'),
        (18,'12:30'),
        (19,'12:45'),
        (20,'13:00'),
        
        (17,'13:15'),
        (18,'13:30'),
        (19,'13:45'),
        (20,'14:00'),
        
        (17,'14:15'),
        (18,'14:30'),
        (19,'14:45'),
        (20,'15:00'),
        
        (17,'15:15'),
        (18,'15:30'),
        (19,'15:45'),
        (20,'16:00'),
        
        (17,'16:15'),
        (18,'16:30'),
        (19,'16:45'),
        (20,'17:00'),
        
        (17,'17:15'),
        (18,'17:30'),
        (19,'17:45'),
        (20,'18:00'),
        
        (17,'18:15'),
        (18,'18:30'),
        (19,'18:45'),
        (20,'19:00'),
        
        (17,'19:15'),
        (18,'19:30'),
        (19,'19:45'),
        (20,'20:00'),
        )


class Diagnostico_Institucional(models.Model):
    
	day  = timezone.now()
	hour = timezone.now()
	    #formatedHour = hour.strftime("%Y/%m/%d %H:%M:%S")
	formatedDay  		= day.strftime("%Y/%m/%d")
	annio             	= models.IntegerField(default=2019)
	fecha               = models.DateField()
	objetivo_general 	= models.TextField(blank=True,null=True)
	objetivo_especifico = models.TextField(blank=True,null=True)
   
	participantes       = models.IntegerField(choices=PARTICIPANTES, blank=True, null=True)
	obs_partipantes		= models.TextField(blank=True,null=True)
	establecimiento     = models.ForeignKey(establecimiento,blank=True, null=True)
	desarrollo          = models.TextField(blank=True, null=True) 
	usuario             = models.ForeignKey(User)  

	def get_participantes(self):
		return u'%s' %PARTICIPANTES[self.participantes][1]
	def __unicode__(self):
		return '{} {}'.format(self.fecha,self.establecimiento)  
    
class Diagnostico_Institucional_curso(models.Model):
    
	curso               		= models.IntegerField(choices=CURSO, blank=True, null=True)
	tipo_letras         		= models.IntegerField(choices=TIPO_LETRAS, blank=True, null=True)
	participantes          		= models.TextField(blank=True, null=True) 
	establecimiento     		= models.ForeignKey(establecimiento,blank=True, null=True)
	desarrollo          		= models.TextField(blank=True, null=True) 
	Diagnostico_Institucional 	= models.ForeignKey(Diagnostico_Institucional)        
	usuario             		= models.ForeignKey(User)  

	def get_curso(self):
		return u'%s' %CURSO[self.curso][1]
	def get_tipo_letras(self):
		return u'%s' %TIPO_LETRAS[self.tipo_letras][1]    
        
	def __unicode__(self):
		return '{} {}'.format(self.curso,self.tipo_letras)  
           

class Diagnostico_Institucional_curso_indicador(models.Model):
     

	enfoque		          		= models.TextField(blank=True, null=True) 
	Diagnostico_Institucional 	= models.ForeignKey(Diagnostico_Institucional)
	Dimensiones        			= models.ForeignKey(Dimensiones)
	usuario             		= models.ForeignKey(User)  

	def get_curso(self):
		return u'%s' %CURSO[self.curso][1]
	def get_tipo_letras(self):
		return u'%s' %TIPO_LETRAS[self.tipo_letras][1]    
        
	def __unicode__(self):
		return '{}'.format(self.enfoque)  

