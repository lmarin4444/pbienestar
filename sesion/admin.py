# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import tipo_sesion
from .models import pruebas
from .models import sesion
from .models import Diagnostico
from .models import Intervenidos
from .models import Pasos_intervencion
from .models import Tematicas
from .models import objetivo_intervencion
from .models import objetivo_intervencionhistoria
from .models import Reporte_continuidad
from .models import Motivo_egreso
from .models import Ficha_de_egreso
from .models import Estado
from .models import Seguimiento


# Register your models here.

class sesionAdmin(admin.ModelAdmin):
    list_display = ('fecha','Estudiante','publico','privado','participantes','tipo_sesion','id')
    search_fields = ['fecha']
    list_per_page = 25
    list_max_show_all = 30

class IntervenidosAdmin(admin.ModelAdmin):
    list_display = ('fecha','Estudiante','id','usuario')
    search_fields = ['fecha','Estudiante',]
    list_per_page = 25
    list_max_show_all = 30

admin.site.register(Seguimiento)
admin.site.register(Estado)    
admin.site.register(Ficha_de_egreso)    
admin.site.register(Motivo_egreso)
admin.site.register(Reporte_continuidad)
admin.site.register(objetivo_intervencionhistoria)
admin.site.register(objetivo_intervencion)
admin.site.register(Tematicas)
admin.site.register(tipo_sesion)
admin.site.register(pruebas)
admin.site.register(sesion,sesionAdmin)
admin.site.register(Diagnostico)
admin.site.register(Intervenidos,IntervenidosAdmin)
admin.site.register(Pasos_intervencion)


   
    		
