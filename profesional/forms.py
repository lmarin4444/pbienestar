# -*- coding: utf-8 -*-
from django import forms
from profesional.models import Profesional,Cargo,Acciones_profesional
from secretaria.models import agenda
from sesion.models import Intervenidos,Pasos_intervencion

class CambioProfesionalForm(forms.ModelForm):
	
	class Meta:
		model = Pasos_intervencion
		fields = [
			
			'usuario',
			'observacion',
			
		]
		labels = {
			
			
			'usuario':'Seleccione nuevo Profesional',	
			'observacion':'observación',
		}
		widgets = {
			
			'usuario':forms.Select(attrs={'class':'form-control'}),
			'observacion':forms.TextInput(attrs={'class':'form-control'}),
			
		}





class profesionalForm(forms.ModelForm):

	class Meta:
		model = Profesional

		fields = [
			'rut',
			'adress',
			'phone',
			'tipo_profesional',
			'usuario',
			'establecimiento',
		]
		labels = {
			'rut ': 'Rut Profesinal',
			'adress':'Domicilio',
			'phone': 'Teléfono',
			'tipo_profesional':'Tipo de profesional',
			'usuario':'Seleccione el user a asignar al profesional, debe ser ingresado anteriormente',	
			'establecimiento':'Establecimiento relacionado, sino tiene establecimiento asignado elegir SA',
		}
		widgets = {
			'rut': forms.TextInput(attrs={'class':'form-control'}),
			'adress': forms.TextInput(attrs={'class':'form-control'}),
			'phone':forms.TextInput(attrs={'class':'form-control'}),
			'tipo_profesional': forms.Select(attrs={'class':'form-control'}),
			'usuario':forms.Select(attrs={'class':'form-control'}),
			
			'establecimiento': forms.CheckboxSelectMultiple(),
			
		}

class CargoForm(forms.ModelForm):
	
	class Meta:
		model = Cargo
		fields = [
			
			'profesional',
			'escuela',
			'tipo_profesional',
			'cantidad_horas_convivencia',
			'cantidad_horas_dupla',
			
		]
		labels = {
			
			
			'profesional':'Seleccione  usuario para crear Profesional',	
			'escuela':'Selecione establecimiento',
			'tipo_profesional':'Selecione el tipo de profesional',
			'cantidad_horas_convivencia':'Cantidad de horas de Encargado de Convivencia',
			'cantidad_horas_dupla':'Cantidad de horas de Encargado de Dupla PsicoSocial',
			
		}
		widgets = {
			
			'profesional':forms.Select(attrs={'class':'form-control'}),
			'escuela':forms.Select(attrs={'class':'form-control'}),
			'tipo_profesional':forms.Select(attrs={'class':'form-control'}),
			'cantidad_horas_convivencia':forms.TextInput(attrs={'class':'form-control'}),
			'cantidad_horas_dupla':forms.TextInput(attrs={'class':'form-control'}),
		}




class ProfesinalEstablecimientoForm(forms.ModelForm):
	
	class Meta:
		model = Profesional
		fields = [
			
			'establecimiento',
		]
		labels = {
			
			
			'establecimiento':'Seleccione establecimiento',	
			
		}
		widgets = {
			
			'establecimiento':forms.Select(attrs={'class':'form-control'}),
			
			
		}

class Acciones_profesionalForm(forms.ModelForm):
	
	class Meta:
		model = Acciones_profesional
		fields = [
			
			'tipo_accion',
			'objetivo',
			'descripcion',
			'cantidad',
			


		]
		labels = {
			
			
			'tipo_accion':'Seleccione tipo de acción profesional a realizar',
			'objetivo':'Objetivo',	
			'descripcion':'Aspectos Relevantes y/o Sistematizacón',	
			'cantidad':'Cantidad realizada',	
			
			
		}
		widgets = {
			
			'tipo_accion':forms.Select(attrs={'class':'form-control'}),
			'objetivo':forms.TextInput(attrs={'class':'form-control'}),
			'descripcion':forms.TextInput(attrs={'class':'form-control'}),
			'cantidad':forms.Select(attrs={'class':'form-control'}),
			
			
			
		}

