# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from sesion.models import tipo_sesion,pruebas,sesion,Diagnostico,Tematicas, \
objetivo_intervencion,Reporte_continuidad,Ficha_de_egreso,Motivo_egreso,Seguimiento
from secretaria.models import agenda,Registro
from django.forms.widgets import CheckboxSelectMultiple

class FormCita(forms.ModelForm):
	class Meta:
		model = agenda 

		fields = [
			
			'fecha',
			'horario_i',
			
			'participantes',
			'tipo_actividad',
			'furgon',	
		
		]
		labels = {
			
			'fecha':'Fecha de la cita',
			'horario_i': 'Horario inicio de sesión',
			
			'participantes':'Participantes a la sesión',
			'tipo_actividad': 'Tipo Actividad',
			'furgon': 'Seleccione necesidad de furgón',
			
			
		}
		widgets = {
			'fecha':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			
			'horarios_i': forms.TextInput(attrs={'class':'form-control'}),
			
			'participantes': forms.Select(attrs={'class':'form-control'}),
			'tipo_actividad': forms.Select(attrs={'class':'form-control'}),
			
			

		}

	
class DiagnosticoForm(forms.ModelForm):
	class Meta:
		model = Diagnostico


		fields = [
			
			'situacion_actual',
			'observaciones',
			'familia',		
		]
		labels = {

			'situacion_actual':'Situación actual',
			'observaciones':'Observaciones',
			'familia':'Sugerencias a la familia'
		}
		widgets = {
			
			
			'situacion_actual': forms.Textarea(attrs={'class':'form-control'}),
			'observaciones': forms.Textarea(attrs={'class':'form-control'}),
			'familia': forms.Textarea(attrs={'class':'form-control'}),
			
		}
class ContinuidadForm(forms.ModelForm):
	class Meta:
		model = Reporte_continuidad

		fields = [
			
			'motivo',
			'antecedentes',
			'observaciones',		
			'sugerencias',
		]
		labels = {

			'motivo':'Selecionar motivo del egreso',
			'antecedentes':'Antecedentes',
			'observaciones':'Observaciones',
			'sugerencias':'Sugerencias',
		}
		widgets = {
			
			
			'motivo': forms.Select(attrs={'class':'form-control'}),
			'antecedentes': forms.Textarea(attrs={'class':'form-control'}),
			'observaciones': forms.Textarea(attrs={'class':'form-control'}),
			'sugerencias': forms.Textarea(attrs={'class':'form-control'}),
			
			
		}

class FichaEgresoForm(forms.ModelForm):
	class Meta:
		model = Ficha_de_egreso


		fields = [
			
			'Motivo_egreso',
			'sintesis',
			'sugerencias',		
			
		]
		labels = {

			'Motivo_egreso':'Motivo de egreso',
			'sintesis':'Síntesis',
			'Sugerencias':'Sugerencias',
		}
		widgets = {
			
			'Motivo_egreso': forms.Select(attrs={'class':'form-control'}),
			'sintesis': forms.Textarea(attrs={'class':'form-control'}),
			'sugerencias': forms.Textarea(attrs={'class':'form-control'}),
		
		}

class Tipo_sesionForm(forms.ModelForm):
	class Meta:
		model = tipo_sesion
		
		fields = [
				'nombre',
				'observacion',
			]

		labels = {

			'nombre':'Nombre tipo sesión',
			'observacion':'Obervación',
			

		}
		widgets = {
			
			
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'observacion': forms.TextInput(attrs={'class':'form-control'}),
			
	

		}




class CrearRegistroForm(forms.ModelForm):

	class Meta:
		model = Registro

		fields = [
			
			'situacion',
			'obs',
			'otros',
			
		]
		labels = {

			'situacion':'Acción ocurrida',
			'obs':'Observación',
			'otros':'Observación adicional',
			}
		widgets = {
			
			'situacion': forms.Select(attrs={'class':'form-control'}),
			'obs': forms.Textarea(attrs={'class':'form-control'}),
			'otros': forms.Textarea(attrs={'class':'form-control'}),

			

		}




class ModificarRegistroForm(forms.ModelForm):

	class Meta:
		model = Registro

		fields = [
			
			
			'situacion',
			'obs',
			'otros',
			
		]
		labels = {
			
			'situacion':'Acción ocurrida',
			'obs':'Observación',
			'otros':'Observación adicional',
			}
		widgets = {
			
			'situacion': forms.Select(attrs={'class':'form-control'}),
			'obs': forms.Textarea(attrs={'class':'form-control'}),
			'otros': forms.Textarea(attrs={'class':'form-control'}),

			

		}		
class SesionForm(forms.ModelForm):

	class Meta:
		model = sesion

		fields = [
			'fecha',
			'publico',
			'privado',
			'observacion',
			'participantes',
			'pruebas',
			'tipo_sesion',
			
			'Estudiante',
			
		]
		labels = {

			'fecha':'Fecha de la sesión',
			
			'publico':'Área de texto público',
			'privado':'Área de texto privado',
			'observacion':'Objetivo específico',
			'participantes':'Participantes a la sesión',
			
			'pruebas':'Pruebas si es necesario',
			'tipo_sesion':'Selecione el tipo de sesión',
			
			'Estudiante':'Estudiante',


		}
		widgets = {
			
			'fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			
			'publico': forms.Textarea(attrs={'class':'form-control'}),
			'privado': forms.Textarea(attrs={'class':'form-control'}),
			'observacion': forms.TextInput(attrs={'class':'form-control'}),
			'participantes': forms.Select(attrs={'class':'form-control'}),
			
			'pruebas': forms.Select(attrs={'class':'form-control'}),
			'tipo_sesion': forms.Select(attrs={'class':'form-control'}),
			
			'Estudiante': forms.Select(attrs={'class':'form-control'}),

		


		}


