# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from alumno.models import Estudiante, establecimiento
from sesion.models import Tematicas,objetivo_intervencion,Motivo_egreso
from derivacion.models import Motivo_derivacion,Red_apoyo,Ficha_derivacion
from dupla.models import Motivo_derivacion_dupla

OPCION = (
        (0, 'Si'),
        (1, 'No'),        
        )

MOTIVO = (
        (0, 'Se encuentra en proceso de evaluación'),
        (1, 'No ha terminado el proceso de intervención'),
        
        )


class Historia(models.Model):

	fecha 					= models.DateField()
	Estudiante 				= models.ForeignKey(Estudiante)
	Ficha_derivacion 		= models.ForeignKey(Ficha_derivacion)
	objetivo_intervencion   = models.ForeignKey(objetivo_intervencion,blank=True,null=True)
	observacion			    = models.TextField(blank=True,null=True)
	def __unicode__(self):
		return '{} {} {}  '.format(self.id,self.fecha,self.Estudiante)

class Ficha_de_egreso_historia(models.Model):
	"""docstring for Diagnostico"""

	Historia						= models.ForeignKey(Historia)
	fecha_informe					= models.DateField(blank=True,null=True)
	fecha_egreso 					= models.DateField(blank=True,null=True)
	Motivo_egreso 					= models.ForeignKey(Motivo_egreso)
	sintesis 			    		= models.TextField(blank=True,null=True)
	sugerencias						= models.TextField(blank=True,null=True)
	usuario 						= models.ForeignKey(User)
	
	
	def __unicode__(self):
		return '{} {} '.format(self.Historia, self.fecha_egreso)	
	

class Diagnostico_historia(models.Model):
	"""docstring for Diagnostico"""

	Historia						= models.ForeignKey(Historia)
	fecha 							= models.DateField(blank=True,null=True)
	situacion_actual		    	= models.TextField(blank=True,null=True)
	observaciones		    		= models.TextField(blank=True,null=True)
	familia				    		= models.TextField(blank=True,null=True)
	usuario 						= models.ForeignKey(User)
	
	
	def __unicode__(self):
		return '{} {} '.format(self.Historia, self.fecha)
# Create your models here.
class Ficha_derivacion_historica(models.Model):
	
	fecha_derivacion 		= models.DateField()
	pie  					= models.CharField(max_length=100,blank = True)
	anio_pie				= models.IntegerField(default=2000)
	habilidades		 		= models.CharField(max_length=100,blank = True)
#Preguntas abiertas de la ficha de derivacion	
	cuatro					= models.TextField()
	cinco					= models.TextField()
	conducta 				= models.TextField()
	rendimiento 			= models.TextField()
	area_responsabilidad	= models.TextField()
	antecedentes_familiares = models.TextField()
	seis					= models.TextField()
	observacion 			= models.TextField(default="Sin observación")	
	
	Red_apoyo 				= models.CharField(max_length=100,blank =True)
	Red_apoyo_obs			= models.TextField()
# Fecha de ingreso a lista de espera s
	fecha_espera			= models.DateField('Fecha de creacion',blank=True,null=True)
	Historia				= models.ForeignKey(Historia)
	def __unicode__(self):
		return '{} {}  '.format(self.id,self.fecha_derivacion)	

#Fichas de duplas hostoricas
class Ficha_derivacion_dupla_hostorica(models.Model):
	
    fecha_derivacion 		= models.DateField(null=True),
    quien_deriva			= models.CharField(max_length=200,blank=True, null=True)
    profe_jefe              = models.CharField(max_length=200,blank=True, null=True)
    	
    #Preguntas abiertas de la ficha de derivacion	
    	
    derivado     	 		= models.IntegerField(default=1,blank=True, null=True)
    pasada 					= models.IntegerField(default=1,blank=True, null=True)
    	
    #Preguntas abiertas de la ficha de derivacion	
    Motivo_derivacion_dupla	= models.TextField(null=True)
    conducta				= models.TextField(null=True)
    afecta 					= models.TextField(null=True)
    reiterada				= models.TextField(null=True)
    marzo					= models.IntegerField(null=True)
    abril					= models.IntegerField(null=True)
    mayo					= models.IntegerField(null=True)
    junio					= models.IntegerField(null=True)
    julio					= models.IntegerField(null=True)
    agosto					= models.IntegerField(null=True)
    septiembre				= models.IntegerField(default=0,blank=True, null=True)
    octubre					= models.IntegerField(default=0,blank=True, null=True)
    noviembre				= models.IntegerField(default=0,blank=True, null=True)
    diciembre				= models.IntegerField(default=0,blank=True, null=True)
    observacion 			= models.TextField(default="No observado")
