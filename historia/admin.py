# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Historia
from .models import Ficha_derivacion_historica
from .models import Intervenidos_historico
from .models import agenda_historica
from .models import objetivo_intervencion_historico
from .models import sesion_historica
from .models import Motivo_Retorno_historia
from .models import Diagnostico_historia
from .models import Ficha_de_egreso_historia
from .models import Reporte_continuidad_historia

# Register your models here.
admin.site.register(Reporte_continuidad_historia)
admin.site.register(Ficha_de_egreso_historia)
admin.site.register(Diagnostico_historia)
admin.site.register(Motivo_Retorno_historia)
admin.site.register(sesion_historica)
admin.site.register(objetivo_intervencion_historico)
admin.site.register(agenda_historica)
admin.site.register(Intervenidos_historico)
admin.site.register(Ficha_derivacion_historica)
admin.site.register(Historia)
