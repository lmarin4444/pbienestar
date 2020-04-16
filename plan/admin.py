# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Plan
from .models import Base
from .models import Medios_verificacion
from .models import Planes_externos
from .models import Accion
from .models import Indicador_base
from .models import Plancillo
from .models import Actividades
from .models import Hecho_Actividades
from .models import Verificadores
from .models import Planes_mineduc
from .models import Planes_mineduc_establecimientos
from .models import Planes_convivencia

admin.site.register(Plan)
admin.site.register(Base)
admin.site.register(Medios_verificacion)
admin.site.register(Planes_externos)
admin.site.register(Accion)
admin.site.register(Indicador_base)
admin.site.register(Plancillo)
admin.site.register(Actividades)
admin.site.register(Hecho_Actividades)
admin.site.register(Verificadores)
admin.site.register(Planes_mineduc)
admin.site.register(Planes_mineduc_establecimientos)
admin.site.register(Planes_convivencia)