class SesionModificarForm(forms.ModelForm):

	class Meta:
		model = sesion

		fields = [
			
			'observacion',
			'publico',
			'privado',
			
			'participantes',
			'pruebas',
			'tipo_sesion',
			
			
			
		]
		labels = {

			'observacion':'Objetivo específico',
			'publico':'Área de texto público',
			'privado':'Área de texto privado',
			
			'participantes':'Participantes a la sesión',
			
			'pruebas':'Pruebas si es que es necesario',
			'tipo_sesion':'Selecione el tipo de sesión',
			
		}
		widgets = {

			'observacion': forms.TextInput(attrs={'class':'form-control'}),
			'publico': forms.Textarea(attrs={'class':'form-control'}),
			'privado': forms.Textarea(attrs={'class':'form-control'}),
			'participantes': forms.Select(attrs={'class':'form-control'}),
			'pruebas': forms.Select(attrs={'class':'form-control'}),
			'tipo_sesion': forms.Select(attrs={'class':'form-control'}),
		}		
	
class SesionFormCalendar(forms.ModelForm):

	class Meta:
		model = sesion

		fields = [
			'observacion',
			'publico',
			'privado',
			
			'participantes',
			'pruebas',
			'tipo_sesion',
			
			
		]
		labels = {

			'observacion':'Objetivo específico',
			'privado':'Área de texto privada',
			'publico':'Área de texto pública',
			
			'participantes':'Participantes a la sesión',
			
			'pruebas':'Pruebas si es que es necesario',
			'tipo_sesion':'Selecione el tipo de sesión',
		

		}
		widgets = {
			
			'Fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			'observacion': forms.TextInput(attrs={'class':'form-control'}),
			'publico': forms.Textarea(attrs={'class':'form-control'}),
			'privado': forms.Textarea(attrs={'class':'form-control'}),
			
			'participantes': forms.Select(attrs={'class':'form-control'}),
			
			'pruebas': forms.Select(attrs={'class':'form-control'}),
			'tipo_sesion': forms.Select(attrs={'class':'form-control'}),
			
			

	

		}



class SesionIniciaForm(forms.ModelForm):

	class Meta:
		model = sesion

		fields = [
			'fecha',
			
			'publico',
			'privado',
			'observacion',
			'participantes',
			'pruebas',
			'tipo_sesion',
			
			
		]
		labels = {

			'fecha':'Fecha de la sesión',
			
			'privado':'Área de texto privada',
			'publico':'Área de texto pública',
			'observacion':'Observación',
			'participantes':'Participantes a la sesión',
			
			'pruebas':'Pruebas si es que es necesario',
			'tipo_sesion':'Selecionar tipo de sesión',
			

		}
		widgets = {
			
			'Fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			
			'publico': forms.Textarea(attrs={'class':'form-control'}),
			'privado': forms.Textarea(attrs={'class':'form-control'}),
			'observacion': forms.TextInput(attrs={'class':'form-control'}),
			'participantes': forms.Select(attrs={'class':'form-control'}),
			
			'pruebas': forms.Select(attrs={'class':'form-control'}),
			'tipo_sesion': forms.Select(attrs={'class':'form-control'}),
			
			

		


		}



class TematicaForm(forms.ModelForm):

	class Meta:
		model = Tematicas

		fields = [
			'nombre',
			'descripcion',
			
			
		]
		labels = {

			'nombre':'Nombre de la temática',
			'descripcion':'Descripción de la temática',
			

		}
		widgets = {
			
			
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'descripcion': forms.Textarea(attrs={'class':'form-control'}),
			

		}



class Objetivo_intervencionForm(forms.ModelForm):

	class Meta:
		model = objetivo_intervencion

		fields = [
			
			'objetivo_particular',
			'Tematicas',
		]
		labels = {
			
			'objetivo_particular':'Descripción del Objetivo',
			'Tematicas':'Selecionar temática(as)',
		}
		widgets = {
			
			
			'objetivo_particular': forms.Textarea(attrs={'class':'form-control'}),	
			
			'Tematicas': forms.CheckboxSelectMultiple(),
		}


class motivo_egresoForm(forms.ModelForm):

	class Meta: 
		model = Motivo_egreso

		fields = [
			
			'nombre',
			'descripcion',
		]
		labels = {
			
			'nombre':'Nombre del motivo de egreso',
			'descripcion':'Descripción',
		}
		widgets = {
			
			
			'nombre': forms.TextInput(attrs={'class':'form-control'}),	
			'descripcion': forms.TextInput(attrs={'class':'form-control'}),
		}

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
			'tipo_seg':'Actividad de seguimiento',
			'tipo_s':'Origen del seguimiento'


		}
		widgets = {
			
			'fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			'observacion': forms.Textarea(attrs={'class':'form-control'}),	
			'tipo_seg': forms.Select(attrs={'class':'form-control'}),
			'tipo_s': forms.Select(attrs={'class':'form-control'}),

		}
# Formulario para el centro de bienestar
class SeguimientocentroForm(forms.ModelForm):

	class Meta: 
		model = Seguimiento

		fields = [
			
			'fecha',
			'observacion',
			'tipo_seg',
			
				
		]
		labels = {
			'fecha':'Fecha',
			'observacion':'Acciones relalizadas',
			'tipo_seg':'Actividad de seguimiento',
			


		}
		widgets = {
			
			'fecha':forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'datepicker','placeholder':'Selecionar Fecha '}),
			'observacion': forms.Textarea(attrs={'class':'form-control'}),	
			'tipo_seg': forms.Select(attrs={'class':'form-control'}),
			

		}


