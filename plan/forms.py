# -*- coding: utf-8 -*-
from django import forms
#from derivacion.models import Area_derivacion
#from derivacion.models import Motivo_derivacion,Escolaridad
from plan.models import  Plan,Base,Indicador_base,Accion,Plancillo,Actividades,Hecho_Actividades,Planes_mineduc
from bootstrap3_datetime.widgets import DateTimePicker


class PlanForm(forms.ModelForm):

	class Meta:
		model = Plan


		fields = [
			
			'fecha',
			'responsable' ,
			'sello',	
			'objetivo_general',
			'objetivo_especificos',
		
		]
		labels = {
			
			'fecha':'Fecha de ingreso plan',
			'responsable':'Grupo de trabajo, participantes en la confección del plan ' ,
			'sello':'Sello del establecimiento',
			'objetivo_general':'Objetivo General',
			'objetivo_especificos':'Objetivos específicos',
			
			

		}
		widgets = {
			
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			#'fecha_derivacion': forms.DateInput(format=('%d-%m-%Y'), 
                                          #   attrs={'class':'myDateClass', 
                                          # 'placeholder':'Select a date'}),

			

			'responsable': forms.TextInput(attrs={'class':'form-control'}),
			'sello': forms.TextInput(attrs={'class':'form-control'}),
			'objetivo_general': forms.Textarea(attrs={'class':'form-control'}),
			'objetivo_especificos': forms.Textarea(attrs={'class':'form-control'}),

			
		}

class PlanFormMineduc(forms.ModelForm):

	class Meta:
		model = Planes_mineduc


		fields = [
			
			'fecha',
			'nombre' ,
			'descripcion',	
			'objetivo_general',
			'docfile1',
		
		]
		labels = {
			
			'fecha':'Fecha de ingreso plan',
			'nombre':'Ingresar nombre del plan ' ,
			'descripcion':'Descripción ',
			'objetivo_general':'Objetivo General',
			'docfile1':'Adjuntar archivo',
			
			

		}
		widgets = {
			
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			#'fecha_derivacion': forms.DateInput(format=('%d-%m-%Y'), 
                                          #   attrs={'class':'myDateClass', 
                                          # 'placeholder':'Select a date'}),

			

			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control'}),
			'objetivo_general': forms.Textarea(attrs={'class':'form-control'}),
			'docfile1':forms.FileInput(attrs={'class':'form-control'}),

			
		}
class Base_PlanForm(forms.ModelForm):

	class Meta:
		model = Base


		fields = [
			
			'nombre',
			'dimension_pme',
			'dimension',
			'objetivo',
			'estrategia',
			#'cantidad_indicadores',
			'cantidad_acciones',

			
		]
		labels = {
			
			'nombre':'Nombre del componente base  a  planificar ',
			'dimension_pme':'Dimensión relacionada con el  PME',
			'dimension':'Indicador',
			'objetivo':'Objetivo',
			'estrategia':'Estrategia',
			#'cantidad_indicadores':'Cantidad de Indicadores a definir',
			'cantidad_acciones':'Cantidad de acciones por componentes ',
			
		
		}
		widgets = {
			
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'dimension_pme':forms.Select(attrs={'class':'form-control'}),
			'dimension': forms.Select(attrs={'class':'form-control'}),
			'objetivo': forms.Textarea(attrs={'class':'form-control'}),
			'estrategia': forms.Textarea(attrs={'class':'form-control'}),
			#'cantidad_indicadores': forms.Select(attrs={'class':'form-control'}),
			'cantidad_acciones': forms.Select(attrs={'class':'form-control'}),
			}

class Indicador_baseForm(forms.ModelForm):

	class Meta:
		model = Indicador_base


		fields = [
			
			'nombre',
			'descripcion',
			'objetivo',
			'alcance',
			'tipo',

			
		
		]
		labels = {
			
			'nombre':'Nombre de identificación del indicador',
			'descripcion':'Descripción del indicador ' ,
			'objetivo':'Objetivo del indicador ' ,
			'alcance':'Identificar el alcance del indicador ' ,
			'tipo':'Selecione el tipo de indicador a ser declarado ' ,
			
			
			

		}
		widgets = {
			
			
			
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'descripcion': forms.Textarea(attrs={'class':'form-control'}),
			'objetivo': forms.Textarea(attrs={'class':'form-control'}),
			'alcance': forms.Textarea(attrs={'class':'form-control'}),
			'tipo': forms.Select(attrs={'class':'form-control'}),
			
		}
