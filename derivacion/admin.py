# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from derivacion.models import Ficha_derivacion
from derivacion.models import Motivo_derivacion
from derivacion.models import Parentesco

from derivacion.models import Area_derivacion
from derivacion.models import Red_apoyo
from derivacion.models import Retorno
from derivacion.models import Bitacora
from derivacion.models import intervencion
from derivacion.models import Motivo_Retorno_Ficha_derivacion


# Register your models here.

class Ficha_derivacionAdmin(admin.ModelAdmin):
	list_display = ('fecha_derivacion','derivado','pasada','get_Estudiante','get_usuario','id','estado')
	search_fields = ['fecha_derivacion','get_Estudiante']
	list_per_page = 25
	list_max_show_all = 30
	    #funcion que trae al estudiante de cada ficha     
	def get_Estudiante(self, obj):
		return obj.Estudiante
	def get_usuario(self, obj):
			return obj.usuario
			
admin.site.register(Motivo_Retorno_Ficha_derivacion)
admin.site.register(Bitacora)
admin.site.register(Ficha_derivacion,Ficha_derivacionAdmin)
admin.site.register(Motivo_derivacion)

admin.site.register(Red_apoyo)
admin.site.register(Area_derivacion)
admin.site.register(Retorno)
admin.site.register(intervencion)