# datos que indican escolaridad del estudiante al momento de realizar la ficha de derivacion 
# sacados de la escolaridad
    #establecimiento 		= models.ForeignKey(establecimiento)
    curso			 		= models.CharField(max_length=10,blank=True, null=True)
    letra			 		= models.CharField(max_length=2,blank=True, null=True)
# enlaces a los otros  modelos
    Estudiante              = models.ForeignKey(Estudiante)
    edad                    = models.IntegerField(blank=True, null=True)
    edad_f                  = models.IntegerField(blank=True, null=True)	
    estado                  = models.IntegerField(default=1)
    usuario                 = models.ForeignKey(User)
	

    def __unicode__(self):
        return '{} '.format(self.id)	


class sesion_historica(models.Model):
	numero			= models.IntegerField(default=0)
	horario_i       = models.CharField(max_length=100,blank =True)
	fecha 			= models.DateField()
	publico 		= models.CharField(max_length=100,blank = True)
	privado			= models.CharField(max_length=100,blank = True)
	observacion 	= models.CharField(max_length=100,blank = True)
	participantes 	= models.CharField(max_length=100,blank = True)
	pruebas			= models.CharField(max_length=100,blank = True)
	tipo_sesion 	= models.CharField(max_length=100,blank = True)
	usuario 		= models.CharField(max_length=100,blank = True)
	#Informacion sobre el regisro de la sesion
	situacion       = models.CharField(max_length=100,blank = True)
	obs             = models.TextField(blank=True, null=True)
	otros           = models.TextField(blank=True, null=True)#Agregar informacion sobre inacistencia extra
	    #Desde la confirmacion solo registro la observacion
	obs_confirma	= models.CharField(max_length=100,blank = True)
	Historia 		= models.ForeignKey(Historia)
	def __unicode__(self):
		return '{} {} {}'.format(self.Estudiante,self.observacion,self.publico)
	
	def get_participantes(self):
		return u'%s' % TIPO_CHOICES[self.participantes][1]

class objetivo_historico(models.Model):
	
	fecha_creacion 				= models.DateField(blank=True)
	objetivo_particular			= models.TextField(blank=True,null=True)
	Tematicas 					= models.ManyToManyField(Tematicas)
	Estudiante					= models.ForeignKey(Estudiante)
	usuario 					= models.ForeignKey(User)
	
	def __unicode__(self):
		return self.objetivo_particular

class Intervenidos_historico(models.Model):
	"""docstring for Intervenidos"""
	
	
	fecha_intervencion				= models.DateField(blank=True,null=True)
	
	estado 							= models.TextField()
	sintesis				    	= models.TextField()
	usuario 						= models.ForeignKey(User)
	#datos de la derivacion
	fecha_derivacion				= models.DateField(blank=True,null=True)
	dia 							= models.CharField(max_length=2,blank = True)
	mes 							= models.CharField(max_length=2,blank = True)
	anno 							= models.CharField(max_length=4,blank = True)
#numero que indica si el PsicoloTratante es el iniicla 1 si es 2 sino
	numero 							= models.IntegerField(default=1)
#numero que indica si un estudiante esta activo o no, dado que cuando se derive a otra institucion
# no estara disponible en la bandeja de cada una de las profesionales
# pero si debe estar hasta que se decida egresar. 1:activo 2 : derivado a otra institucion 	
	activo							= models.IntegerField(default=1)
	Profesional 					= models.CharField(max_length=100,blank=True,null=True)	
	Historia 						= models.ForeignKey(Historia)


# Archivos para guardar las sesiones de un estudiante