#Para modificar el indicador incluyendo el nivel de logros
class Indicador_baseLogroForm(forms.ModelForm):

	class Meta:
		model = Indicador_base


		fields = [
			
			'nombre',
			'descripcion',
			'objetivo',
			'alcance',
			'nivel_logro',
			'justificacion_logro',

			
		
		]
		labels = {
			
			'nombre':'Nombre de identificación del indicador',
			'descripcion':'Descripción del indicador ' ,
			'objetivo':'Objetivo del indicador ' ,
			'alcance':'Identificar el alcance del indicador ' ,
			'nivel_logro':'Porcentaje de nivel de logro ' ,
			'justificacion_logro':'Justificación de exito o fracaso de logro' ,
			
			

		}
		widgets = {
			
			
			
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'descripcion': forms.Textarea(attrs={'class':'form-control'}),
			'objetivo': forms.Textarea(attrs={'class':'form-control'}),
			'alcance': forms.Textarea(attrs={'class':'form-control'}),
			'nivel_logro': forms.Select(attrs={'class':'form-control'}),
			'justificacion_logro': forms.Textarea(attrs={'class':'form-control'}),
			
		}
class Accion_baseForm(forms.ModelForm):

	class Meta:
		model = Accion


		fields = [
			
			'nombre',
			'objetivo_estrategico',
			'descripcion',
			'fecha_inicio',
			'fecha_termino',
			'responsables',
			'recursos',
			'medios_verificacion',
			
		]
		labels = {
			
			'nombre':'Nombre de identificación de la acción',
			'objetivo_estrategico':'Descripción de la estrategica ( Objetivo estratégico)' ,
			'descripcion':'Descripción de la acción ' ,
			'fecha_inicio':'Fecha inicial estimada ' ,
			'fecha_termino':'Fecha de término estimada' ,
			'responsables':'Responsables de la ejecución de la acción',
			'recursos':'Recursos a utilizar ',
			'medios_verificacion':'Medios de verificación',	
			
			

		}
		widgets = {
			
			
			
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'objetivo_estrategico': forms.TextInput(attrs={'class':'form-control'}),
			'descripcion': forms.Textarea(attrs={'class':'form-control'}),
			'fecha_inicio':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'fecha_termino':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'responsables': forms.Textarea(attrs={'class':'form-control'}),
			'recursos': forms.TextInput(attrs={'class':'form-control'}),
			'medios_verificacion':forms.CheckboxSelectMultiple(),
			
		}


class Base_PlancilloForm(forms.ModelForm):

	class Meta:
		model = Plancillo


		fields = [
			
			'fecha',
			'nombre',
			'responsable',
			'numero',
			'letra',
		
			
			'cantidad_horas',
			'duracion',
			'justificacion',
			'objetivo_general',
			'objetivo_especificos',
			'materiales',
			'indicador',
			'reportes',

			

			
		]
		labels = {
			
			'fecha':'Fecha de creación cronología de acciones ',
			'nombre':'Nombre del plan ',
			'responsable':'Responsable / Responsables',
			
			'numero':'Ingresar curso',
			'letra':'Letra del curso',
			'cantidad_horas':'Cantidad total de horas que abordara el plan',
			'duracion':'Indicar duración en meses ',
			'justificacion':'Justificación de la construcción del plan',
			'objetivo_general':'Objetivo general de la cronología de actividades',
			'objetivo_especificos':'Objetivo específico de la cronología de actividades',
			'materiales':'Materiales a utilizar ',
			'indicador':'Ingrese el indicador con el cual esta relacionando',
			'reportes':'Reportes de estado de avance a entregar',

		
		}
		widgets = {

			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),	
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'responsable':forms.Select(attrs={'class':'form-control'}),
			'numero': forms.Select(attrs={'class':'form-control'}),
			'letra': forms.Select(attrs={'class':'form-control'}),
			
			
			'cantidad_horas': forms.TextInput(attrs={'class':'form-control'}),
			'duracion': forms.TextInput(attrs={'class':'form-control'}),
			'justificacion': forms.TextInput(attrs={'class':'form-control'}),
			'objetivo_general': forms.TextInput(attrs={'class':'form-control'}),
			'objetivo_especificos': forms.TextInput(attrs={'class':'form-control'}),
			'materiales': forms.Textarea(attrs={'class':'form-control'}),
			'indicador':forms.Select(attrs={'class':'form-control'}),
			'reportes': forms.TextInput(attrs={'class':'form-control'}),
		
			}

