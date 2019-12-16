# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from alumno.models import Estudiante
from django.contrib.auth.models import User
# Create your models here.

TIPO = (
        (0,'Centro de Bienestar'),
        (1,'Formación y convivencia'),  
        (2,'Convivencia Escolar'),  

        )
class documentos(models.Model):

	
	fecha_subida			= models.DateField(blank=True, null=True)
	nombre	 				= models.CharField(max_length=100,blank=True, null=True)
 	docfile1 				= models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
 	Estudiante 				= models.ForeignKey(Estudiante)
 		

	def docfile1_link(self):
		if self.docfile1:
			return "<a href='%s'>download</a>" % (self.docfile1.url,)

		else:
			return "No attachment"

		docfile1.allow_tags = True

	def __unicode__(self):
		return '{} {} {} '.format(self.fecha_subida,self.Estudiante,self.nombre)

class formatos(models.Model):

	
	fecha_subida			= models.DateField(blank=True, null=True)
	nombre	 				= models.CharField(max_length=100,blank=True, null=True)
 	docfile1 				= models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
 	tipo		 			= models.IntegerField(choices=TIPO,default=1)
 	usuario 				= models.ForeignKey(User)
 	
 		

	def docfile1_link(self):
		if self.docfile1:
			return "<a href='%s'>download</a>" % (self.docfile1.url,)

		else:
			return "No attachment"

		docfile1.allow_tags = True

	def get_tipo(self):
		return u'%s' % TIPO[self.tipo][1]

	def __unicode__(self):
		return '{} {} '.format(self.fecha_subida,self.nombre)		