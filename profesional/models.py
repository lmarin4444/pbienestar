# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
# Create your models here.
# models.py
from django.contrib.auth.models import User
from django.forms import ModelForm
from alumno.models import establecimiento

TIPO = (
            (0,'Supervisor'),
            (1,'Secretaria'),
            (2,'Profesional Centro Bienestar'),
            (3,'Profesional Pie'),
            (4,'Psicóloga Psicólogo  Dupla'),
            (5,'Trabajadora trabajador  Social  Dupla'),
            (6,'Encargada / encargado de convivencia '),
            (7,'Encargado de convivencia y Psicologo Dupla'),
            (8,'Encargado de convivencia y Trabajador Social Dupla'),
            (9,'Encargado de convivencia, Psicólogo Psicóloga y Trabajador Social Dupla'),
            )

TIPO_ACCION = (
            (0,'Informes Tribunal de Familia'),
            (1,'Denuncia a Carabineros'),
            (2,'Denuncia a PDI'),
            (3,'Coordinación especial'),
            (4,'Gestión especial'),
            (5,'Reuniones'),
            (6,'Audencia Judiciales (Tribunales - Fiscalía)'),
            (7,'Capacitaciones'),
            
            
            )

CANTIDAD = (
        (0, '1'),
        (1, '2'),
        (2, '3'),
        (3, '4'),
        (4, '5'),
        (5, '6'),
        (6, '7'),
        (7, '8'),
        (8, '9'),
        (9, '10'),
        (10, '11'),
        (11, '12'),
        (12, '13'),
        (13, '14'),
        (14, '15'),
        (15, '16'),

        )
class Profesional(models.Model):
	rut 				= models.CharField(max_length=12, unique=True)
	adress 				= models.CharField(max_length=100)
	phone 				= models.CharField(max_length=20)
	email				= models.EmailField()
	tipo_profesional 	= models.PositiveIntegerField(choices=TIPO, blank=True, null=True)
	usuario 			= models.OneToOneField(User)
	establecimiento		= models.ManyToManyField(establecimiento)
	
	def get_profesional(self):
		return u'%s' % TIPO[self.tipo_profesional][1]
	def __unicode__(self):
		return '{} {} {} '.format(self.rut,self.usuario.first_name,self.usuario.last_name)
	
class Cargo(models.Model):
	profesional 					= models.ForeignKey(Profesional, on_delete=models.CASCADE)
	escuela							= models.ForeignKey(establecimiento, on_delete=models.CASCADE)
	tipo_profesional 				= models.PositiveIntegerField(choices=TIPO, blank=True, null=True)     
	cantidad_horas_convivencia 		= models.PositiveIntegerField()     
	cantidad_horas_dupla 			= models.PositiveIntegerField()     
	

	def get_profesional(self):
			return u'%s' % TIPO[self.tipo_profesional][1]
	def __unicode__(self):
		return '{} {} '.format(self.profesional,self.escuela)

class Acciones_profesional(models.Model):
	
	fecha							= models.DateField('Fecha de registro',blank=True,null=True)
	profesional 					= models.ForeignKey(Profesional, on_delete=models.CASCADE)
	objetivo						= models.TextField()
	descripcion						= models.TextField()
	tipo_accion 	 				= models.PositiveIntegerField(choices=TIPO_ACCION)     
	cantidad						= models.IntegerField(choices=CANTIDAD,default=0)# 1 significa planificada 
	
	
	def get_tipo_accion(self):
			return u'%s' % TIPO_ACCION[self.tipo_accion][1]
	def get_cantidad(self):
			return u'%s' %CANTIDAD[self.cantidad][1]			
	def __unicode__(self):
		return '{} {} '.format(self.profesional,self.tipo_accion)
