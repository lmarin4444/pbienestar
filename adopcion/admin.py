from django.contrib import admin

from adopcion.models import Persona
from adopcion.models import Solicitud


# Register your models here.
class PersonaAdmin(admin.ModelAdmin):
	list_display=('nombre','apellidos','edad','telefono')
	list_filter=('nombre','apellidos')
	search_fields=('apellidos',)

admin.site.register(Persona,PersonaAdmin)
admin.site.register(Solicitud)
