# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from alumno.models import establecimiento
from dupla.models import Dimensiones
from alumno.models import curso

# Create your models here.
CANTIDAD = (
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3'),  
        (4,'4'),  
        (5,'5'),  
        (6,'6'),  
        (7,'7'),  
        (8,'8'),          
        (9,'9'),          
        (10,'10'),          
        )

DIMENSION_PME = (
        (1,'Gestión Pedagógica'),
        (2,'Liderazgo'),
        (3,'Convivencia escolar'),  
        (4,'Gestión de recursos'),  
               
        )
EJECUTORES = (
            (0,'Equipo de formación y convivencia'),
            (1,'Dupla'),
            (2,'Encargado de convivencia'),
            (3,'Psicólogo Dupla'),
            (4,'Trabajador Social  Dupla'),
            (5,'Profesional externo'),
            (6,'Red externa'),
            (7,'Programa municipal externo'),
            (8,'Profesional comunidad educativa'),

          
            )
RESPONSABLES = (
            (0,'Equipo de formación y convivencia'),
            (1,'Dupla'),
            (2,'Encargado de convivencia'),
            (3,'Psicólogo Dupla'),
            (4,'Trabajador Social  Dupla'),
           

          
            )
EVALUACION = (
            (0,'Encuestas de satisfacción '),
            (1,'Conversatorios retroalimentados'),
            (2,'Presentaciones abiertas a la comunidad'),
            (3,'Representaciones '),
            (4,'Actividad sin evaluación'),

            
          
            )
PARTICIPANTES = (
            (0,'Comunidad educativa'),
            (1,'Consejo escolar'),
            (2,'Estudiantado'),
            (3,'Centro de padres y/o Apoderados'),
            (4,'Consejo de profesores / Docentes / Asistentes de la educación '),
            (5,'Estudiantes mismo curso'),
            (6,'Estudiantes diferentes cursos '),
            (7,'Estudiantes / Docentes / Asistentes de la educación'),
            (8,'Estudiantes / Apoderados'),
            (9,'Estudiantes / Directivos'),
            (10,'Docentes / Apoderados'),
            (11,'Docentes /  Directivos'),
            (12,'Directivos / Estudiantes'),
            (13,'Directivos / Apoderados'),
            (14,'Directivos / Docentes'),
             
            )
ESTADO = (
            (0,'Definido'),

            (1,'Realizado'),
            (2,'Re agendado'),
            (3,'Postergado - Justificado'),
            (4,'Suspendido por ordenes del director'),
            (5,'Suspendido por actividades del establecimiento'),
            (6,'Suspendido por mal tiempo'),
            (7,'Suspendido por problemas de fuerza mayor'),
            (8,'Planificado'),
            (9,'NO REALIZADA - FUERA DE PLAZO'),
           
             
            )

