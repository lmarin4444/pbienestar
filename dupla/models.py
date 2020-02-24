# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import datetime

from alumno.models import Estudiante
from alumno.models import curso 
from alumno.models import establecimiento
from alumno.models import Profesor
from profesional.models import Profesional
from alumno.models import Parentesco
from derivacion.models import Red_apoyo
from sesion.models import Tematicas


# Create your models here.

TIPO = (
        (0,'Sí'),
        (1,'No'),        
        )
TIPO_CONVIVENCIA = (
        (0,'Evento aislado '),
        (1,'Evento con curso involucrado'), 
        (2,'Evento mediación escolar'),
        (3,'Seguimiento '),
        

        )

OPCION = (
        (0, 'Si'),
        (1, 'No'),        
        )
# Los tipos de estado de un estudiante dentro del centro
ESTADO    = (
            (0,'Derivado'),
            (1,'Evaluación'),
            (2,'Lista de espera'),
            (3,'Intervención'),
            (4,'Derivado a otra institución'),
            (5,'Dado de alta'),
            (6,'Retornado a dupla'),
            (7,'Abandona la intervención por iniciativa propia'),
            (8,'Otro'),
            (9,'Derivado al Centro de Bienestar'),

            )

#Motivos de termino de una intervencion 
MOTIVO_TERMINO   = (
            (0,'Apoderado deserta de la atención'),
            (1,'No asiste regularmente'),
            (2,'Se cambia de institución '),
            (3,'Estudiante desvinculado por motivos personales '),
			(4,'Estudiante derivado a otra institución '), 
            (5,'Estudiante egresa del sistema educacional '), 
            (6,'Estudiante egresa del establecimiento de enseñanza básica'), 
            
	
            )

#Responsables de la creacion de un diagnostico 
RESPONSABLE   = (
            (0,'Equipo completo de formación y convivencia escolar'),
            (1,'Encargado de convivencia'),
            (2,'Psicóloga / Psicólogo del equipo de convivencia escolar'),
            (3,'Encargada de convivencia / Encargado de convivencia del equipo de convivencia escolar '),
			

            )

TIPO_CHOICES = (
        (0, 'Estudiantes'),
        (1, 'Estudiante'),
        (2, 'Adulto responsable'),
        (3, 'Estudiante - Mamá'),
        (4, 'Estudiante - Papá'),
        (5, 'Estudiante - Mama y Papá o Padrastros'),
        (6, 'Estudiante - Hermano o Hermana'),
        (7, 'Estudiante - Tío o Tía'),
        (8, 'Estudiante - Abuelo o Abuela'),
        (9, 'Estudiante -  Otro'),
        (10, 'Reunión Adulto Responsable'),
        (11, 'Reunión Profesionales (Dupla - Pie)'),
        (12, 'Reunión Profesionales Establecimiento'),
        (13, 'Reunión Profesionales Centro'),
        (14, 'Reunión Otros'),
        

        
        )


PARTICIPANTES = (
        (0, 'Estudiantes '),
        (1, 'Estudiantes - Docentes'),
        (2, 'Estudiantes - Apoderados'),
        (3, 'Estudiantes - Asistentes de la educación'),
        (4, 'Estudiantes - Directivos'),
        (5, 'Estudiantes - Familiares'),
        (6, 'Estudiantes - Otros'),
        (7, 'Docentes '),
        (8, 'Docentes - Apoderados'),
        (9, 'Docentes - Asistentes de la educación'),
        (10, 'Docentes - Directivos'),
        (11, 'Apoderados'),
        (12, 'Apoderados - Docentes'),
        (13, 'Apoderados - Asistentes de la educación'),
        (14, 'Apoderados - Directivos'),
        (15, 'Asistentes de la educación'),
        (16, 'Asistentes de la educación - Directivos'),

        (17, 'Directivos '),
        
        (18, 'Estudiantes - Docentes - Asistentes de la educación '),
        (19, 'Docentes - Asistente de la educación - Apoderados'),
        (20, 'Docentes - Apoderados - Directivos'),
        (21, 'Asistentes de la educación - Apoderados - Directivos'),
        (22, 'Estudiantes - Asistentes de la educación -  Apoderados'),
        (23, 'Estudiantes - Apoderados - Directivos'),

    
        )

