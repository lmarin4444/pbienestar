# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#from __future__ import unicode_literals

from django.db import models
from alumno.models import Estudiante
from profesional.models import Profesional
from django.contrib.auth.models import User
from django import forms
from sesion.models import sesion


# Create your models here.


import datetime

ESTADO    = (
            (0,'Confirma asistencia'),
            (1,'Confirma inasistencia'),
            (2,'No contesta'),
            (3,'Apagado'),
            (4,'Ocupado'),
            (5,'Buzón de voz'),
            (6,'Número incorrecto'),
            (7,'Devuelve el llamado'),
            (8,'Devuelve el llamado otra persona confirma'),
            (9,'Devuelve el llamado otra persona o confirma'),
            (10,'Devuelve el llamado otra persona no sabe'),
            (11,'No se realizó el llamado'),


            )
SITUACION    = (
            (0,'No asiste'),
            (1,'No asiste, justifica posteriormente'),
            (2,'No asiste, avisa ausencia'),
            (3,'Asiste, este valor es automático'),
            (4,'Asiste, no se realiza sesión devido a que llega tarde'),
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
            

        
            
#proceso de confirmacion de asistencia en base a una sesion 

class fechas(object):
    """docstring for fechas"""
    fecha_desde = models.DateTimeField() 
    fecha_hasta = models.DateTimeField() 

        
class VacunaT(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.nombre)


class Pregunta(models.Model):

    TIPO_HORARIO = (
        ('09:00', '09:00'),
        ('09:30', '09:30'),
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('11:00', '11:00'),
        ('11:30', '11:30'),
        ('12:00', '12:00'),
        ('12:30', '12:30'),
        ('13:00', '13:00'),
        ('13:30', '13:30'),
        ('14:00', '14:00'),
        ('14:30', '14:30'),
        ('15:00', '15:00'),
        ('15:30', '15:30'),
        ('16:00', '16:00'),
        ('16:30', '16:30'),
        ('17:00', '17:00'),
        ('17:30', '17:30'),
        ('18:00', '18:00'),
        ('18:30', '18:30'),

        )

    
    texto_pregunta  = models.CharField(max_length=200)
    fe_publicacion  = models.DateField(null=True)
    Estudiante      = models.ForeignKey(Estudiante)
    Profesional     = models.ForeignKey(Profesional)
    fecha           = models.DateTimeField(null=True)
    horario_f       = models.CharField(max_length=20, choices=TIPO_HORARIO)
    horario_i       = models.CharField(max_length=20, choices=TIPO_HORARIO)
    obs             = models.CharField(max_length=100)
    usuario         = models.ForeignKey(User)
 
    def __str__(self):
        return self.texto_pregunta

    def publicada_recientemente(self, dias=1):
        return self.fe_publicacion >= timezone.now() - datetime.timedelta(days=dias)

    publicada_recientemente.admin_order_field = 'fe_publicacion'
    publicada_recientemente.boolean = True
    publicada_recientemente.short_description = '¿Publicada recientemente?'

      
    class Meta:
        ordering = ['-fe_publicacion']
    

class MascotaRA(models.Model):
	TIPO_HORARIO = (
        ('9:00', '9:00'),
        ('9:30', '9:30'),
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('11:00', '11:00'),
        ('11:30', '11:30'),
        ('12:00', '12:00'),
        ('12:30', '12:30'),
        ('13:00', '13:00'),
        ('13:30', '13:30'),
        ('14:00', '14:00'),
        ('14:30', '14:30'),
        ('15:00', '15:00'),
        ('15:30', '15:30'),
        ('16:00', '16:00'),
        ('16:30', '16:30'),
        ('17:00', '17:00'),
        ('17:30', '17:30'),
        ('18:00', '18:00'),
        ('18:30', '18:30'),

        )

	horario_i  = models.CharField(max_length=20, choices=TIPO_HORARIO)
	horario_f  = models.CharField(max_length=20, choices=TIPO_HORARIO)
	obs        = models.CharField(max_length=100)
	fecha      = models.DateField(null=True)
	Estudiante = models.ForeignKey(Estudiante)
	VacunaT    = models.ManyToManyField(VacunaT, blank=True)
	usuario    = models.ForeignKey(User)

	def __unicode__(self):
		return '{} {}'.format(self.Estudiante, self.fecha)	

class tipo_actividad(models.Model):
	
    Definicion = models.CharField(max_length=100)
    nombre     = models.CharField(max_length=50)
    def __str__(self):
        return '{}'.format(self.nombre)





class agenda(models.Model):
    PARTICIPANTES = (
        ('Estudiante ', ' Estudiante'),
        ('Adulto Responsable ', 'Adulto Responsable '),
        ('Estudiante - Mamá', 'Estudiante - Mamá'),
        ('Estudiante - Papá', 'Estudiante - Papá'),
        ('Estudiante - Mamá Papá o Padrastros', 'Estudiante - Mamá Papá o Padrastros'),
        ('Estudiante - Tía o Tío', 'Estudiante - Tía o Tío'),
        ('Estudiante - Abuelo o Abuela', 'Estudiante - Abuelo o Abuela'),
        ('Estudiante - Otro', 'Estudiante - Otro'),

        ('Reunión Adulto Responsable', 'Reunión Adulto Responsable'),
        ('Reunión Profesionales Dupla - Pie', 'Reunión Profesionales Dupla - Pie'),
        ('Reunión Profesionales Establecimiento', 'Reunión Profesionales Establecimiento'),
        ('Reunión Profesionales Centro', 'Reunión Profesionales Centro'),
        ('Reunión Otros', 'Reunión Otros'),
             
        )

    Estudiante      = models.ForeignKey(Estudiante)
    fecha           = models.DateField(null=True)
    
    horario_i       = models.IntegerField(choices=TIPO_HORARIO,default=0)
    participantes   = models.CharField(max_length=100, choices=PARTICIPANTES)
    tipo_actividad  = models.ForeignKey(tipo_actividad)
    usuario         = models.ForeignKey(User)
    numero          = models.IntegerField(blank=True, null=True)# 1: hora tomada 2:hora realizada 3:hora no asistida
    estado          = models.IntegerField(blank=True, null=True, default=1)# 1: hora por confirmar 2:hora confirmada
    
    def get_horario_i(self):
        return u'%s' % TIPO_HORARIO[self.horario_i][1]
    def __str__(self):
		return '{} {} {} {}'.format( self.id,self.Estudiante,self.fecha,self.horario_i)

class Confirma(models.Model):
    
    fecha           = models.DateTimeField(auto_now_add=True)
    fecha_confirma  = models.DateField()
    estado1         = models.IntegerField(choices=ESTADO)
    estado2         = models.IntegerField(choices=ESTADO, blank=True, null=True)
    estado3         = models.IntegerField(choices=ESTADO, blank=True, null=True)
    obs             = models.CharField(max_length=100)
    agenda          = models.ForeignKey(agenda)
    usuario         = models.ForeignKey(User)
    Estudiante      = models.ForeignKey(Estudiante)

    
    def get_estado1(self):
        return u'%s' % ESTADO[self.estado1][1]
    def get_estado2(self):
        return u'%s' % ESTADO[self.estado2][1]
    def get_estado3(self):
        return u'%s' % ESTADO[self.estado3][1]

    def __str__(self):
        return '{} {} {}  '.format(self.fecha_confirma, self.estado1,self.estado2)

class  Registro(models.Model):
    """docstring for  Registro"""
#este es el archivo que almacena el registro de asistencia de los estudiantes a las sesiones
    fecha           = models.DateField()   
    agenda          = models.ForeignKey(agenda)
    Estudiante      = models.ForeignKey(Estudiante)
    situacion       = models.IntegerField(choices=SITUACION)
    obs             = models.TextField(blank=True, null=True)
    otros           = models.TextField(blank=True, null=True)#Agregar informacion sobre inacistencia extra
    usuario         = models.ForeignKey(User)

    #usuario         = models.ForeignKey(User)          
    def get_situacion(self):
        return u'%s' % SITUACION[self.situacion][1]

    def __str__(self):
        return '{} {} {}'.format(self.id,self.fecha, self.usuario.username)
        
class Reserva(models.Model):
	"""docstring for reserva"""
	fecha_entrada  = models.DateField
	fecha_salida   = models.DateField
