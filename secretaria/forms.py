# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from secretaria.models import MascotaRA,agenda,Reserva,Pregunta,agenda_profesional
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from secretaria.models import Confirma



class FormFechas(forms.ModelForm): 

        fecha_desde = forms.DateField() 
        fecha_hasta = forms.DateField() 

class FormPregunta(forms.ModelForm):
	class Meta:
		model = Pregunta 
		fields = '__all__'


class Formconfirma(forms.ModelForm):
	class Meta:
		model = Confirma

		fields = [
			
			'estado1',
			'estado2',
			'estado3',
			'obs',
			
		
		]
		labels = {
		
			'estado1': 'Primera llamada',
			'estado2': 'Segunda llamada',
			'estado3': 'Tercera llamada',
			'obs': ' Comentario general',

			
		}
		widgets = {
			
			'estado1': forms.Select(attrs={'class':'form-control'}),
			'estado1': forms.Select(attrs={'class':'form-control'}),
			'estado1': forms.Select(attrs={'class':'form-control'}),
			'obs': forms.TextInput(attrs={'class':'form-control'}),
			
			

		}


class Formagenda(forms.ModelForm):
	class Meta:
		model = agenda 

		fields = [
			'Estudiante',
			'fecha',
			'horario_i',
			
			'participantes',
			'tipo_actividad',	
		
		]
		labels = {
			'Estudiante': 'Estudiante',
			'fecha':'Fecha de la cita',
			'horario_i': 'Horario inicio de sesión',
			
			'participantes':'Participantes a la sesión',
			'tipo_actividad': 'Tipo Actividad',
			
			
		}
		widgets = {
			'Estudiante': forms.Select(attrs={'class':'form-control'}),
			'Fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			'horarios_i': forms.TextInput(attrs={'class':'form-control'}),
			
			'participantes': forms.Select(attrs={'class':'form-control'}),
			'tipo_actividad': forms.Select(attrs={'class':'form-control'}),
			

		}

# Crear un evento a ser agendado por un profesional que no sea una sesion 

class FormagendaProfesional(forms.ModelForm):
	class Meta:
		model = agenda_profesional 

		fields = [
			
			'fecha',
			'horario_i',
			'horario_t',
			'accion',
			'tipo_actividad',	
			
			
		
		]
		labels = {
			
			'fecha':'Fecha de la cita',
			'horario_i': 'Horario inicio ',
			'horario_t': 'Horario término',
			'accion': 'Acción a realizar',
			'tipo_actividad': 'Tipo Actividad',
			
			
			
			
		}
		widgets = {
			
			'Fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			'horarios_i': forms.TextInput(attrs={'class':'form-control'}),
			'horarios_t': forms.TextInput(attrs={'class':'form-control'}),
			'accion': forms.Select(attrs={'class':'form-control'}),
			'tipo_actividad': forms.Select(attrs={'class':'form-control'}),
			
			
			

		}




class FormagendaCalendario(forms.ModelForm):
	class Meta:
		model = agenda 

		fields = [
			
			'horario_i',
			
			'participantes',
			'tipo_actividad',	
		
		]
		labels = {
			
			'horario_i': 'Horar inicio de sesión',
			
			'participantes':'Participantes a la sesión',
			'tipo_actividad': 'Tipo Actividad',
			
			
		}
		widgets = {
			
			'horarios_i': forms.TextInput(attrs={'class':'form-control'}),
			
			'participantes': forms.Select(attrs={'class':'form-control'}),
			'tipo_actividad': forms.Select(attrs={'class':'form-control'}),
			

		}



class MascotaRAForm(forms.ModelForm):

	class Meta:
		model = MascotaRA

		fields = [
			'fecha',
			'horario_i',
			
			'obs',
			'Estudiante',
			'VacunaT',
			'usuario',
		]
		labels = {
			'fecha':'Fecha de la cita',
			'horario_i': 'Horar inicio de sesion',
			
			'obs': 'Observacion',
			'Estudiante': 'Estudiante',
			'VacunaT': 'Tipo de actividad',
			'usuario':'Seleccionar usuario',
		}
		widgets = {
			'Fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			'horarios_i': forms.TextInput(attrs={'class':'form-control'}),
			
			'Obs': forms.Textarea(attrs={'class':'form-control'}),
			'Estudiante': forms.Select(attrs={'class':'form-control'}),
			'VacunaT': forms.Select(attrs={'class':'form-control'}),
			'usuario': forms.Select(attrs={'class':'form-control'}),

		}

