# -*- coding: utf-8 -*-
from django import forms
#from derivacion.models import Area_derivacion
#from derivacion.models import Motivo_derivacion,Escolaridad
from dupla.models import  Ficha_derivacion_dupla,Entrevista_ingreso_dupla,DiagnosticoI,Logros,Indicador,Dimensiones, \
Intervencion_casos,Intervencion_sesion,Intervencion_convivencia,Derivacion_Ficha_derivacion_dupla, Intervencion_convivencia_curso, \
Relacion_Intervencion_convivencia_estudiante,Intervencion_convivencia_mediacion, Continuidad_dupla
from sesion.models import Seguimiento

from alumno.models import Estudiante
from bootstrap3_datetime.widgets import DateTimePicker




class derivacionduplaForm(forms.ModelForm):

	class Meta:
		model = Ficha_derivacion_dupla


		fields = [
			
			'fecha_derivacion',
			
			'quien_deriva',
			'profe_jefe',

			'Motivo_derivacion_dupla' ,
			'conducta',	
			'afecta',
			'reiterada',
			'marzo',	
			'abril',	
			'mayo',	
			'junio',	
			'julio',	
			'agosto',	
			'septiembre',	
			'octubre',	
			'noviembre',	
			'diciembre',
			'observacion',

			
		]
		labels = {
			
			'fecha_derivacion':'Fecha que deriva',
			'Motivo_derivacion_dupla':'Seleccionar motivo de la derivación ' ,
			

			'quien_deriva':'Persona que realiza la derivación ejemplo: Profesor jefe',
			'profe_jefe':'Profesor jefe (Si es la misma persona quien deriva ingresar dos veces) ',
			'conducta':'¿La conducta identificada, afecta el proceso de enseñanza-aprendizaje del estudiante?',
			'afecta':'¿Como afecta?',
			'reiterada':'¿Desde cuando se reitera la conducta?',
			'marzo':'Inasistencia mes de marzo',
			'abril':'Inasistencia mes de abril',
			'mayo':'Inasistencia mes de mayo',
			'junio':'Inasistencia mes de junio',
			'julio':'Inasistencia mes de julio',
			'agosto':'Inasistencia mes de agosto',
			'septiembre':'Inasistencia mes de septiembre',
			'octubre':'Inasistencia mes de octubre',
			'noviembre':'Inasistencia mes de noviembre',
			'diciembre':'Inasistencia mes de diciembre ',
			'observacion':'Entrevista con el profesor que deriva (Observaciones generales)',
			

		}
		widgets = {
			
			
			'fecha_derivacion':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			
			'quien_deriva':forms.TextInput(attrs={'class':'form-control'}),
			'profe_jefe':forms.TextInput(attrs={'class':'form-control'}),
			'marzo':forms.TextInput(attrs={'class':'form-control'}),
			'abril':forms.TextInput(attrs={'class':'form-control'}),
			'mayo':forms.TextInput(attrs={'class':'form-control'}),
			'junio':forms.TextInput(attrs={'class':'form-control'}),
			'julio':forms.TextInput(attrs={'class':'form-control'}),
			'agosto':forms.TextInput(attrs={'class':'form-control'}),
			'septiembre':forms.TextInput(attrs={'class':'form-control'}),
			'octubre':forms.TextInput(attrs={'class':'form-control'}),
			'noviembre':forms.TextInput(attrs={'class':'form-control'}),
			'diciembre':forms.TextInput(attrs={'class':'form-control'}),

			'conducta': forms.Textarea(attrs={'class':'form-control'}),
			'afecta': forms.Textarea(attrs={'class':'form-control'}),
			'reiterada': forms.Textarea(attrs={'class':'form-control'}),
			'observacion': forms.Textarea(attrs={'class':'form-control'}),

			#'Motivo_derivacion': forms.CheckboxSelectMultiple( attrs={'class':'form-control'}),

			'Motivo_derivacion_dupla': forms.CheckboxSelectMultiple(),
			

                    
		}
		