TIPO_HORARIO = (
        (0, '08:00'),
        (1, '08:10'),
        (2, '08:20'),
        (3, '08:30'),
        (4, '08:40'),
        (5, '08:50'),
        
        (6, '09:00'),
        (7, '09:10'),
        (8, '09:20'),
        (9, '09:30'),
        (10, '09:40'),
        (11, '09:50'),

        (12, '10:00'),
        (13, '10:10'),
        (14, '10:20'),
        (15, '10:30'),
        (16, '10:40'),
        (17, '10:50'),

        (18, '11:00'),
        (19, '11:10'),
        (21, '11:20'),
        (22, '11:30'),
        (23, '11:40'),
        (24, '11:50'),

        (25, '12:00'),
        (26, '12:10'),
        (27, '12:20'),
        (28, '12:30'),
        (29, '12:40'),
        (30, '12:50'),

        (31, '13:00'),
        (32, '13:10'),
        (33, '13:20'),
        (34, '13:30'),
        (35, '13:40'),
        (36, '13:50'),

        (37, '14:00'),
        (38, '14:10'),
        (39, '14:20'),
        (40, '14:30'),
        (41, '14:40'),
        (42, '14:50'),

        (43, '15:00'),
        (44, '15:10'),
        (45, '15:20'),
        (46, '15:30'),
        (47, '15:40'),
        (48, '15:50'),

        (49, '16:00'),
        (50, '16:10'),
        (51, '16:20'),
        (52, '16:30'),
        (53, '16:40'),
        (54, '16:50'),

        (55, '17:00'),
        (56, '17:10'),
        (57, '17:20'),
        (58, '17:30'),
        (59, '17:40'),
        (60, '17:50'),

        (61, '18:00'),
        (62, '18:10'),
        (63, '18:20'),
        (64, '18:30'),
        (65, '18:40'),
        (66, '18:50'),

        (67, '19:00'),
        (68, '19:10'),
        (69, '19:20'),
        (70, '19:30'),
        (71, '19:40'),
        (72, '19:50'),

        )
HORARIO = (

        (0,'08:00'),
        (1,'08:15'),
        (2,'08:30'),
        (3,'08:45'),
        (4,'09:00'),
        (5,'09:15'),
        (6,'09:30'),
        (7,'09:45'),
        (8,'10:00'),
        (8,'1O:15'),
        (10,'10:30'),
        (11,'10:45'),
        (12,'11:00'),
        (13,'11:15'),
        (14,'11:30'),
        (15,'11:45'),
        (16,'12:00'),
        (17,'12:15'),
        (18,'12:30'),
        (19,'12:45'),
        (20,'13:00'),
        
        (17,'13:15'),
        (18,'13:30'),
        (19,'13:45'),
        (20,'14:00'),
        
        (17,'14:15'),
        (18,'14:30'),
        (19,'14:45'),
        (20,'15:00'),
        
        (17,'15:15'),
        (18,'15:30'),
        (19,'15:45'),
        (20,'16:00'),
        
        (17,'16:15'),
        (18,'16:30'),
        (19,'16:45'),
        (20,'17:00'),
        
        (17,'17:15'),
        (18,'17:30'),
        (19,'17:45'),
        (20,'18:00'),
        
        (17,'18:15'),
        (18,'18:30'),
        (19,'18:45'),
        (20,'19:00'),
        
        (17,'19:15'),
        (18,'19:30'),
        (19,'19:45'),
        (20,'20:00'),
        )

ESTADO_SESION = (
        (0,'Planificada'),
        (1,'Realizada'),
        (2,'No asiste '),
        (3,'Re-agendada'),        
        )

CANTIDAD = (
        (0, '1'),
        (1, '2'),
        (2, '3'),
        (3, '4'),
        (4, '5'),
        (5, '6'),
        (6, '7'),
        (7, '8'),
        (8, '9'),
        (9, '10'),
        (10, '11'),
        (11, '12'),
        (12, '13'),
        (13, '14'),
        (14, '15'),
        (15, '16'),

        )

CONVIVENCIA   = (
            (0,'Manual de convivencia escolar'),
            (1,'Mediación escolar'),
            (2,'Sugerencia de medidas pedagógicas'),
            (3,'Constatación de lesiones'),
            (4,'Denuncia PDI'),
            (5,'Denuncia Carabineros'),
            (6,'Acción desde el área de la convivencia escolar'),
            

            )


EVENTO   = (
            (0,'Agresión Verbal'),
            (1,'Agresión Física'),
            (2,'Asistencia y/o apoyo '),
            (3,'Contención emocional'),
            (4,'Informes'),
            (5,'Hospital y/o Servicio de salud'),
            (6,'Alcohol y drogas'),
            (7,'Ciber acoso'),



            

            )

