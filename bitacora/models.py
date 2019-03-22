# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from alumno.models import establecimiento
from plan.models import Planes_externos,Actividades
from dupla.models import Intervencion_convivencia,Intervencion_convivencia_mediacion
from dupla.models import Intervencion_sesion,Dimensiones
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.
AMBITO = (

        (0,'CONTINGENCIA'),  
        (1,'PLAN DE GESTIÓN'),
        (2,'ATENCIÓN DE CASOS'),               
        (3,'CONVIVENCIA ESCOLAR'),
        (4,'CONVIVENCIA ESCOLAR MEDIACION'),
                     
        )

TIPO_ACTIVIDAD   = (
        
       
        (0,'Contención'),
        (1,'Atención Apoderados / Profesores / otros'),
        (2,'Apoyo Estudiantes / Profesores / otros profesionales'),
        (3,'Apoyo Situación Médica'),
        (4,'Coordinación '),
        (5,'Construcción / informes '),
        (6,'Reuniones'),
        (7,'Capacitaciones'),
        (8,'Acción propia del establecimiento'),
        (9,'Celebraciones del establecimiento'),
        (10,'Fallas ( Agua - Luz - etc.'),
        (11,'Cambio de activivdades por desplanificación'),
        (12,'Acción Plan'),
        (13,'Atención de casos'),
        (14,'Acción convivencia escolar'),

        
            )
        
PARTICIPANTES = (
            
            (0,'Comunidad educativa'),
            (1,'Consejo escolar'),
            (2,'Estudiantes'),
            (3,'Centro de padres y/o Apoderados'),
            (4,'Consejo de profesores / Docentes / Asistentes de la educación '),
            (5,'Estudiantes mismo curso'),
            (6,'Estudiantes diferentes cursos '),
            (7,'Estudiantes / Docentes / Asistentes de la educación'),
            (8,'Estudiantes / Apoderados'),
            (9,'Estudiantes / Directivos'),
            (10,'Docentes / Apoderados'),
            (11,'Docentes /  Directivos'),
            (12,'Directivos / Estudiantes'),
            (13,'Directivos / Apoderados'),
            (14,'Directivos / Docentes'),
             
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
        (15, '-'),


        )

TIPO_LETRAS = (
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D'),
        (4, 'E'),
        (5, '-'),

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


class Lista(models.Model):
    
    day  = timezone.now()
    hour = timezone.now()
    #formatedHour = hour.strftime("%Y/%m/%d %H:%M:%S")
    formatedDay  = day.strftime("%Y/%m/%d")
    formatedHour = hour.strftime("%H:%M:%S")
    fecha               = models.DateField()
    horario             = models.IntegerField(choices=HORARIO)
    nombre              = models.CharField(max_length=100 )
    curso               = models.IntegerField(choices=CURSO, default=15)
    tipo_letras         = models.IntegerField(choices=TIPO_LETRAS, default=5)
    ambito              = models.IntegerField(choices=AMBITO,default=0)
    tipo_actividad      = models.IntegerField(choices=TIPO_ACTIVIDAD,default=0)
    participantes       = models.IntegerField(choices=PARTICIPANTES,default=2)
    establecimiento     = models.ForeignKey(establecimiento,blank=True, null=True)
    desarrollo          = models.TextField(blank=True, null=True) 
    planes_externos     = models.ForeignKey(Planes_externos,blank=True, null=True)
    numero              = models.IntegerField(default=1)
    # Numero = 1 accion sin ejecutar
    # Numero = 2 accion ejecutada 
    # Numero = 3 accion eliminada - suspendida - no ejecutada
    
    # Relación con los archivos externos 
    # Sesion : para la sesion de los estudiantes
    # Actividad para la actividad de los planes
    # Convivencia : relacion con las acciones de convivencia 
    # Las contigencias quedaran solo en la bitacora diaria de cada persona
    actividad           = models.ForeignKey(Actividades,blank=True, null=True)  
    sesion              = models.ForeignKey(Intervencion_sesion,blank=True, null=True)  
    convivencia         = models.ForeignKey(Intervencion_convivencia,blank=True, null=True)  
    mediacion           = models.ForeignKey(Intervencion_convivencia_mediacion,blank=True, null=True)  
    
    
    usuario             = models.ForeignKey(User)      
    dimensiones         = models.ForeignKey(Dimensiones,blank=True, null=True)

    
    def get_curso(self):
        return u'%s' %CURSO[self.curso][1]
    def get_tipo_letras(self):
        return u'%s' %TIPO_LETRAS[self.tipo_letras][1]
    def get_ambito(self):
        return u'%s' %AMBITO[self.ambito][1]
    def get_tipo_actividad(self):
        return u'%s' %TIPO_ACTIVIDAD[self.tipo_actividad][1]
    def get_participantes(self):
        return u'%s' %PARTICIPANTES[self.participantes][1]
    def get_horario(self):
        return u'%s' %HORARIO[self.horario][1]
    
    
        
    def __unicode__(self):
        return '{} {} {} {} {}'.format(self.tipo_actividad,self.id,self.fecha,self.nombre,self.horario)  
    
           