class Entrevista_ingreso_duplaForm(forms.ModelForm):

	class Meta:
		model = Entrevista_ingreso_dupla


		fields = [
			
			'fecha_derivacion',

			'atencion_previa',
			'familia',
			'imagen',
			'problematica',	
			
		]
		labels = {
			
			'fecha_derivacion':'Fecha que deriva',
			'atencion_previa':'¿Indique antención previa, cuál?',
			'familia':'Composición de la familia ( Genograma y tipo de relaciones),comportamiento figuras de cuidado del estudiante, situación social( Ej: vulneración de derecho, VIF, Presencia de alcoholismo u drogas) o situación de salud.',
			'imagen':'Genograma',
			'problematica':'APRECIACIOÓN DE LAS POSIBLES PROBLEMÁTICAS DE ANÁLISIS (POSIBLES CAUSAS O FACTORES, INDICADORES PRESENTES Y ÁMBITO AFECTADOS - SOCIAL - EDUCACIONAL - FAMILIAR)',

			

		}
		widgets = {
			
			
			'fecha_derivacion':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			#'fecha_derivacion': forms.DateInput(format=('%d-%m-%Y'), 
                                          #   attrs={'class':'myDateClass', 
                                          # 'placeholder':'Select a date'}),

			'atencion_previa':forms.TextInput(attrs={'class':'form-control'}),
			'familia':forms.Textarea(attrs={'class':'form-control'}),
			'imagen':forms.FileInput(attrs={'class':'form-control'}),
			'problematica':forms.Textarea(attrs={'class':'form-control'}),			

                    
		}

class ContinuidadForm(forms.ModelForm):

	class Meta:
		model = Continuidad_dupla


		fields = [
			
			'fecha',
			'motivo_continuidad',
			'observacion',
			
		]
		labels = {
			
			'fecha':'Fecha ',
			'motivo_continuidad':'Motivo continuidad',
			'observacion':'Observación ( Especifique el motivo)',
		
		}
		widgets = {
			
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'motivo_continuidad':forms.CheckboxSelectMultiple(),
			'observacion':forms.Textarea(attrs={'class':'form-control'}),
			

                    
		}		


class Diagnostico_duplaForm(forms.ModelForm):

	class Meta:
		model = DiagnosticoI


		fields = [
			
			'fecha_diagnostico',
			'responsables',
			'resumen',
			'acuerdos',
			'desacuerdos',
			'plenario',
			
			
		]
		labels = {
			
			'fecha_diagnostico':'Fecha de ingreso diagnóstico',
			'responsables':'Descripción del equipo que construyó el diagnóstico ',
			'resumen':'Resumen general ',
			'acuerdos':'Descripción de los acuerdos  ',
			'desacuerdos':'Descripción de los desacuerdos  ',
			'plenario':'Descripción de las conclusiones finales',

			
		



		}
		widgets = {
			
			
			'fecha_diagnostico':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			#'fecha_derivacion': forms.DateInput(format=('%d-%m-%Y'), 
                                          #   attrs={'class':'myDateClass', 
                                          # 'placeholder':'Select a date'}),

			'responsables':forms.TextInput(attrs={'class':'form-control'}),
			'resumen':forms.Textarea(attrs={'class':'form-control'}),
			'acuerdos':forms.Textarea(attrs={'class':'form-control'}),
			'desacuerdos':forms.Textarea(attrs={'class':'form-control'}),
			
			'plenario':forms.Textarea(attrs={'class':'form-control'}),
			
			
                    
		}		
		


class IndicadorAuto_duplaForm(forms.ModelForm):

	class Meta:
		model = Logros


		fields = [
			
			'porcentaje',
			'observacion',
			'dimension',

			
		]
		labels = {
			
			'porcentaje':'Debe ingresar valores desde el 0 hasta el 100 ',
			'observacion':'Observación a registrar',
			'dimension':'Dimensión',
		
		}
		widgets = {
			
			'porcentaje':forms.TextInput(attrs={'class':'form-control'}),
			'observacion':forms.Textarea(attrs={'class':'form-control'}),
			'dimension': forms.Select(attrs={'class':'form-control'}),
			}

			
