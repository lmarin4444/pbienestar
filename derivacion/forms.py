# -*- coding: utf-8 -*-
from django import forms
#from derivacion.models import Area_derivacion
#from derivacion.models import Motivo_derivacion,Escolaridad
from derivacion.models import  Ficha_derivacion
from bootstrap3_datetime.widgets import DateTimePicker
from alumno.models import Estudiante
from derivacion.models import Bitacora,intervencion,Retorno, Motivo_Retorno_Ficha_derivacion,Motivo_derivacion


#from derivacion.models import Tipo_atencion
class FormBitacora(forms.ModelForm):
	class Meta:
		model = Bitacora
		fields = '__all__'

class FormRetorno(forms.ModelForm):
	class Meta:
		model = Ficha_derivacion
		fields = '__all__'

		
class IntervencionForm(forms.ModelForm):
	class Meta:
		model = intervencion
		fields = '__all__'

class derivacionForm(forms.ModelForm):

	class Meta:
		model = Ficha_derivacion


		fields = [
			
			'fecha_derivacion',
			
			'pie',
			'anio_pie',
			'edad_f',	
			'habilidades',
			'Red_apoyo',
			'Red_apoyo_obs',
			'edad_f',	
			'Motivo_derivacion' ,
			'cuatro',
			'cinco',
			'conducta',
			'rendimiento',
			'area_responsabilidad',
			'antecedentes_familiares',
			'seis',
			'Imagen',
			
			
		]
		labels = {
			
			'fecha_derivacion':'Fecha que deriva',
			
			'pie':'Pertenece programa Pie?',
			'anio_pie':'Año que pertenece Pie',
			'habilidades':'Participa en el programa H.P.V. (Habilidades para la vida)?',
			'Red_apoyo':'Red de apoyo',
			'Red_apoyo_obs':'DESCRIPCION DETALLE RED DE APOYO',
			'edad_f':'Edad',
			'Motivo_derivacion':'Selecione motivo o motivos',
			'cuatro':'IV. APRECIACIÓN DEL EQUIPO RESPECTO DE MOTIVO DE CONSULTA (POSIBLES CAUSAS O FACTORES, INDICADORES PRESENTES Y ÁMBITOS AFECTADOS –SOCIAL, EDUCACIONAL, FAMILIAR-):',
			'cinco':'V. SEÑALE Y DESCRIBA LAS INTERVENCIONES PREVIAS FRENTE AL MOTIVO CONSULTA Y OBSERVACIONES  DEL ESTUDIANTE EN EL PROCESO (ADHERENCIA, CONDUCTA, ETC).',
			'conducta':'CONDUCTA (elementos más destacables positivos y negativos):',
			'rendimiento':'RENDIMIENTO(área de mayor y menos dificultad, repitencias):',
			'area_responsabilidad':'ÁREA DE RESPONSABILIDAD( asistencia, cumplimiendo de deberes:',
			'antecedentes_familiares':'Composición de la Familia (Genograma y tipo de relaciones:',
			'seis':'Historia familiar (Antecedentes relevantes - Comportamiento figura de cuidado del estudiante - Situación social ej: vulneración de derecho, VIF, Presencia de  alcohol y/o droga )',
			'Imagen':'Ingrese imagen relacionada con la familia',


		}
		widgets = {
			
			
			'fecha_derivacion':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			#'fecha_derivacion': forms.DateInput(format=('%d-%m-%Y'), 
                                          #   attrs={'class':'myDateClass', 
                                          # 'placeholder':'Select a date'}),

			'pie':forms.Select(choices=[(1, 'Si'), (2, 'No')]),
			'anio_pie': forms.TextInput(attrs={'class':'form-control'}),
			'habilidades':forms.Select(choices=[(1, 'Si'), (2, 'No')]),
			'Red_apoyo': forms.Select(),
			'Red_apoyo_obs':forms.Textarea(attrs={'class':'form-control'}),
			'edad_f':forms.TextInput(attrs={'class':'form-control'}),

			'cuatro': forms.Textarea(attrs={'class':'form-control'}),
			'cinco': forms.Textarea(attrs={'class':'form-control'}),
			'conducta': forms.Textarea(attrs={'class':'form-control'}),
			'rendimiento': forms.Textarea(attrs={'class':'form-control'}),
			'area_responsabilidad': forms.Textarea(attrs={'class':'form-control'}),
			'antecedentes_familiares':forms.Textarea(attrs={'class':'form-control'}),
			
			'seis': forms.Textarea(attrs={'class':'form-control'}),
			#'Motivo_derivacion': forms.CheckboxSelectMultiple( attrs={'class':'form-control'}),

			'Motivo_derivacion': forms.CheckboxSelectMultiple(),
			'imagen':forms.FileInput(attrs={'class':'form-control'}),

                    
		}
		