class Base_ActividadesForm(forms.ModelForm):

	class Meta:
		model = Actividades


		fields = [
			
			'fecha',
			'horario', 
			
			'nombre',
			'tipo',
			'descripcion',
			'ejecutores',
			'inicio',
			'desarrollo',
			'cierre',
			'participantes',
			'numero',
			'letra',

			'responsable',
			'cantidad_convocada',
			
			'verificadores',
			'observaciones',
			'planes_externos',
			'planes_mineduc',

			'evaluacion',
			

			
		]
		labels = {
			
			'fecha':'Fecha de la actividad ',
			'horario':'Horario de la actividad',
			'nombre':'Nombre de la actividad',
			'tipo':'Tipo de la actividad',
			'descripcion ':'Descripción de la actividad',
			'ejecutores':'Ejecutores de la actividad',
			'inicio':'Planificación : Inicio',
			'desarrollo':'Planificación : Desarrollo',
			'cierre':'Plaificación : Cierre',
			'participantes':'Participantes a la  actividad',
			'numero':'Curso',
			'letra':'Letra',
			'responsable':'Responsable o responsables de la actividad',

			'cantidad_convocada':'Cantidad de personas convocadas',
			
			'verificadores':'Verificadores de la actividad ',
			'observaciones':'Observaciones',
			'planes_externos':'Programas comunales ',
			'planes_mineduc':'Programas mineduc ',
			
			'evaluacion':'Proceso de evaluación de la actividad',
			


		
		}
		widgets = {

			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),	
			'horario':forms.Select(attrs={'class':'form-control'}),
			
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			
			'tipo':forms.Select(attrs={'class':'form-control'}),
			'descripcion':forms.TextInput(attrs={'class':'form-control'}),
			'ejecutores': forms.Select(attrs={'class':'form-control'}),
			'inicio':forms.Textarea(attrs={'class':'form-control'}),
			'desarrollo':forms.Textarea(attrs={'class':'form-control'}),
			'cierre':forms.Textarea(attrs={'class':'form-control'}),
			'participantes': forms.Select(attrs={'class':'form-control'}),

			'numero': forms.Select(attrs={'class':'form-control'}),
			'letra': forms.Select(attrs={'class':'form-control'}),
			
			'responsable':forms.Textarea(attrs={'class':'form-control'}),	
			'cantidad_convocada': forms.TextInput(attrs={'class':'form-control'}),
			
			'verificadores': forms.CheckboxSelectMultiple(),
			'observaciones': forms.TextInput(attrs={'class':'form-control'}),
			'planes_externos': forms.Select(attrs={'class':'form-control'}),
			'planes_mineduc': forms.CheckboxSelectMultiple(),
			'evaluacion': forms.Select(attrs={'class':'form-control'}),
			
		
			}


#Formulario para modificar la fecha de cada actividad para ingrasar la planificacion
class Base_ActividadesPlanificacion(forms.ModelForm):

	class Meta:
		model = Actividades


		fields = [
			
			'fecha',
			'horario', 
			'nombre',
			'tipo',
			'descripcion',
			'ejecutores',
			'inicio',
			'desarrollo',
			'cierre',
			'participantes',
			'responsable',
			'cantidad_convocada',
			'planes_externos',
			
			

			
		]
		labels = {
			
			'fecha':'Fecha de la actividad ',
			'horario':'Horario de la actividad',
			'nombre':'Nombre de la actividad',
			'tipo':'Tipo de la actividad',
			'descripcion ':'Descripción de la actividad',
			'ejecutores':'Ejecutores de la actividad',
			'inicio':'Planificación : Inicio',
			'desarrollo':'Planificación : Desarrollo',
			'cierre':'Planificación : Cierre',
			'participantes':'Participantes a la  actividad',
			'responsable':'Responsable o responsables de la actividad',
			'cantidad_convocada':'Cantidad de personas convocadas',
			'planes_externos':'Planes externnos ligados a la actividad',
			
			


		
		}
		widgets = {

			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),	
			'horario':forms.Select(attrs={'class':'form-control'}),
			'mes':forms.Select(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			
			'tipo':forms.Select(attrs={'class':'form-control'}),
			'descripcion':forms.TextInput(attrs={'class':'form-control'}),
			'ejecutores': forms.Select(attrs={'class':'form-control'}),
			'inicio':forms.Textarea(attrs={'class':'form-control'}),
			'desarrollo':forms.Textarea(attrs={'class':'form-control'}),
			'cierre':forms.Textarea(attrs={'class':'form-control'}),
			'participantes': forms.Select(attrs={'class':'form-control'}),
			'responsable':forms.Textarea(attrs={'class':'form-control'}),	
			'cantidad_convocada': forms.TextInput(attrs={'class':'form-control'}),
			'planes_externos': forms.Select(attrs={'class':'form-control'}),
			
			}



