# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db.models import Q
from models import Proyecto, Peticion, Wiki, Documento, Archivo, Comentario

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre','slug',)
    search_fields = ['nombre','slug',]
    list_per_page = 25
    list_max_show_all = 30

    class Media:
        js = ('grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
                'filebrowser/js/FB_TinyMCE.js',
                'filebrowser/js/TinyMCEAdmin.js',)

class WikiAdmin(admin.ModelAdmin):
    #list_display = ('proyecto',)
    list_per_page = 25
    list_max_show_all = 30

    class Media:
        js = ('grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
                'filebrowser/js/FB_TinyMCE.js',
                'filebrowser/js/TinyMCEAdmin.js',)

class PeticionAdmin(admin.ModelAdmin):
    list_display = ('proyecto','asunto','creado_fecha','inicio_fecha','terminado_fecha','creado_por','estado','asignado_a','prioridad',)
    list_filter = ['estado','prioridad',]
    search_fields = ['asunto']
    list_per_page = 25
    list_max_show_all = 30
    exclude = ('creado_por',)

    class Media:
        js = ('grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
                'filebrowser/js/FB_TinyMCE.js',
                'filebrowser/js/TinyMCEAdmin.js',)

    def save_model(self, request, obj, form, change):
        obj.creado_por = request.user
        obj.save()
        obj.notificar()

    def queryset(self, request):
        qs = super(PeticionAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(asignado_a=request.user) | Q(creado_por=request.user))

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('proyecto','categoria','titulo',)
    list_per_page = 25
    list_max_show_all = 30

    class Media:
        js = ('grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
                'filebrowser/js/FB_TinyMCE.js',
                'filebrowser/js/TinyMCEAdmin.js',)

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor','peticion','fecha',)
    list_per_page = 25
    list_max_show_all = 30

    class Media:
        js = ('grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
                'filebrowser/js/FB_TinyMCE.js',
                'filebrowser/js/TinyMCEAdmin.js',)

class ArchivoAdmin(admin.ModelAdmin):
    list_display = ('proyecto','archivo','descripcion',)
    list_per_page = 25
    list_max_show_all = 30        

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Peticion, PeticionAdmin)
admin.site.register(Wiki, WikiAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Archivo, ArchivoAdmin)
