# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from informe.models import documentos
from informe.models import formatos

			
admin.site.register(documentos)
admin.site.register(formatos)