class Intervencion_casosForm(forms.ModelForm):

	class Meta:
		model = Intervencion_casos


		fields = [
			
			
			'fecha',
			'problematica',
			'objetivo_general',
			'objetivo_especifico',
			'Tematicas',
			'Area_intervencion',
			'cantidad',	

			
		]
		labels = {
			
			'fecha':'Seleccionar fecha de creación plan de intervención ',
			'problematica':'Contextualizar Problemática ',
			'objetivo_general':'Objetivo General',
			'objetivo_especifico':'Objetivo Específico',
			'Tematicas':'Temática a ser tratada',
			'Area_intervencion':'Áreas de intervención a ser tratadas',
			'cantidad':'Cantidad de sesiones',
		
		}
		widgets = {
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'problematica':forms.Textarea(attrs={'class':'form-control'}),
			'objetivo_general':forms.Textarea(attrs={'class':'form-control'}),
			'objetivo_especifico':forms.Textarea(attrs={'class':'form-control'}),
			'Tematicas': forms.CheckboxSelectMultiple(),
			'Area_intervencion': forms.CheckboxSelectMultiple(),
			'cantidad':forms.Select(attrs={'class':'form-control'}),
			}

class Intervencion_sesionForm(forms.ModelForm):

	class Meta:
		model = Intervencion_sesion


		fields = [
			
			
			'fecha',
			'horario',
			'objetivo_especifico',
			'tematicas',
			'area_intervencion',
			'observacion',
			'participantes',	
			'numero',	

			
		]
		labels = {
			
			'fecha':'Seleccionar fecha de  sesión ',
			'horario':'Seleccionar horario de  sesión ',
			'objetivo_especifico':'Objetivo Especifico',
			'tematicas':'Temática a ser tratada',
			'area_intervencion':'Áreas de intervención a ser tratadas',
			'observacion':'Observación',
			'participantes':'Asistentes a la sesión',
			'numero':'Estado de la sesión',
		
		}
		widgets = {
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'horario':forms.Select(attrs={'class':'form-control'}),
			'objetivo_especifico':forms.Textarea(attrs={'class':'form-control'}),
			'tematicas':forms.Textarea(attrs={'class':'form-control'}),
			'area_intervencion': forms.CheckboxSelectMultiple(),
			'observacion':forms.Textarea(attrs={'class':'form-control'}),
			'participantes':forms.Select(attrs={'class':'form-control'}),
			'numero':forms.Select(attrs={'class':'form-control'}),
			}
# Registro de los datos para una sesion sin registrar fecha - horario
class Intervencion_asistencia_sesionForm(forms.ModelForm):

	class Meta:
		model = Intervencion_sesion


		fields = [
			
			
			
			'objetivo_especifico',
			'tematicas',
			'area_intervencion',
			'observacion',
			'participantes',	
		

			
		]
		labels = {
			
			
			'objetivo_especifico':'Objetivo Específico',
			'tematicas':'Temática a ser tratada',
			'area_intervencion':'Áreas de intervención a ser tratadas',
			'observacion':'Observación',
			'participantes':'Asistentes a la sesión',
			
		
		}
		widgets = {
			
			
			'objetivo_especifico':forms.Textarea(attrs={'class':'form-control'}),
			'tematicas':forms.Textarea(attrs={'class':'form-control'}),
			'area_intervencion': forms.CheckboxSelectMultiple(),
			'observacion':forms.Textarea(attrs={'class':'form-control'}),
			'participantes':forms.Select(attrs={'class':'form-control'}),
			
			}
# Registrar el registro asistencia a una sesion por parte del estudiante 
class Intervencion_sesioninicialForm(forms.ModelForm):

	class Meta:
		model = Intervencion_sesion


		fields = [
			
			
			'fecha',
			'horario',
			

			'area_intervencion',
			
			
		]
		labels = {
			
			'fecha':'Seleccionar fecha de la sesión ',
			'horario':'Seleccionar horario de la sesión ',
			
			'area_intervencion':'Áreas de intervención a ser tratadas',
			
		
		}
		widgets = {
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'horario':forms.Select(attrs={'class':'form-control'}),
			
			'area_intervencion': forms.CheckboxSelectMultiple(),
			
			}




