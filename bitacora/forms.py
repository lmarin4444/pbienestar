# -*- coding: utf-8 -*-
#from  bootstrap_datepicker.widgets  import  DatePicker
from django import forms
from alumno.models import establecimiento
from bitacora.models import Lista


class BitacoraForm(forms.ModelForm):
	
	class Meta:
		model = Lista


		fields = [
			
			'fecha',
			'horario',
			'nombre',
			'curso',
			'tipo_letras',
			'ambito',
			'tipo_actividad',
			'participantes',
			'desarrollo',
		]
		labels = {
			'fecha': 'Fecha',
			'horario': 'Horario',
			'nombre':'Nombre de la acción',
			'curso': 'Curso o nivel',
			'tipo_letras':' Letra',
			'ambito':'Área de acción de la actividad',
			'tipo_actividad':'Tipo de la actividad',
			'participantes': 'Participantes de la actividad',
			
			'desarrollo':'Describa la actividad realizada',
																	
		}
		widgets = {
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'horario': forms.Select(attrs={'class':'form-control'}),
			'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Actividad '}),
			'desarrollo': forms.TextInput(attrs={'class':'form-control'}),

		}