MOTIVO_TERMINO   = (
            (0,'Estudiante deserta de la atención'),
            (1,'No asiste regularmente'),
            (2,'Se cambia de institución '),
            (3,'Estudiante desvinculado por motivos personales '),
            (4,'Estudiante derivado a otra institución '), 
            (5,'Egresa proceso de intervención '), 
            


            )

CURSO    = (
        (0, 'NT1'),
        (1, 'KINDER (NT2)'),
        (2, '1º'),
        (3, '2º'),
        (4, '3º'),
        (5, '4º'),
        (6, '5º'),
        (7, '6º'),
        (8, '7º'),
        (9, '8º'),
        (10, '1 MEDIO'),
        (11, '2 MEDIO'),
        (12, '3 MEDIO'),
        (13, '4 MEDIO'),
        (14, 'MULTIGRADO'),
        (15, '-'),


        )

TIPO_LETRAS = (
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D'),
        (4, 'E'),
        (5, '-'),

        )

TIPO_SEGUIMIENTO = (
        (0,'Evento aislado '),
        (1,'Evento con curso involucrado'), 
        (2,'Evento mediación escolar'),
        (3,'Seguimiento individual  '),
        

        )

class Indicador(models.Model):
    
    nombre              = models.CharField(max_length=100 ,blank=True)
    fuente              = models.CharField(max_length=500 ,blank=True)
    decripcion          = models.CharField(max_length=500 ,blank=True)
    #Tipo es devido a que los indicadores son 8 y solo se tomaran los primeros 4 dado que 
    tipo   			 	= models.IntegerField(choices=TIPO,default=0)
        
    def __unicode__(self):
        return '{} {}'.format(self.id,self.nombre)  
    
class Dimensiones(models.Model):
    
    
    
    nombre              = models.CharField(max_length=200 ,blank=True)
    decripcion          = models.CharField(max_length=500 ,blank=True)
    Indicador           = models.ForeignKey(Indicador,blank=True, null=True)
    
    
        
    def __unicode__(self):
        return '{}'.format(self.nombre)  
    


# MODELOS IGUAL A LOS QUE SE UTILZARON EN DERIVACION DADO QUE ES UNA OPCION SIMILAR.	
class intervencion_dupla(models.Model):

	fecha 		=models.DateField(auto_now_add=True)
	observacion =models.CharField(max_length=100)
	Estudiante  =models.ForeignKey(Estudiante)
	atiende 	=models.ForeignKey(User)
	def __unicode__(self):
		return '{}'.format(self.Estudiante)

# Create your models here.
	
class Motivo_derivacion_dupla(models.Model):
	nombre			= models.CharField(max_length=200)
	observacion 	= models.CharField(max_length=100)
	Indicador= models.ForeignKey(Indicador)
	def __unicode__(self):
		return self.nombre	

class Motivo_continuidad_dupla(models.Model):
    nombre          = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.nombre  



class Ficha_derivacion_dupla(models.Model):
	
    fecha_derivacion 		= models.DateField()
    quien_deriva			= models.CharField(max_length=200,blank=True, null=True)
    profe_jefe              = models.CharField(max_length=200,blank=True, null=True)
    	
    #Preguntas abiertas de la ficha de derivacion	
    	
    derivado     	 		= models.IntegerField(default=1)
    pasada 					= models.IntegerField(default=1)
    	
    #Preguntas abiertas de la ficha de derivacion	
    Motivo_derivacion_dupla	= models.ManyToManyField(Motivo_derivacion_dupla)
    conducta				= models.TextField()
    afecta 					= models.TextField()
    reiterada				= models.TextField()
    marzo					= models.IntegerField()
    abril					= models.IntegerField()
    mayo					= models.IntegerField()
    junio					= models.IntegerField()
    julio					= models.IntegerField()
    agosto					= models.IntegerField()
    septiembre				= models.IntegerField()
    octubre					= models.IntegerField()
    noviembre				= models.IntegerField()
    diciembre				= models.IntegerField()
    observacion 			= models.TextField(default="Sin observación")
# datos que indican escolaridad del estudiante al momento de realizar la ficha de derivacion 
# sacados de la escolaridad
    establecimiento 		= models.ForeignKey(establecimiento)
    curso			 		= models.CharField(max_length=10,blank=True, null=True)
    letra			 		= models.CharField(max_length=2,blank=True, null=True)
