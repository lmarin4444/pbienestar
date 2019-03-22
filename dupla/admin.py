# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Indicador
from .models import Dimensiones
from .models import Ficha_derivacion_dupla
from .models import Motivo_derivacion_dupla
from .models import Entrevista_ingreso_dupla
from .models import DiagnosticoI
from .models import Logros
from .models import Area_intervencion
from .models import Intervencion_casos
from .models import Intervencion_sesion
from .models import Intervencion_convivencia
from .models import Evento_convivencia
from .models import Derivacion_Ficha_derivacion_dupla
from .models import Intervencion_convivencia_curso
from .models import Relacion_Intervencion_convivencia_estudiante
from .models import Intervencion_convivencia_mediacion
from .models import Continuidad_dupla
from .models import Motivo_continuidad_dupla


admin.site.register(Intervencion_convivencia)
admin.site.register(Intervencion_sesion)
admin.site.register(Intervencion_casos)
admin.site.register(Area_intervencion)
admin.site.register(DiagnosticoI)
admin.site.register(Indicador)
admin.site.register(Dimensiones)
admin.site.register(Ficha_derivacion_dupla)
admin.site.register(Motivo_derivacion_dupla)
admin.site.register(Entrevista_ingreso_dupla)
admin.site.register(Logros)
admin.site.register(Evento_convivencia)
admin.site.register(Derivacion_Ficha_derivacion_dupla)
admin.site.register(Intervencion_convivencia_curso)
admin.site.register(Relacion_Intervencion_convivencia_estudiante)
admin.site.register(Intervencion_convivencia_mediacion)
admin.site.register(Continuidad_dupla)
admin.site.register(Motivo_continuidad_dupla)