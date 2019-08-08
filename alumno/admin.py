# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
#para agregar las fincionalidades del admin principal de djamgo
from django.contrib.admin import AdminSite
# Register your models here.


from .models import Profesor
from .models import curso
from .models import apoderado
from .models import Parentesco
from .models import Estudiante
from .models import Escolaridad
from .models import establecimiento
from .models import vida
from .models import hermano
from .models import Familia
from .models import EscolaridadAnterior
from .models import Profesor

class EstudianteAdmin(admin.ModelAdmin):
	list_display = ('id','rut','nombres','firs_name','last_name','curso')
	search_fields = ['Estudiante']
	list_per_page = 25
	list_max_show_all = 30
	    #funcion que trae al estudiante de cada ficha     
	def get_Estudiante(self, obj):
		return obj.Estudiante
	def get_usuario(self, obj):
			return obj.usuario

class establecimientoAdmin(admin.ModelAdmin):
	list_display = ('id','Rbd','nombre','alias')
	search_fields = ['establecimiento']
	list_per_page = 25
	list_max_show_all = 30
	    #funcion que trae al estudiante de cada ficha     



# Register your models here.
admin.site.register(Familia)
admin.site.register(apoderado)
admin.site.register(hermano)
admin.site.register(Parentesco)
admin.site.register(Profesor)
admin.site.register(curso)
admin.site.register(Estudiante,EstudianteAdmin)
admin.site.register(EscolaridadAnterior)
admin.site.register(Escolaridad)
admin.site.register(establecimiento,establecimientoAdmin)
admin.site.register(vida)


class SitioAdministrativo(AdminSite):
    site_header = 'Sitio Administrativo Personalizado'
# Register your models here.
