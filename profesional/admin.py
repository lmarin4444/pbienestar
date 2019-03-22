# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Profesional
from .models import Cargo
from .models import Acciones_profesional



# Register your models here.
admin.site.register(Acciones_profesional)
admin.site.register(Profesional)
admin.site.register(Cargo)


# Register your models here.