class BitacoraForm(forms.ModelForm):
	class Meta:
	        model = Bitacora
	        fields = ['estado']
	def clean_observacion(self):
		cantidad = self.cleaned_data['cantidad']
		if cantidad == '':
			raise forms.ValidationError("Debe ingresar una cantidad valida")
		return cantidad
# Formulario de retorno desde el centro una vez que el estudiante ya fue aceptado por un profesional del centro
class MotivoRetornoForm(forms.ModelForm):
	class Meta:
			model = Motivo_Retorno_Ficha_derivacion
			fields = [
			
			'motivo_termino',
			'observacion_termino',
			'opcion1',
			'filename1',
			'docfile1',
			'opcion2',
			'filename2',
			'docfile2',
			'opcion3',
			'filename3',
			'docfile3',
			
			'Red_apoyo',

			
		]
	labels = {
			
			'motivo_termino':'Motivo del término',
			'observacion_termino':'Observación o sugerencias',
			
			'opcion1':'Indique Si solo si quiere que el profesional Psicosocial pueda visualizar el archivo',
			'filename1':'Nombre del archivo1',
			'docfile1':'archivo1',
			
			'opcion2':'Indique Si solo si quiere que el profesional Psicosocial pueda visualizar el archivo',
			'filename2':'Nombre del archivo2',
			'docfile2':'archivo2',
			
			'opcion3':'Indique Si solo si quiere que el profesional Psicosocial pueda visualizar el archivo',
			'filename3':'Nombre del archivo3',
			'docfile3':'archivo2',
			'Red_apoyo':'Selecione red a derivar',

			}
	widgets = {
			
			'motivo_termino': forms.Select(attrs={'class':'form-control'}),			 
			'observacion_termino': forms.Textarea(attrs={'class':'form-control'}),
			'opcion1': forms.Select(attrs={'class':'form-control'}),			 
			'docfile1':forms.FileInput(attrs={'class':'form-control'}),
			'filename1': forms.TextInput(attrs={'class':'form-control'}),
			'opcion2': forms.Select(attrs={'class':'form-control'}),			 
			'docfile2':forms.FileInput(attrs={'class':'form-control'}),	
			'filename2': forms.TextInput(attrs={'class':'form-control'}),
			'opcion3': forms.Select(attrs={'class':'form-control'}),			 
			'docfile3':forms.FileInput(attrs={'class':'form-control'}),	
			'filename3': forms.TextInput(attrs={'class':'form-control'}),
			'Red_apoyo': forms.Select(attrs={'class':'form-control'}),			 

			
		}
#Formulario de retorno por falta de informacion en la ficha de derivacion 
class RetornoFaltainfoForm(forms.ModelForm):
	class Meta:
		model = Motivo_Retorno_Ficha_derivacion
		fields = [
		
			'observacion_termino',
			
		]
	labels = {
			
			'observacion_termino':'Observación  ',
			
			}
	widgets = {
			
			'observacion_termino': forms.Textarea(attrs={'class':'form-control'}),			 
						
		}

    