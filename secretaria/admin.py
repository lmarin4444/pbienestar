# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from .models import Pregunta
from .models import VacunaT
from .models import MascotaRA
from .models import agenda
from .models import tipo_actividad
from .models import Reserva
from .models import Confirma
from .models import Registro




class agendaAdmin(admin.ModelAdmin):
    list_display = ('fecha','Estudiante','usuario','id')
    search_fields = ['fecha','objetivo',]
    list_per_page = 20
    list_max_show_all = 30

# Register your models here.

admin.site.register(Registro)
admin.site.register(Confirma)
admin.site.register(Pregunta)
admin.site.register(VacunaT)
admin.site.register(MascotaRA)
admin.site.register(agenda,agendaAdmin)
admin.site.register(tipo_actividad)
admin.site.register(Reserva)

