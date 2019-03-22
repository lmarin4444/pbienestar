# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from alumno.models import establecimiento
from django.contrib.auth.models import User
# Create your models here.
# usuario/models.py


class Profile(models.Model):
	"""docstring for Profile"""
	user 			= models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
	adress 			= models.CharField(max_length=100, blank=True)
	location 		= models.CharField(max_length=100, blank=True)
	birth_date 		= models.DateField(null=True,blank=True)
	area			= models.IntegerField(blank=True, null=True)
	firma	 	    = models.ImageField(upload_to='imagenes/%Y/%m/%d',blank=True, null=True)


	def __unicode__(self):
		return '{}'.format(self.user.username)