#Formulario para modificar la fecha de cada actividad para ingrasar la planificacion
class Base_ActividadesPlan(forms.ModelForm):

	class Meta:
		model = Actividades


		fields = [
			
			'mes',
			'nombre',
			'tipo',
			'descripcion',
			'ejecutores',
			'participantes',
			'numero',
			'letra',
			'responsable',
			'planes_externos',
			'planes_mineduc',

			'verificadores',

					
		]
		labels = {
			
			'mes':'Mes aproximado en que se realizará la actividad ',
			'nombre':'Nombre de la actividad',
			'tipo':'Tipo de la actividad',
			'descripcion ':'Descripción de la actividad',
			'ejecutores ':'Selecione a el o los encargados de la actividad ',

			'participantes':'Participantes a la  actividad',
			'numero':'Ingresar el curso',
			'letra':'Ingresar Letra',

			'responsable':'Responsable o responsables de la actividad',
			'planes_externos':'Programas comunales',
			'planes_mineduc':'Programas  institucionales ',
			
			'verificadores':'Verificadores de la actividades',
			
		}
		widgets = {

			'mes':forms.Select(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			
			'tipo':forms.Select(attrs={'class':'form-control'}),
			'descripcion':forms.TextInput(attrs={'class':'form-control'}),
			'ejecutores': forms.Select(attrs={'class':'form-control'}),
			'participantes': forms.Select(attrs={'class':'form-control'}),
			
			'numero':forms.Select(attrs={'class':'form-control'}),
			'letra':forms.Select(attrs={'class':'form-control'}),
			'responsable':forms.Textarea(attrs={'class':'form-control'}),	
			
			'planes_externos': forms.Select(attrs={'class':'form-control'}),
			'planes_mineduc': forms.CheckboxSelectMultiple(),
			'verificadores': forms.CheckboxSelectMultiple(), 
			

        
			}




class Hecho_ActividadesForm(forms.ModelForm):

	class Meta:
		model = Hecho_Actividades


		fields = [
			
			
			'observacion',
			'asistencia', 
			'logros', 
			'mejora', 
			'tipo_evaluacion', 
			'nota', 
			'comentario', 
			
		
			
		]
		labels = {
			
			
			'observacion':'Observación  de la actividad',
			'asistencia':'Asistencia ',
			'logros':'Logros alcanzados',
			'mejora':'Oportunidad de mejora',
			'tipo_evaluacion':'Ingresar tipo de evaluación',
			'nota':'Evaluación obtenida',
			'comentario':'Observación de la evaluación',
			
			
		
		}
		widgets = {

			
			'observacion':forms.Textarea(attrs={'class':'form-control'}),
			'asistencia':forms.TextInput(attrs={'class':'form-control'}),
			'logros':forms.Textarea(attrs={'class':'form-control'}),
			'mejora':forms.Textarea(attrs={'class':'form-control'}),
			'tipo_evaluacion':forms.Select(attrs={'class':'form-control'}),
			'nota':forms.Select(attrs={'class':'form-control'}),

			'comentario':forms.Textarea(attrs={'class':'form-control'}),
			
		
			}

class Justificar_ActividadesForm(forms.ModelForm):

	class Meta:
		model = Hecho_Actividades


		fields = [
			
			'observacion',
			'estado', 	
		]
		labels = {
			
			
			'observacion':'Observación',
			'estado':'Estado '
		}
		widgets = {

			
			'observacion':forms.Textarea(attrs={'class':'form-control'}),
			'estado':forms.Select(attrs={'class':'form-control'}),
		
			}


class Reagendar_ActividadesForm(forms.ModelForm):

	class Meta:
		model = Actividades


		fields = [
			
			'fecha',
			'horario', 
		]
		labels = {
			
			'fecha':'Fecha de la actividad ',
			'horario':'Horario de la actividad',
		
		}
		widgets = {

			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),	
			'horario':forms.Select(attrs={'class':'form-control'}),
			
			
		
			}