class Intervencion_convivenciaForm(forms.ModelForm):

	class Meta:
		model = Intervencion_convivencia


		fields = [
			
			
			'fecha',
			'horario',
			'observacion',
		
			'participantes',
			'dimensiones',        
			

			
		]
		labels = {
			
			'fecha':'Seleccionar Fecha  ',
			'horario':'Seleccionar Horario ',
			'observacion':'Observación',
			
			'participantes':'Participantes ',
			'dimensiones':'Indique la relación con los indicadores de desarrollo personal y social',
			
		
		}
		widgets = {
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'horario':forms.Select(attrs={'class':'form-control'}),
			
			'observacion':forms.Textarea(attrs={'class':'form-control'}),

			
			'participantes':forms.Select(attrs={'class':'form-control'}),
			'dimensiones':forms.Select(attrs={'class':'form-control'}),
			
			}

class Intervencion_convivencia_mediacionForm(forms.ModelForm):

	class Meta:
		model = Intervencion_convivencia_mediacion


		fields = [
			
			
			'fecha',
			'horario',
			'observacion',
		
			'participantes',
			'dimensiones',        
			

			
		]
		labels = {
			
			'fecha':'Seleccionar Fecha  ',
			'horario':'Seleccionar Horario ',
			'observacion':'Observación',
			
			'participantes':'Participantes ',
			'dimensiones':'Relación con los indicadores de desarrollo personal y social',
			
		
		}
		widgets = {
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'horario':forms.Select(attrs={'class':'form-control'}),
			
			'observacion':forms.Textarea(attrs={'class':'form-control'}),

			
			'participantes':forms.Select(attrs={'class':'form-control'}),
			'dimensiones':forms.Select(attrs={'class':'form-control'}),
			
			}			

class Derivacion_Ficha_derivacionForm(forms.ModelForm):
	class Meta:
			model = Derivacion_Ficha_derivacion_dupla
			fields = [
			
			'fecha_retorno', 
			'motivo_termino',
			'observacion_termino',
			
			'filename1',
			'docfile1',
			
			'filename2',
			'docfile2',
			
			'filename3',
			'docfile3',
			
			'Red_apoyo',

			
		]
	labels = {
			
			'fecha_retorno':'Fecha ',
			'motivo_termino':'Motivo del término',
			'observacion_termino':'Observación o sugerencias',
			
			
			'filename1':'Nombre del archivo1',
			'docfile1':'archivo1',
			
			
			'filename2':'Nombre del archivo2',
			'docfile2':'archivo2',
			
			
			'filename3':'Nombre del archivo3',
			'docfile3':'archivo2',
			'Red_apoyo':'Selecione red a derivar',

			}
	widgets = {
			'fecha_retorno':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'motivo_termino': forms.Select(attrs={'class':'form-control'}),			 
			'observacion_termino': forms.TextInput(attrs={'class':'form-control'}),
			
			'docfile1':forms.FileInput(attrs={'class':'form-control'}),
			'filename1': forms.TextInput(attrs={'class':'form-control'}),
			
			'docfile2':forms.FileInput(attrs={'class':'form-control'}),	
			'filename2': forms.TextInput(attrs={'class':'form-control'}),
			
			'docfile3':forms.FileInput(attrs={'class':'form-control'}),	
			'filename3': forms.TextInput(attrs={'class':'form-control'}),
			'Red_apoyo': forms.Select(attrs={'class':'form-control'}),			 

			
		}




