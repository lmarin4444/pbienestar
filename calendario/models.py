# -*- coding: utf-8 -*-
from django.db import models
from django.forms.models import ModelForm
from django import forms
from django.contrib import admin
from django.core.mail import EmailMessage
from django.contrib.auth.models import User,Group
import string, datetime
from django.template.defaultfilters import slugify
from alumno.models import Estudiante
import datetime

PRIORIDAD = (
            (0,'Baja'),
            (1,'Normal'),
            (2,'Alta'),
            (3,'Urgente'),
            (4,'Inmediata'),
            )
CATEGORIA = (
            (0,'Documentación de usuario'),
            (1,'Documentación tecnica'),
            )
ESTADO    = (
            (0,'Diagnostico'),
            (1,'Intervencion'),
            (2,'Retorno Dupla'),
            (3,'Derivado otra entidad'),
            (4,'Dado de alta'),
            
            )
AVANCE    = (
            (0,'0 %'),
            (1,'10 %'),
            (2,'20 %'),
            (3,'30 %'),
            (4,'40 %'),
            (5,'50 %'),
            (5,'50 %'),
            (6,'60 %'),
            (7,'70 %'),
            (8,'80 %'),
            (9,'90 %'),
            (10,'100 %'),
            )

class Proyecto(models.Model):
    nombre       = models.CharField('Proyecto',max_length=60)
    descripcion  = models.TextField('Descripcion',blank=True,null=True)
    slug         = models.SlugField('Slug',max_length=60,editable=False, unique=True)
    #groupo       = models.ForeignKey(Group, related_name='Grupo')
    
    creado_fecha = models.DateTimeField('Fecha de creación',auto_now=True)


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nombre)
        super(Proyecto, self).save(*args, **kwargs)

    def __unicode__(self):#	modified:  
        return self.nombre

    objects = models.Manager()
        
    class Meta:
        ordering = ["nombre"]
        verbose_name = 'Proyectos'
        verbose_name_plural = "Proyectos"
        #unique_together = ("groupo", "slug")
        
class Peticion(models.Model):
    asunto          = models.CharField('Asunto',max_length=140)
    proyecto        = models.ForeignKey(Proyecto)
    descripcion     = models.TextField('Descripcion',blank=True,null=True)
    creado_fecha    = models.DateTimeField('Fecha de creacion',auto_now=True)
    #inicio_fecha    = models.DateField('Fecha de inicio',default = datetime.date.today())
    inicio_fecha    = models.DateField('Fecha de inicio')
    terminado_fecha = models.DateField('Fecha fin',blank=True,null=True,)
    completo_fecha  = models.DateTimeField('Fecha de culminacion',blank=True,null=True,editable = False)
    creado_por      = models.ForeignKey(User)
    estado          = models.PositiveIntegerField('Estado',choices=ESTADO, default = 0)
    asignado_a      = models.ForeignKey(User, related_name='Asignado')
    prioridad       = models.PositiveIntegerField('Prioridad', choices=PRIORIDAD, default = 1)
    avance          = models.PositiveIntegerField('% realizado', choices=AVANCE, default = 0)
    tiempo_estimado = models.PositiveIntegerField('Tiempo estimado', blank = True, null = True)

    def __unicode__(self):
        return self.asunto

    def notificar(self):
        asunto = u'%s - Peticion #%s (%s) %s' % (self.proyecto.nombre,self.pk, self.get_estado(), self.asunto)
        de, a = self.creado_por.email, self.asignado_a.email
        cuerpo = u'<p>Ticket #%s ha sido reportado por %s</p><h3>Peticion #%s: %s</h3><ul><li>Autor: %s</li><li>Estado: %s</li><li>Prioridad: %s</li><li>Asignado a: %s</li></ul><p>%s</p>' % (
            self.pk,
            self.creado_por.get_full_name(),
            self.pk,
            self.asunto,
            self.creado_por.get_full_name(),
            self.get_estado(),
            self.get_prioridad(),
            self.asignado_a.get_full_name(),
            self.descripcion,
            )
        msg = EmailMessage(asunto, cuerpo, de, [a])
        msg.content_subtype = "html"
        #msg.send()
    #def save(self):
        #if self.completed :
        #    self.completo_fecha = datetime.datetime.now()
        #super(Peticion, self).save()

    def get_estado(self):
        return u'%s' % ESTADO[self.estado][1]

    def get_prioridad(self):
        return u'%s' % PRIORIDAD[self.prioridad][1]

    class Meta:
        ordering = ["prioridad"]
        verbose_name = 'Peticion'
        verbose_name_plural = 'Peticiones'
        
class Wiki(models.Model):
    proyecto  = models.OneToOneField(Proyecto)
    cuerpo    = models.TextField('Contenido')
    cometario = models.CharField('Comentario',max_length=255,blank=True,null=True)

    class Meta:
        verbose_name = 'Wiki'
        verbose_name_plural = 'Wikis'

    def __unicode__(self):
        return u'Wiki del %s' % self.proyecto

class Documento(models.Model):
    proyecto  = models.ForeignKey(Proyecto)
    categoria = models.IntegerField('Categoria', choices=CATEGORIA, default=0)
    titulo    = models.CharField('Titulo',max_length=255)
    cuerpo    = models.TextField('Contenido')

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __unicode__(self):
        return self.titulo

class Archivo(models.Model):
    proyecto    = models.ForeignKey(Proyecto)
    archivo     = models.FileField('Archivo', upload_to='uploads/archivo/')
    descripcion = models.CharField('Descripcion', max_length=255,blank=True,null=True)

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

    def __unicode__(self):
        return u'archivo: %s' % self.proyecto

class Comentario(models.Model):    
    """
    Not using Django's built-in comments becase we want to be able to save 
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    autor    = models.ForeignKey(User, related_name='Autor')
    peticion = models.ForeignKey(Peticion, related_name='Peticion')
    fecha    = models.DateTimeField(default=datetime.datetime.now)
    cuerpo   = models.TextField('Comentario',blank=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __unicode__(self):        
        return '%s - %s' % (
                self.autor, 
                self.fecha, 
                )
