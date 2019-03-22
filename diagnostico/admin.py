# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Diagnostico_Institucional
from .models import Diagnostico_Institucional_curso
from .models import Diagnostico_Institucional_curso_indicador


# Register your models here.
admin.site.register(Diagnostico_Institucional)
admin.site.register(Diagnostico_Institucional_curso)
admin.site.register(Diagnostico_Institucional_curso_indicador)