class Intervencion_convivencia_cursoForm(forms.ModelForm):

	class Meta:
		model = Intervencion_convivencia_curso


		fields = [
			
			
			'fecha',
			'horario',
			'observacion',
		
			'participantes',
			'dimensiones', 
			'observacion_curso',
			'curso', 
			'letra', 

		
		]
		labels = {
			
			'fecha':'Seleccionar Fecha  ',
			'horario':'Seleccionar Horario ',
			'observacion':'Observación',
			
			'participantes':'Participantes ',
			'dimensiones':'Relación con los indicadores de desarrollo personal y social',
			'observacion_curso':'Observación particular del curso, o del curso con más cursos relacionados',
			'curso':'Seleccionar curso ',
			'letra':'Seleccionar Letra',
		
		}
		widgets = {
			
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'horario':forms.Select(attrs={'class':'form-control'}),
			
			'observacion':forms.Textarea(attrs={'class':'form-control'}),

			
			'participantes':forms.Select(attrs={'class':'form-control'}),
			'dimensiones':forms.Select(attrs={'class':'form-control'}),
			'observacion_curso':forms.Textarea(attrs={'class':'form-control'}),
			'curso':forms.Select(attrs={'class':'form-control'}),
			'letra':forms.Select(attrs={'class':'form-control'}),
			
			}		


#class MeasurementForm(ModelForm):
#    class Meta:
#        model = Estudiante
#    def __init__(self, *args, **kwargs):
#        experiment = kwargs.pop('experiment')
#        super(MeasurementForm, self).__init__(*args, **kwargs)
#        self.fields["subject"].queryset = Subject.objects.filter(experiment=experiment)



class BuscarMoverForm(forms.Form):


	observacion_estudiante=forms.Textarea()
	estudiante = forms.ModelChoiceField(queryset=Relacion_Intervencion_convivencia_estudiante.objects.none())


	def __init__(self, idcolegio, *args, **kwargs):
		super(BuscarMoverForm, self).__init__(*args, **kwargs)
		self.fields['estudiante'].queryset =Estudiante.objects.filter(curso__establecimiento__id=idcolegio)

# Formulario para ingresar la sesion 
class Intervencion_sesionIngresar(forms.ModelForm):

	class Meta:
		model = Intervencion_sesion


		fields = [
			
			'objetivo_especifico',
			'tematicas',
			'area_intervencion',
			'observacion',
			'participantes',	
			
		]
		labels = {
			
			'objetivo_especifico':'Objetivo Especifico',
			'tematicas':'Tematica a ser tratada',
			'area_intervencion':'Áreas de intervención a ser tratada',
			'observacion':'Observación',
			'participantes':'Asistentes a la sesión',
			
		
		}
		widgets = {
			
			
			
			'objetivo_especifico':forms.Textarea(attrs={'class':'form-control'}),
			'tematicas':forms.Textarea(attrs={'class':'form-control'}),
			'area_intervencion': forms.CheckboxSelectMultiple(),
			'observacion':forms.Textarea(attrs={'class':'form-control'}),
			'participantes':forms.Select(attrs={'class':'form-control'}),
			
			}

# Registro para anular una cita 

class Intervencion_anular_sesionForm(forms.ModelForm):

	class Meta:
		model = Intervencion_sesion


		fields = [
		
			'observacion',
	
		

			
		]
		labels = {
			
			
			'observacion':'Observación',

			
		
		}
		widgets = {
			

			'observacion':forms.Textarea(attrs={'class':'form-control'}),

			
			}
	
# SEGUIMIENTO DE LOS CASOS DE LAS DUPLAS
class SeguimientoForm(forms.ModelForm):

	class Meta: 
		model = Seguimiento

		fields = [
			
			'fecha',
			'observacion',
			'tipo_seg',
			'tipo_s',
				
		]
		labels = {
			'fecha':'Fecha',
			'observacin':'Acciones relalizadas',
			'tipo_seg':'Tipo de seguimiento',
			'tipo_s':'Origen del seguimiento',


		}
		widgets = {
			
			'fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			'observacion': forms.Textarea(attrs={'class':'form-control'}),	
			'tipo_seg': forms.Select(attrs={'class':'form-control'}),
			'tipo_s': forms.Select(attrs={'class':'form-control'}),

		}