# enlaces a los otros  modelos
    Estudiante              = models.ForeignKey(Estudiante)
    edad                    = models.IntegerField(blank=True, null=True)
    edad_f                  = models.IntegerField(blank=True, null=True)	
    estado                  = models.IntegerField(default=1)
    usuario                 = models.ForeignKey(User)
	

    def __unicode__(self):
        return '{} {} {}'.format(self.id,self.fecha_derivacion,self.Estudiante)	
	
	
class Entrevista_ingreso_dupla(models.Model):
	
    fecha_derivacion 		= models.DateField()
    quien_deriva			= models.CharField(max_length=200,blank=True, null=True)
    		
    #Preguntas abiertas de la ficha de derivacion	
    	
    atencion_previa			= models.TextField()
    familia					= models.TextField()
    imagen 				    = models.ImageField(upload_to='imagenes/%Y/%m/%d',blank=True, null=True)
    problematica			= models.TextField()
	
	
# datos que indican escolaridad del estudiante al momento de realizar la ficha de derivacion 
# sacados de la escolaridad
	
    ficha_derivacion_dupla        = models.ForeignKey(Ficha_derivacion_dupla)
    usuario 		        	  = models.ForeignKey(User)
    	

    def __unicode__(self):
        return '{} {}'.format(self.id,self.fecha_derivacion)

class Continuidad_dupla(models.Model):
    
    fecha                         = models.DateField()
    motivo_continuidad            = models.ManyToManyField(Motivo_continuidad_dupla) # 1 significa planificada 
    observacion                   = models.TextField()
    ficha_derivacion_dupla        = models.ForeignKey(Ficha_derivacion_dupla)
    usuario                       = models.ForeignKey(User)
        

    def __unicode__(self):
        return '{} {}  '.format(self.id,self.fecha)

	
class DiagnosticoI(models.Model):
	
	fecha_diagnostico 			= models.DateField()			
	responsables  				= models.TextField()	
	annio 						= models.CharField(max_length=4)
#Preguntas abiertas de la ficha de derivacion	
	
	resumen						= models.TextField()
	acuerdos					= models.TextField()
	desacuerdos					= models.TextField()
	plenario					= models.TextField()

	establecimiento 			= models.ForeignKey(establecimiento)
# enlaces a los otros  modelos

	usuario 					= models.ForeignKey(User)
	

	def __unicode__(self):
		return '{} {} {} {}  '.format(self.annio,self.establecimiento.nombre,self.id,self.fecha_diagnostico)		