class agenda_historica(models.Model):

	fecha           		= models.DateField(null=True)
	Historia        		= models.ForeignKey(Historia)
	horario_i    			= models.CharField(max_length=5,blank = True)
		#informacion de la sesion						
	participantes 			 = models.CharField(max_length=50,blank = True)
	tipo_sesion 			 = models.CharField(max_length=100,blank = True)
	usuario     	 		 = models.CharField(max_length=50,blank = True)
	
	publico 				= models.TextField(blank=True, null=True)
	privado					= models.TextField(blank=True, null=True)
	observacion 			= models.CharField(max_length=100,blank = True)
	pruebas					= models.CharField(max_length=30,blank = True)
	usuario_sesion          = models.CharField(max_length=50,blank = True)
	numero					= models.IntegerField(blank=True, null=True)
	
		        
	
	        #Informacion del registro de sesion
	
	situacion  			    = models.TextField(blank=True, null=True)
	obs            		    =  models.TextField(blank=True, null=True)
	otros     	     		=  models.TextField(blank=True, null=True)#Agregar informacion sobre inacistencia extra
	
	
    	
	#informacion de la confirmacion 
	obs_confirma 			 =  models.TextField(blank=True, null=True)	
	def __str__(self):
		return '{} {} {} '.format( self.id,self.fecha,self.Historia.Estudiante)


class Motivo_Retorno_historia(models.Model):

	
	fecha_retorno			= models.DateField(blank=True, null=True)
	Historia 				= models.ForeignKey(Historia)
	motivo_termino 			= models.CharField(max_length=100,blank=True, null=True)
	observacion_termino 	= models.TextField(blank=True, null=True)
	
	opcion1		 			= models.IntegerField(choices=OPCION,default=1)
	filename1 				= models.CharField(max_length=100,blank=True, null=True)
 	docfile1 				= models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
 	
 	opcion2		 			= models.IntegerField(choices=OPCION,default=1)
 	filename2 				= models.CharField(max_length=100,blank=True, null=True)
 	docfile2 			    = models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
 						   	
 	opcion3		 			= models.IntegerField(choices=OPCION,default=1)
 	filename3 				= models.CharField(max_length=100,blank=True, null=True)
 	docfile3 				= models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
 	
 	Ficha_derivacion 		= models.ForeignKey(Ficha_derivacion)
 	
 	Red_apoyo				=  models.CharField(max_length=100,blank=True, null=True)
 	


	def docfile1_link(self):
		if self.docfile1:
			return "<a href='%s'>download</a>" % (self.docfile1.url,)
		else:
			return "No attachment"

		docfile1.allow_tags = True
		
	def docfile2_link(self):
		if self.docfile2:
			return "<a href='%s'>download</a>" % (self.docfile2.url,)
		else:
			return "No attachment"

		docfile2.allow_tags = True

	def docfile3_link(self):
		if self.docfile3:
			return "<a href='%s'>download</a>" % (self.docfile3.url,)
		else:
			return "No attachment"

		docfile3.allow_tags = True


	def __unicode__(self):
		return '{} {} {} '.format(self.id,self.Historia.Estudiante,self.observacion_termino)	
	

class objetivo_intervencion_historico(models.Model):
	
	fecha_creacion 				= models.DateField(blank=True)
	Historia 					= models.ForeignKey(Historia)
	objetivo_particular			= models.TextField(blank=True,null=True)
	Tematicas 					= models.ManyToManyField(Tematicas)
	usuario 					= models.ForeignKey(User)
	
	def __unicode__(self):
		return self.objetivo_particular
#Para la construcciond de los informes 
class informes_historico(models.Model):
	
	fecha_creacion 				= models.DateField(blank=True)
	Historia 					= models.ForeignKey(Historia)
	objetivo_particular			= models.TextField(blank=True,null=True)
	usuario 					= models.ForeignKey(User)
	
	def __unicode__(self):
		return self.objetivo_particular

class Reporte_continuidad_historia(models.Model):
	"""docstring for Diagnostico"""

	Historia 						= models.ForeignKey(Historia)
	fecha 							= models.DateField()
	motivo 							= models.PositiveIntegerField('Tipo_choices',choices=MOTIVO, default = 0)
	antecedentes		    		= models.TextField()
	observaciones					= models.TextField()
	sugerencias						= models.TextField()
	usuario 						= models.ForeignKey(User)
	
	
	def __unicode__(self):
		return '{} {} {} '.format(self.id,self.Historia, self.fecha)	
	def get_motivo(self):
		return u'%s' % MOTIVO[self.motivo][1]

