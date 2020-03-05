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
            (11,'LLama el adulto responsable al Centro de Bienestar'),



            )
SITUACION    = (
            (0,'No asiste'),
            (1,'No asiste, justifica posteriormente'),
            (2,'No asiste, avisa ausencia'),
            (3,'Asiste, este valor es automático'),
            (4,'Asiste, no se realiza sesión devido a que llega tarde'),
            )
TIPO_HORARIO = (
        (0, '08:00'),
        (1, '08:10'),
        (2, '08:20'),
        (3, '08:30'),
        (4, '08:40'),
        (5, '08:50'),
        
        (6, '09:00'),
        (7, '09:10'),
        (8, '09:20'),
        (9, '09:30'),
        (10, '09:40'),
        (11, '09:50'),

        (12, '10:00'),
        (13, '10:10'),
        (14, '10:20'),
        (15, '10:30'),
        (16, '10:40'),
        (17, '10:50'),

        (18, '11:00'),
        (19, '11:10'),
        (20, '11:20'),
        (21, '11:30'),
        (22, '11:40'),
        (23, '11:50'),

        (24, '12:00'),
        (25, '12:10'),
        (26, '12:20'),
        (27, '12:30'),
        (28, '12:40'),
        (29, '12:50'),

        (30, '13:00'),
        (31, '13:10'),
        (32, '13:20'),
        (33, '13:30'),
        (34, '13:40'),
        (35, '13:50'),

        (36, '14:00'),
        (37, '14:10'),
        (38, '14:20'),
        (39, '14:30'),
        (40, '14:40'),
        (41, '14:50'),

        (42, '15:00'),
        (43, '15:10'),
        (44, '15:20'),
        (45, '15:30'),
        (46, '15:40'),
        (47, '15:50'),

        (48, '16:00'),
        (49, '16:10'),
        (50, '16:20'),
        (51, '16:30'),
        (52, '16:40'),
        (53, '16:50'),

        (54, '17:00'),
        (55, '17:10'),
        (56, '17:20'),
        (57, '17:30'),

        (58, '17:40'),
        (59, '17:50'),
        (60, '18:00'),
        (61, '18:10'),

        (62, '18:20'),
        (63, '18:30'),
        (64, '18:40'),
        (65, '18:50'),

        (66, '19:00'),
        (67, '19:10'),
        (68, '19:20'),
        (69, '19:30'),

        (70, '19:40'),
        (71, '20:00'),
        




        )
            
FURGON = (
        (0, 'No'),
        (1, 'Sí'),
        )
        
ACCION = (
        (0,'Sesión '),
        (1,'Reunión Centro Bienestar'),        
        (2,'Reunión establecimiento'),        
        (3,'Reunión duplas y/o equipos de convivencia'),        
        (4,'Jornadas'),        
        (5,'Ferias'),        
        (6,'Capacitación'),        
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
        return '{} '.format(self.nombre)





class agenda(models.Model):
    PARTICIPANTES = (
        ('Estudiante ', ' Estudiante'),
        ('Adulto Responsable ', 'Adulto Responsable '),
        ('Papá mamá ambos ', 'Papá mamá ambos '),
       
        ('Estudiante - Mamá', 'Estudiante - Mamá'),
        ('Estudiante - Papá', 'Estudiante - Papá'),
        ('Estudiante - Mamá Papá o Padrastros', 'Estudiante - Mamá Papá o Padrastros'),
        ('Estudiante - Tía o Tío', 'Estudiante - Tía o Tío'),
        ('Estudiante - Abuelo o Abuela', 'Estudiante - Abuelo o Abuela'),
        ('Estudiante - Otro', 'Estudiante - Otro'),

        ('Dupla Psicosocial y/o Pie', 'Dupla Psicosocial y/o Pie'),
        ('Profesionales Establecimiento', 'Profesionales Establecimiento'),
        ('Profesionales Centro', 'Profesionales Centro'),
        ('Instituciones', 'Instituciones'),
             
        )

    Estudiante      = models.ForeignKey(Estudiante)
    fecha           = models.DateField(null=True)
    
    horario_i       = models.IntegerField(choices=TIPO_HORARIO,default=0)
    participantes   = models.CharField(max_length=100, choices=PARTICIPANTES)
    tipo_actividad  = models.ForeignKey(tipo_actividad)
    usuario         = models.ForeignKey(User)
    numero          = models.IntegerField(blank=True, null=True)# 1: hora tomada 2:hora realizada 3:hora no asistida
    estado          = models.IntegerField(blank=True, null=True, default=1)# 1: hora por confirmar 2:hora confirmada
    furgon          = models.IntegerField(choices=FURGON,default=0)# 0: no necesita furgon 1: si necesita coordinar furgón
    quien           = models.IntegerField(blank=True, null=True, default=1)# 1: psicologo 2:secretaria


    def get_horario_i(self):
        return u'%s' % TIPO_HORARIO[self.horario_i][1]
    def get_furgon(self):
        return u'%s' % FURGON[self.Furgon][1]        
    def __str__(self):
		return '{} {} {} {} {}'.format( self.id,self.Estudiante,self.fecha,self.horario_i,self.tipo_actividad.nombre)

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
        return '{} {} {}  '.format(self.fecha_confirma, self.estado1,self.estado2,self.estado3)

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

class agenda_profesional (models.Model):
   

    fecha           = models.DateField(null=True)
    horario_i       = models.IntegerField(choices=TIPO_HORARIO,default=0)
    horario_t       = models.IntegerField(choices=TIPO_HORARIO,default=1)
    bloques         = models.IntegerField(blank=True, null=True)# 1: hora tomada 2:hora realizada 3:hora no asistida
    accion          = models.IntegerField(choices=ACCION,default=0)
    tipo_actividad  = models.ForeignKey(tipo_actividad)
    usuario         = models.ForeignKey(User)
    numero          = models.IntegerField(blank=True, null=True)# 1: hora tomada 2:hora realizada 3:hora no asistida
    estado          = models.IntegerField(blank=True, null=True, default=1)# 1: hora por confirmar 2:hora confirmada
    observacion     = models.TextField(blank=True, null=True)#Agregar informacion sobre inacistencia extra
    agendar         = models.ForeignKey(agenda,blank=True, null=True)
    
    def get_horario_i(self):
        return u'%s' % TIPO_HORARIO[self.horario_i][1]
    def get_horario_t(self):
        return u'%s' % TIPO_HORARIO[self.horario_t][1]        
        
    def __str__(self):
        return '{} {} {} {}'.format( self.id,self.fecha,self.horario_i,self.horario_t)