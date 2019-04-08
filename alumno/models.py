# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
CENTRO = (
        (0,'Sí'),
        (1,'No'),        
        )
        
TIPO_FAMILIAR = (
        ('PADRE', 'PADRE'),
        ('MADRE', 'MADRE'),
        ('PADRASTRO', 'PADRASTRO'),
        ('MADRASTRA', 'MADRASTRA'),

        ('HERMANO', 'HERMANO'),
        ('HERMANA', 'HERMANA'),
        ('HERMANASTRO', 'HERMANASTRO'),
        ('HERMANASTRA', 'HERMANASTRA'),
        
        ('MADRINA', 'MADRINA'),
        ('PADRINO', 'PADRINO'),

        ('ABUELO MATERNO ', 'ABUELO MATERNO'),
        ('ABUELO PATERNO ', 'ABUELO PATERNO'),
        ('ABUELA MATERNA ', 'ABUELA MATERNA'),
        ('ABUELA PATERNA ', 'ABUELA PATERNA'),

        
        ('ABUELASTRO', 'ABUELASTRO'),
        ('ABUELASTRA', 'ABUELASTRA'),
       
        ('TIO ABUELO', 'TIO ABUELO'),
        ('TIA ABUELA', 'TIA ABUELA'),
       
        ('TIO', 'TIO'),
        ('TIA', 'TIA'),
       
        ('PRIMO', 'PRIMO'),
        ('PRIMA', 'PRIMA'),
        ('TUTOR', 'TUTOR'),

        )


EDUCACION    = (
            (0,'Básica Incompleta'),
            (1,'Básica Completa'),
            (2,'Media Incompleta'),
            (3,'Media Completa'),
            (4,'Superior Incompleta'),
            (5,'Superior Completa'),
            (6,'Enseñanza básica'),
            (7,'Enseñanza Media'),
            (8,'Enseñanza superior'),


            )
TIPO_CHOICES = (
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
        (14, 'Multigrado'),


        )
TIPO_LETRAS = (
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D'),
        (4, 'E'),

        )
OPCION = (
        (0, 'Sí'),
        (1, 'No'),        
        )

class establecimiento(models.Model):
	"""docstring for materia"""
	nombre 		= models.CharField(max_length=50)
	Rbd 		= models.CharField(max_length=10,unique=True)
	localidad 	= models.CharField(max_length=50)
	clave		= models.CharField(max_length=20)
	director 	= models.CharField(max_length=50)
	telefono 	= models.CharField(max_length=50)
	correo		= models.EmailField(blank=True, null=True)
	cantidad 	= models.IntegerField()
	saldo 		= models.IntegerField()
	horas_ps 	= models.IntegerField(blank=True, null=True)
	horas_ts 	= models.IntegerField(blank=True, null=True)
	horas_ec 	= models.IntegerField(blank=True, null=True)


	def __unicode__(self):
		return self.nombre
	

class Profesor(models.Model):
	"""docstring for Profesor"""
	rut_p 			= models.CharField(max_length=12,unique=True)
	nombres 		= models.CharField(max_length=50)
	apellido_p 		= models.CharField(max_length=50)
	apellido_m		= models.CharField(max_length=50)
	telefono		= models.CharField(max_length=50)
	correo	    	= models.EmailField(blank=True, null=True)
	establecimiento = models.ManyToManyField(establecimiento)

	def __unicode__(self):
		return '{} {} {} '.format(self.nombres, self.apellido_m, self.apellido_m)


class curso(models.Model):
	"""docstring for materia"""

	numero 			= models.IntegerField(choices=TIPO_CHOICES, blank=True, null=True)
	letra 			= models.IntegerField(choices=TIPO_LETRAS, blank=True, null=True)
	
	establecimiento = models.ForeignKey(establecimiento)
	Profesor 		= models.ForeignKey(Profesor,blank=True, null=True)

	
	def get_numero(self):
			return u'%s' %TIPO_CHOICES[self.numero][1]

	def get_letra(self):
			return u'%s' %TIPO_LETRAS[self.letra][1]
	def __unicode__(self):
		return '{} {} {} '.format(self.numero, self.letra, self.establecimiento)
class Familia(models.Model):

	cantidad 			= models.IntegerField()
	
	def __unicode__(self):
		return '{} {}'.format(self.id,self.cantidad)