class Logros(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
	porcentaje					= models.IntegerField()
	observacion 				= models.TextField()
	dimension 					= models.ForeignKey(Dimensiones)
	diagnostico 	 	    	= models.ForeignKey(DiagnosticoI)

	

	def __unicode__(self):
		return '{} {}  '.format(self.dimension,self.porcentaje)		



#Modelos para la intervencion de casos de las duplas 

class Area_intervencion(models.Model):
	
	nombre  			     	= models.CharField(max_length=15)	
	descripcion 		    	= models.CharField(max_length=40)	

	

	def __unicode__(self):
		return '{}'.format(self.nombre)		
#Modelos para la intervencion de casos convivencia escolar

    

class Intervencion_casos(models.Model):
	
    fecha 			 			= models.DateField()			
    problematica  				= models.TextField()	
    objetivo_general 			= models.CharField(max_length=300)
    #Preguntas abiertas de la ficha de derivacion	
    	
    objetivo_especifico			= models.TextField()
    Tematicas                   = models.ManyToManyField(Tematicas)
    Area_intervencion 		    = models.ManyToManyField(Area_intervencion)
    estudiante 					= models.ForeignKey(Estudiante)
    # enlaces a los otros  modelos
    cantidad					= models.IntegerField(choices=CANTIDAD,default=5)# 1 significa planificada 
    	
    usuario 					= models.ForeignKey(User)
    ficha_derivacion_dupla      = models.ForeignKey(Ficha_derivacion_dupla)					
    	
    def get_cantidad(self):
        return u'%s' %CANTIDAD[self.cantidad][1]

    def __unicode__(self):
    	return '{} {} {}'.format(self.id,self.estudiante,self.fecha)		


class Intervencion_sesion(models.Model):
	
    fecha 			 			= models.DateField()			
    horario   		  		    = models.IntegerField(choices=HORARIO,default=0)
    objetivo_especifico			= models.TextField(blank=True, null=True)
    tematicas					= models.TextField(blank=True, null=True)
    area_intervencion 		    = models.ManyToManyField(Area_intervencion)
    observacion 				= models.CharField(max_length=500,blank=True, null=True)
    participantes   		    = models.IntegerField(choices=TIPO_CHOICES,default=0)
    numero						= models.IntegerField(choices=ESTADO_SESION,default=0)# 1 significa planificada 
# enlaces a los otros  modelos
# 0: Creada y planificada  - Agendada
# 1: Realizada
# 2: Eliminada
# 3: Suspendida o cancelada - cambiada de día
    intervencion_casos          = models.ForeignKey(Intervencion_casos)
    usuario 					= models.ForeignKey(User)
    	
    	
    class Meta:
    # sort by "fecha" in descending order unless
    # overridden in the query with order_by()
        ordering = ['fecha']
    def get_participantes(self):
    			return u'%s' %TIPO_CHOICES[self.participantes][1]
    def get_horario(self):
            return u'%s' %HORARIO[self.horario][1]		
    def get_numero(self):
            return u'%s' %ESTADO_SESION[self.numero][1]		


    def __unicode__(self):
        return '{} {} {} {}'.format(self.intervencion_casos,self.id,self.fecha,self.horario)	

#crear seguiniento de una causa
class Derivacion_Ficha_derivacion_dupla(models.Model):

    motivo_termino          = models.IntegerField(choices=MOTIVO_TERMINO)
    motivo                  = models.TextField(blank=True, null=True)
    fecha_derivacion        = models.DateField(auto_now_add=True)
    fecha_retorno           = models.DateField(blank=True, null=True)
    observacion_termino     = models.TextField(blank=True, null=True)
    
    
    filename1               = models.CharField(max_length=100,blank=True, null=True)
    docfile1                = models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
    
    
    filename2               = models.CharField(max_length=100,blank=True, null=True)
    docfile2                = models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
                            
    
    filename3               = models.CharField(max_length=100,blank=True, null=True)
    docfile3                = models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
    
    ficha_derivacion_dupla  = models.ForeignKey(Ficha_derivacion_dupla)
    Red_apoyo               = models.ForeignKey(Red_apoyo,blank=True,null=True)
    estado                  = models.IntegerField(default=1)
    usuario                 = models.ForeignKey(User)
    

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
    

    def get_motivo_termino(self):
        return u'%s' % MOTIVO_TERMINO[self.motivo_termino][1]

    def __unicode__(self):
        return '{} {}'.format(self.id,self.ficha_derivacion_dupla)    

class Evento_convivencia(models.Model):
    
    tipo_evento                = models.IntegerField(choices=EVENTO,default=0)
    observacion                = models.TextField()
# enlaces a los otros  modelos
    estudiante                  = models.ForeignKey(Estudiante)
    usuario                     = models.ForeignKey(User)
    
    
    def get_tipo_evento(self):
            return u'%s' %TIPO_CHOICES[self.particip][1]
    def get_horario(self):
            return u'%s' %HORARIO[self.horario][1]      
    
    def __unicode__(self):
        return '{} {}'.format(self.id,self.observacion) 

class Intervencion_convivencia(models.Model):
    
    fecha                       = models.DateField()            
    horario                     = models.IntegerField(choices=HORARIO,default=0)
    observacion                 = models.TextField()
    participantes               = models.IntegerField(choices=TIPO_CHOICES,default=0)
    
# enlaces a los otros  modelos
    dimensiones                 = models.ForeignKey(Dimensiones,blank=True, null=True)
    establecimiento             = models.ForeignKey(establecimiento,blank=True, null=True)
    usuario                     = models.ForeignKey(User)
    evento                      = models.ForeignKey(Evento_convivencia,blank=True, null=True)
#campo que indica si un evento tiene o no niños asociados, indica la cantidad  
    ninnos                      = models.IntegerField(choices=TIPO_CHOICES,default=0)    
    tipo_convivencia            = models.IntegerField(choices=TIPO_CONVIVENCIA,default=0)
    def get_participantes(self):
            return u'%s' %TIPO_CHOICES[self.participantes][1]
    def get_horario(self):
            return u'%s' %HORARIO[self.horario][1] 
    def get_tipo_convivencia(self):
            return u'%s' %TIPO_CONVIVENCIA[self.tipo_convivencia][1]                  
    def __unicode__(self):
        return '{} {}'.format(self.id,self.fecha)

class Intervencion_convivencia_mediacion(models.Model):
    
    fecha                       = models.DateField()            
    horario                     = models.IntegerField(choices=HORARIO,default=0)
    observacion                 = models.TextField()
    participantes               = models.IntegerField(choices=PARTICIPANTES,default=0)
    
# enlaces a los otros  modelos
    dimensiones                 = models.ForeignKey(Dimensiones,blank=True, null=True)
    establecimiento             = models.ForeignKey(establecimiento,blank=True, null=True)
    usuario                     = models.ForeignKey(User)
    tipo_convivencia            = models.IntegerField(choices=TIPO_CONVIVENCIA,default=0)
    
    def get_participantes(self):
            return u'%s' %PARTICIPANTES[self.participantes][1]
    def get_horario(self):
            return u'%s' %HORARIO[self.horario][1] 
    def get_tipo_convivencia(self):
            return u'%s' %TIPO_CONVIVENCIA[self.tipo_convivencia][1]                  
    

    def __unicode__(self):
        return '{} {}'.format(self.id,self.fecha)


class  Intervencion_convivencia_curso( Intervencion_convivencia ): 
    observacion_curso            = models.CharField(max_length=500,blank=True, null=True)    
    curso                        = models.IntegerField(choices=CURSO,default=15)    
    letra                        = models.IntegerField(choices=TIPO_LETRAS,default=5)    

    def get_curso(self):
            return u'%s' %CURSO[self.curso][1]
    def get_letra(self):
            return u'%s' %TIPO_LETRAS[self.letra][1] 
    
    
    def __unicode__(self):
        return '{} {} {}  '.format(self.id,self.curso, self.letra)   


# Tabla de relaciona al evento de convivencia con el estudiante
class  Relacion_Intervencion_convivencia_estudiante( models.Model ): 
    
    observacion_estudiante            = models.CharField(max_length=500,blank=True, null=True)    
    intervencion_convivencia          = models.ForeignKey(Intervencion_convivencia)  
    estudiante                        = models.ForeignKey(Estudiante)
    
    def __unicode__(self):
        return '{} {}  '.format(self.id,self.estudiante)   



class convivencia(models.Model):
    
    fecha                       = models.DateField()            
    horario                     = models.IntegerField(choices=HORARIO,default=0)
    observacion                 = models.TextField()
    participantes               = models.IntegerField(choices=PARTICIPANTES,default=0)
    
# enlaces a los otros  modelos
    dimensiones                 = models.ForeignKey(Dimensiones,blank=True, null=True)
    establecimiento             = models.ForeignKey(establecimiento,blank=True, null=True)
    usuario                     = models.ForeignKey(User)
    evento                      = models.ForeignKey(Evento_convivencia,blank=True, null=True)
#campo que indica si un evento tiene o no niños asociados, indica la cantidad  
    
    tipo_convivencia             = models.IntegerField(choices=TIPO_CONVIVENCIA,default=0)
    curso                        = models.IntegerField(choices=CURSO,default=15)    
    letra                        = models.IntegerField(choices=TIPO_LETRAS,default=5)    

    def get_curso(self):
            return u'%s' %CURSO[self.curso][1]
    def get_letra(self):
            return u'%s' %TIPO_LETRAS[self.letra][1] 
    def get_participantes(self):
            return u'%s' %PARTICIPANTES[self.participantes][1]
    def get_horario(self):
            return u'%s' %HORARIO[self.horario][1] 
    def get_tipo_convivencia(self):
            return u'%s' %TIPO_CONVIVENCIA[self.tipo_convivencia][1]                  
    def __unicode__(self):
        return '{} {}'.format(self.id,self.fecha)


class Seguimiento_convivencia(models.Model):
    
    fecha                   = models.DateField()
    observacion             = models.CharField(max_length=100,blank = True)
    
    
    #tipo_s indica el tipo de seguimento en el cual se deve relizar 
    tipo_s                  = models.PositiveIntegerField('TIPO_SEGUIMIENTO',choices=TIPO_SEGUIMIENTO)
    usuario                 = models.ForeignKey(User)
    evento                  = models.ForeignKey(Evento_convivencia)
    
    def __unicode__(self):
        return '{} {} '.format(self.Estudiante,self.observacion)
    
    def get_tipo_s(self):
        return u'%s' % TIPO_SEGUIMIENTO[self.tipo_s][1] 