TIPO_NUMERO = (
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
        (14, 'Multigrado'),
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

TIPO_HORARIO = (

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



MES = (
        (0,'Enero'),
        (1,'Febrero'),
        (2,'Marzo'),
        (3,'Abril'),
        (4,'Mayo'),  
        (5,'Junio'),  
        (6,'Julio'),  
        (7,'Agosto'),  
        (8,'Septiembre'),  
        (9,'Octubre'),          
        (10,'Noviembre'),          
        (11,'Diciembre'),          
        )
LOGRO = (
        (0,'0%'),
        (1,'5%'),
        (2,'10%'),
        (3,'15%'),
        (4,'16%'),
        (5,'17%'),
        (6,'18%'),  
        (7,'19%'),  
        
        (8,'20%'),
        (9,'21%'),    
        (10,'22%'),  
        (11,'23%'),  
        (12,'24%'),  
        (13,'25%'),          
        (14,'26%'),          
        (15,'27%'), 
        (16,'28%'),  
        (17,'29%'),

        (18,'30%'),  
        (19,'31%'),          
        (20,'32%'),
        (21,'33%'),
        (22,'34%'),
        (23,'35%'),
        (24,'36%'),
        (25,'37%'),                
        (26,'38%'),
        (27,'39%'),

        (28,'40%'),
        (29,'41%'),          
        (30,'42%'),
        (31,'43%'),
        (32,'44%'),
        (33,'45%'),
        (34,'46%'),
        (35,'47%'),                
        (36,'48%'),
        (37,'49%'),

        (38,'50%'),
        (39,'51%'),          
        (40,'52%'),
        (41,'53%'),
        (42,'54%'),
        (43,'55%'),
        (44,'56%'),
        (45,'57%'),                
        (46,'58%'),
        (47,'59%'),

        (48,'60%'),
        (49,'61%'),          
        (50,'62%'),
        (51,'63%'),
        (52,'64%'),
        (53,'65%'),
        (54,'66%'),
        (55,'67%'),                
        (56,'68%'),
        (57,'69%'),

        (58,'70%'),
        (59,'71%'),          
        (60,'72%'),
        (61,'73%'),
        (62,'74%'),
        (63,'75%'),
        (64,'76%'),
        (65,'77%'),                
        (66,'78%'),
        (67,'79%'),

        (68,'80%'),
        (69,'81%'),          
        (70,'82%'),
        (71,'83%'),
        (72,'84%'),
        (73,'85%'),
        (74,'86%'),
        (75,'87%'),                
        (76,'88%'),
        (77,'89%'),
        (78,'90%'),
        (79,'91%'),          
        (80,'92%'),
        (81,'93%'),
        (82,'94%'),
        (83,'95%'),
        (84,'96%'),
        (85,'97%'),                
        (86,'98%'),
        (87,'99%'),

        (88,'100%'),
        


        )

TIPO_INDICADOR = (
        (0,'Cuantitativo'),
        (1,'Cualitativo'),
             
        )
TIPO_ACTIVIDAD   = (
        
       
        (0,'Contención'),
        (1,'Atención Apoderados / Profesores / otros'),
        (2,'Apoyo Estudiantes / Profesores / otros profesionales'),
        (3,'Apoyo Situación Médica'),
        (4,'Coordinación '),
        (5,'Construcción / informes '),
        (6,'Reuniones'),
        (7,'Capacitaciones'),
        (8,'Acción propia del establecimiento'),
        (9,'Celebraciones del establecimiento'),
        (10,'Fallas ( Agua - Luz - etc.'),
        (11,'Cambio de activivdades por desplanificación'),
        (12,'Acción Plan'),
        (13,'Atención de casos'),
        (14,'Acción convivencia escolar'),

        
            )

TIPO_EVALUACION = (
        (0,'Encuesta de satisfacción'),
        (1,'Encuesta Nº1'),
        (1,'Encuesta Nº2'),
        (1,'Encuesta Nº3'),
        (1,'Encuesta Nº4'),
             
        )
NOTA = (
        (0,'2,0'),
        (1,'3,0'),
        (2,'4,1'),
        (3,'4,2'),
        (4,'4,3'),
        (5,'4,4'),
        (6,'4,5'),
        (7,'4,6'),
        (8,'4,7'),
        (9,'4,8'),
        (10,'4,9'),
        (11,'5,0'),
        (12,'5,1'),
        (13,'5,2'),
        (14,'5,3'),
        (15,'5,4'),
        (16,'5,5'),
        (17,'5,6'),
        (18,'5,7'),
        (19,'5,8'),
        (20,'5,9'),
        (21,'6,0'),
        (22,'6,1'),
        (23,'6,2'),
        (24,'6,3'),
        (25,'6,4'),
        (26,'6,5'),
        (27,'6,6'),
        (28,'6,7'),
        (29,'6,8'),
        (30,'6,9'),
        (31,'7,0'),
             
        )


class Plan(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnóstico
	
	fecha				 		= models.DateField()
	responsable					= models.TextField()#Quien construye el plan
	sello		 				= models.TextField()
	objetivo_general			= models.TextField()
	objetivo_especificos		= models.TextField()
	annio 						= models.IntegerField()
	establecimiento 			= models.ForeignKey(establecimiento)
	usuario 					= models.ForeignKey(User)
	

	def __unicode__(self):
		return '{} {} {} {} '.format(self.establecimiento.nombre, self.fecha,self.responsable,self.id)		

class Base(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
	nombre		 				= models.TextField()#Nombre de la base a desarrollar 
	dimension_pme				= models.IntegerField(default=0,choices=DIMENSION_PME)
	dimension		 			= models.ForeignKey(Dimensiones)
	objetivo 					= models.TextField()
	estrategia 					= models.TextField()
	cantidad_indicadores 		= models.IntegerField(default=0,choices=CANTIDAD)
	cantidad_acciones 			= models.IntegerField(default=0,choices=CANTIDAD)
	
	plan 	 					= models.ForeignKey(Plan)
	usuario 					= models.ForeignKey(User)
	
	
	def get_dimension_pme(self):
			return u'%s' %DIMENSION_PME[self.dimension_pme][1]
	def get_indicadores(self):
			return u'%s' %CANTIDAD[self.cantidad_indicadores][1]
	def get_acciones(self):
			return u'%s' %CANTIDAD[self.cantidad_acciones][1]		

	def __unicode__(self):
		return '{} {} {} {} {}'.format(self.id,self.plan.establecimiento.nombre,self.cantidad_indicadores,self.cantidad_acciones,self.dimension.nombre)	


class Medios_verificacion(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
	nombre		 				= models.CharField(max_length=50)
	descripcion					= models.TextField()

	def __unicode__(self):
		return '{} '.format(self.nombre)	

class Verificadores(models.Model):
    
    #Ingresar cada uno de los niveles de logros por diagnostico
    
    nombre                      = models.CharField(max_length=50)
    descripcion                 = models.TextField()

    def __unicode__(self):
        return '{} {} '.format(self.id,self.nombre)

	
class Planes_externos(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
    nombre		 				= models.CharField(max_length=70)
    descripcion                 = models.TextField()
    objetivo_general            = models.TextField()
    objetivo_especifico         = models.TextField()
    acciones                    = models.TextField()




    def __unicode__(self):
            return '{} '.format(self.nombre)	
class Planes_mineduc(models.Model):
    
    #Ingresar cada uno de los niveles de logros por diagnostico
    
    
    fecha                       = models.DateField('Fecha de creacion',blank=True,null=True)
    nombre                      = models.CharField(max_length=70)
    descripcion                 = models.TextField()
    objetivo_general            = models.TextField()
    establecimiento             = models.ForeignKey(establecimiento)
    docfile1                    = models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)


    def docfile1_link(self):
        if self.docfile1:
            return "<a href='%s'>download</a>" % (self.docfile1.url,)
        else:
            return "No attachment"

        docfile1.allow_tags = True

    def __unicode__(self):
            return '{} '.format(self.nombre)

class Accion(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
	nombre		 				= models.TextField()
	objetivo_estrategico		= models.TextField()#Quien construye el plan
	descripcion		 			= models.TextField()
	fecha_inicio		 		= models.DateField()
	fecha_termino		 		= models.DateField()
	responsables 				= models.TextField()
	recursos 					= models.TextField()
	medios_verificacion 		= models.ManyToManyField(Medios_verificacion)
	base 				 		= models.ForeignKey(Base)
	
	usuario 					= models.ForeignKey(User)



	def __unicode__(self):
		return '{} {} {} '.format(self.nombre,self.id,self.base.plan.establecimiento.nombre)	
		

class Indicador_base(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
    nombre		 				= models.TextField()
    descripcion		 			= models.TextField()
    objetivo		 			= models.TextField()
    alcance		 				= models.TextField()
    nivel_logro                 = models.IntegerField(choices=LOGRO)
    tipo                        = models.IntegerField(choices=TIPO_INDICADOR, blank=True,null=True)
    justificacion_logro         = models.TextField(blank=True, null=True)
    base 				 		= models.ForeignKey(Base)
    usuario 					= models.ForeignKey(User)

    def get_nivel_logro(self):
        return u'%s' %LOGRO[self.nivel_logro][1]    
    def get_tipo(self):
        return u'%s' %TIPO_INDICADOR[self.tipo][1]    

    def __unicode__(self):
        return '{} {} {}'.format(self.nombre,self.descripcion,self.tipo)	
		
class Plancillo(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
	fecha				 		= models.DateField()
	nombre		 				= models.CharField(max_length=70)
	responsable		 			= models.IntegerField(default=0,choices=RESPONSABLES)
	numero 						= models.IntegerField(choices=TIPO_NUMERO)
	letra 						= models.IntegerField(choices=TIPO_LETRAS)			
	Curso 	 					= models.ForeignKey(curso,blank=True, null=True)
	cantidad_horas 				= models.IntegerField()
	duracion					= models.TextField()
	justificacion 				= models.TextField()
	objetivo_general 			= models.TextField()
	objetivo_especificos 		= models.TextField()
	materiales  		 		= models.TextField()
	reportes 					= models.TextField()
	evaluacion 					= models.IntegerField(default=0,choices=EVALUACION)
	accion 						= models.ForeignKey(Accion)
	usuario 					= models.ForeignKey(User)
	
	def get_responsable(self):
			return u'%s' %RESPONSABLES[self.responsable][1]
	def get_evaluacion(self):
			return u'%s' %EVALUACION[self.evaluacion][1]
	def get_numero(self):
            return u'%s' %TIPO_NUMERO[self.numero][1]
	def get_letra(self):
			return u'%s' %TIPO_LETRAS[self.letra][1]				
	
	def __unicode__(self):
		return '{} {} {} '.format(self.nombre, self.fecha,self.id)		

class Actividades(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
    fecha				 		= models.DateField(blank=True, null=True,default='2019-01-01')
    horario   		  		    = models.IntegerField(choices=TIPO_HORARIO,default=0)
    mes  						= models.IntegerField(default=0,choices=MES)
    nombre		 				= models.CharField(max_length=70)
    tipo 						= models.IntegerField(default=0,choices=TIPO_ACTIVIDAD)
    descripcion					= models.TextField()
    ejecutores 					= models.IntegerField(default=0,choices=EJECUTORES)
    inicio 	 					= models.TextField(blank=True, null=True)
    desarrollo 	 				= models.TextField(blank=True, null=True)
    cierre 	 					= models.TextField(blank=True, null=True)
    	
    participantes 				= models.IntegerField(default=2,choices=PARTICIPANTES)
    numero                      = models.IntegerField(choices=TIPO_NUMERO)
    letra                       = models.IntegerField(choices=TIPO_LETRAS)          

    responsable 				= models.TextField()
    cantidad_convocada 			= models.IntegerField(default=0)
    
    	
    verificadores               = models.ManyToManyField(Verificadores)
    
    observaciones 		 		= models.TextField(default=0)
    planes_externos 	 		= models.ForeignKey(Planes_externos,blank=True, null=True)
    planes_mineduc              = models.ManyToManyField(Planes_mineduc)
    
    evaluacion  				= models.IntegerField(choices=EVALUACION,default=0)
    estado                      = models.IntegerField(choices=ESTADO,default=0)    
    plancillo                   = models.ForeignKey(Plancillo)
    usuario                     = models.ForeignKey(User)
	
    def get_ejecutores(self):
        return u'%s' %EJECUTORES[self.ejecutores][1]
    def get_evaluacion(self):
    	return u'%s' %EVALUACION[self.evaluacion][1]	
    def get_participantes(self):
    	return u'%s' %PARTICIPANTES[self.participantes][1]		
    def get_estado(self):
    	return u'%s' %ESTADO[self.estado][1]
    def get_horario(self):
    	return u'%s' %TIPO_HORARIO[self.horario][1]										
    def get_mes(self):
    	return u'%s' %MES[self.mes][1]	
    def get_tipo(self):
        return u'%s' %TIPO_ACTIVIDAD[self.mes][1]
    def get_numero(self):
        return u'%s' %TIPO_NUMERO[self.numero][1]
    def get_letra(self):
        return u'%s' %TIPO_LETRAS[self.letra][1]    
    	
    def __unicode__(self):
    	return '{} {} {} '.format(self.id,self.nombre, self.fecha)		

    # Estado campo  me indica el estado en el cual esta la actividad
    # 0: Solo creada en el plan+
    # 1: Planificada
    # 2: ejecutada
    # 3: Contingencia - justificada
    # 4: Contingencia - Suspendida
    # 5: Contingencia - cancelada ( Eliminada)
class Hecho_Actividades(models.Model):
	
	#Ingresar cada uno de los niveles de logros por diagnostico
	
    fecha				 		= models.DateField()
    observacion					= models.TextField()
    asistencia                  = models.IntegerField(default=0)
    estado                      = models.IntegerField(choices=ESTADO,default=0)    
# Estado es un Registro propio que indica la accion que se realizo en cada caso  
    actividades                 = models.ForeignKey(Actividades)
    logros                      = models.TextField(blank=True,null=True)
    mejora                      = models.TextField(blank=True,null=True)
    tipo_evaluacion             = models.IntegerField(choices=TIPO_EVALUACION,default=0)    
    nota                        = models.IntegerField(choices=NOTA,default=0)    
    comentario                  = models.TextField()
    usuario 					= models.ForeignKey(User)
    	
    def get_estado(self):
        return u'%s' %ESTADO[self.estado][1]    					
    def get_tipo_evaluacion(self):
        return u'%s' %TIPO_EVALUACION[self.tipo_evaluacion][1] 
    def get_nota(self):
        return u'%s' %NOTA[self.nota][1]           
    def __unicode__(self):
        return '{} {} {}'.format(self.estado, self.fecha, self.actividades.nombre)		