class Estudiante(models.Model):
	rut 					= models.CharField(max_length=12, unique=True)
	nombres 				= models.CharField(max_length=100)
	firs_name 				= models.CharField(max_length=50)
	last_name 				= models.CharField(max_length=50)
	domicilio_estudiante 	= models.CharField(max_length=70)
	fecha_nacimiento 		= models.DateField()
	edad 					= models.IntegerField(blank=True, null=True)
	curso 					= models.ForeignKey(curso)
	Familia 				= models.ForeignKey(Familia,blank=True, null=True)
	

	def __unicode__(self):
		return '{} {} {} {} {}'.format(self.id, self.rut,self.nombres, self.firs_name, self.last_name)

class vida(models.Model):
	"""docstring for materia"""
	Estudiante 		= models.ForeignKey(Estudiante)
	sesion 			= models.IntegerField()	
	tipo 			= models.IntegerField()	
	nombre 			= models.CharField(max_length=50)
	fecha_vida 		= models.DateField()
	
	def __unicode__(self):
		return self.nombre

class Escolaridad(models.Model):
	

	anno 				= models.CharField(max_length=10)
	fecha_inicio		= models.DateField( blank=True, null=True)
	fecha_termino 		= models.DateField( blank=True, null=True)
	rendimiento 		= models.CharField(max_length=100,blank=True)
	conducta 			= models.CharField(max_length=100,blank=True)
	curso 				= models.IntegerField(choices=TIPO_CHOICES)
	Letra 				= models.IntegerField(choices=TIPO_LETRAS)
	establecimiento 	= models.ForeignKey(establecimiento)
	Estudiante  		= models.ForeignKey(Estudiante)	

	def get_curso(self):
			return u'%s' %TIPO_CHOICES[self.curso][1]

	def get_Letra(self):
			return u'%s' %TIPO_LETRAS[self.Letra][1]
					
	def __unicode__(self):
		return '{} {} '.format(self.anno,self.Estudiante)	
	
class EscolaridadAnterior(models.Model):
	

	anno 				= models.CharField(max_length=10)
	fecha_inicio		= models.DateField( blank=True, null=True)
	fecha_termino 		= models.DateField( blank=True, null=True)
	rendimiento 		= models.CharField(max_length=100,blank=True)
	conducta 			= models.CharField(max_length=100,blank=True)
	curso 				= models.IntegerField(choices=TIPO_CHOICES, blank=True, null=True)
	Letra 				= models.IntegerField(choices=TIPO_LETRAS, blank=True, null=True)
	establecimiento 	= models.ForeignKey(establecimiento)
	Estudiante  		= models.ForeignKey(Estudiante)	

	def get_curso(self):
			return u'%s' %TIPO_CHOICES[self.curso][1]

	def get_Letra(self):
			return u'%s' %TIPO_LETRAS[self.Letra][1]
					
	def __unicode__(self):
		return '{} {} {}'.format(self.anno,self.Estudiante, self.establecimiento)		


class Parentesco(models.Model):
	
	nombre 			= models.CharField(max_length=100)
	apellido_p  	= models.CharField(max_length=100)
	apellido_m  	= models.CharField(max_length=100)
	parentesco  	= models.CharField(max_length=20, choices=TIPO_FAMILIAR, blank=True, null=True)
	edad 			= models.IntegerField()
	Escolaridad 	= models.IntegerField(choices=EDUCACION)
	curso			= models.CharField(max_length=100,blank=True, null=True)
	ocupacion   	= models.CharField(max_length=100 ,blank=True)
	Familia  		= models.ForeignKey(Familia,on_delete=models.CASCADE)	
	opcion		 	= models.IntegerField(choices=OPCION,default=0)
	

	
	def get_escolaridad(self):
			return u'%s' %EDUCACION[self.Escolaridad][1]
	def __unicode__(self):
		return '{} {} {} {} {}'.format(self.id,self.nombre, self.apellido_p, self.apellido_m, self.parentesco)	
	

class  apoderado ( Parentesco ): 
	rut 			= models.CharField(max_length=12,blank=True, null=True)    
	domicilio 		= models.CharField(max_length=100)
	telefono   		= models.CharField(max_length=100)

	
	def __unicode__(self):
		return '{} {} {} {} {} '.format(self.id,self.nombre, self.apellido_p, self.apellido_m, self.telefono)	

class  hermano ( Parentesco ): 
	rut 					= models.CharField(max_length=12,blank=True, null=True)    
	establecimiento 		= models.ForeignKey(establecimiento,blank=True, null=True)
	pertenece_centro 		= models.IntegerField(choices=CENTRO)
	
	def get_pertenece(self):
			return u'%s' %CENTRO[self.pertenece_centro][1]
	def __unicode__(self):
		return '{} {} {} {} {} '.format(self.id,self.nombre, self.apellido_p, self.apellido_m, self.pertenece_centro)	

	
	
	