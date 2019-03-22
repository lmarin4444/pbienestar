# -*- coding: utf-8 -*-
#from  bootstrap_datepicker.widgets  import  DatePicker
from django import forms
from alumno.models import Estudiante
from alumno.models import establecimiento
from alumno.models import curso
from alumno.models import apoderado, hermano,Escolaridad
from profesional.models import Profesional
#from alumno.models import tutor, Pariente
from alumno.models import Parentesco

class EstudianteForm(forms.ModelForm):

	class Meta:
		model = Estudiante

		fields = [
			
			'nombres',
			'firs_name',
			'last_name',
			'fecha_nacimiento',
			'edad',
			'rut',
			'domicilio_estudiante',
		]
		labels = {
			'nombres': 'Nombres',
			'firs_name':'Apellido Paterno',
			'last_name': 'Apellido Materno',
			'fecha_nacimiento':' Fecha nacimiento',
			'edad':'Edad',
			'rut ': 'Rut: (Ingresar sin puntos, con dígito verificador)',
			'domicilio': 'Domicilio',
			
		}
		widgets = {
			'nombres': forms.TextInput(attrs={'class':'form-control'}),
			'firs_name': forms.TextInput(attrs={'class':'form-control'}),
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_nacimiento':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'edad': forms.TextInput(attrs={'readonly':'readonly'}),
			'rut': forms.TextInput(attrs={'readonly':'readonly'}),
			'domicilio_estudiante': forms.TextInput(attrs={'class':'form-control'}),

		}


class EstudianteVerForm(forms.ModelForm):

	class Meta:
		model = Estudiante

		fields = ['rut',]
		labels = {'rut ': 'Rut: (Ingresar sin puntos, con dígito verificador)',}
		widgets = {'rut': forms.TextInput(attrs={'class':'form-control'}),}


class EstudianteNombresForm(forms.ModelForm):

	class Meta:
		model = Estudiante

		fields = ['nombres','firs_name','last_name']
		labels = {
		'nombres ': 'Nombres',
		'firs_name ': 'Apellido Paterno',
		'last_name': 'Apellido Materno',

					}
		widgets = {
		'nombres': forms.TextInput(attrs={'class':'form-control'}),
		'firs_name': forms.TextInput(attrs={'class':'form-control'}),
		'last_ame': forms.TextInput(attrs={'class':'form-control'}),

		}



class EstudianteFormVersinrut(forms.ModelForm):

	class Meta:
		model = Estudiante

		fields = [
			
			'nombres',
			'firs_name',
			'last_name',
			'fecha_nacimiento',
			'domicilio_estudiante',
	
		
		]
		labels = {
			'nombres': 'Nombres',
			'firs_name':'Apellido Paterno',
			'last_name': 'Apellido Materno',
			'fecha_nacimiento':' Fecha_nacimiento',
			'domicilio': 'Domicilio',
	
		
		}
		widgets = {
			'nombres': forms.TextInput(attrs={'class':'form-control'}),
			'firs_name': forms.TextInput(attrs={'class':'form-control'}),
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
			#'fecha_nacimiento':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'domicilio_estudiante': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_nacimiento':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			#'fecha_nacimiento': forms.DateInput(format='%m/%d/%Y', attrs={'class': 'form-control bs-datepicker', 'placeholder': 'Seleccione la fecha Correcta'})

			
			
		}

class EstudianteFormUpdate(forms.ModelForm):

	class Meta:
		model = Estudiante

		fields = [
			
			'nombres',
			'firs_name',
			'last_name',
			'fecha_nacimiento',
			'edad',
			'domicilio_estudiante',
		
		
		]
		labels = {
			'nombres': 'Nombres',
			'firs_name':'Apellido Paterno',
			'last_name': 'Apellido Materno',
			'fecha_nacimiento':' Fecha nacimiento',
			'edad':'Edad',
			'domicilio': 'Domicilio',
			
		
		}
		widgets = {
			'nombres': forms.TextInput(attrs={'class':'form-control'}),
			'firs_name': forms.TextInput(attrs={'class':'form-control'}),
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_nacimiento':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'edad': forms.TextInput(attrs={'class':'form-control'}),
		
			'domicilio_estudiante': forms.TextInput(attrs={'class':'form-control'}),
			
	
		}

class cursoForm(forms.ModelForm):

	class Meta:
		model = curso
		fields = [
			'numero',
			'letra',
			'establecimiento',
			'Profesor',	
		]
		labels = {
			'numero': 'Numero de mascotas',
			'letra': 'Razones para adoptar',
			'establecimiento':'Establecimiento',
			'Profesor':'Profesor del curdo',
		}
		widgets = {
			'numero':forms.Select(attrs={'class':'form-control'}),
			'letra':forms.Select(attrs={'class':'form-control'}),
			'establecimiento':forms.Textarea(attrs={'class':'form-control'}),
			'Profesor':forms.Textarea(attrs={'class':'form-control'}),
		}

class EstablecimientoForm(forms.ModelForm):

	class Meta:
		model = establecimiento

		fields = [
			'nombre',
			'Rbd',
			'localidad',
			'clave',
			'director',
			'telefono',
			'cantidad',
			'saldo',	

		]
		labels = {
			'nombre ': 'Establecimiento',
			'Rbd': 'Numero de rbd',
			'localidad':'Localidad',
			'clave': 'indicador de clave',
			'director': 'Director',
			'telefono':' Telefono:',
			'cantidad':'Cupo de estudiantes',
			'saldo':'Cupo actual',

		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'Rbd': forms.TextInput(attrs={'class':'form-control'}),
			'localidad': forms.TextInput(attrs={'class':'form-control'}),
			'clave': forms.TextInput(attrs={'class':'form-control'}),
			'director': forms.TextInput(attrs={'class':'form-control'}),
			'telefono': forms.TextInput(attrs={'class':'form-control'}),
			'cantidad': forms.TextInput(attrs={'class':'form-control'}),
			'saldo': forms.TextInput(attrs={'class':'form-control'}),

		}




class ParentescoForm(forms.ModelForm):

	class Meta:
		model = Parentesco

		fields = [
			
			'nombre',
			'apellido_p',			
			'apellido_m',
			'parentesco',
			'edad',
			'ocupacion',
			'Escolaridad',
			'opcion',
			
			

		]
		labels = {
			
			'nombre': 'Nombre del integrante de la familia:',
			'apellido_p': 'Apellido Paterno',
			'apellido_m': 'Apellido Materno',
			'parentesco': 'Parentesco',
			'edad':'Edad',
			'ocupacion':'Ocupacion',
			'Escolaridad':'Escolaridad',
			'opcion':'Indique SÍ -> si el familiar vive con el niño o niña en la misma casa y NO -> si el familia no vive en la misma casa',
			
			
			

		}
		widgets = {
			
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'apellido_p': forms.TextInput(attrs={'class':'form-control'}),
			'apellido_m': forms.TextInput(attrs={'class':'form-control'}),
			'parentesco': forms.Select(attrs={'class':'form-control'}),
			'edad': forms.TextInput(attrs={'class':'form-control'}),
			'ocupacion': forms.TextInput(attrs={'class':'form-control'}),
			'Escolaridad': forms.Select(attrs={'class':'form-control'}),
			'opcion': forms.Select(attrs={'class':'form-control'}),
			
			
			
			
		}


class ApoderadoForm(forms.ModelForm):

	class Meta:
		model = apoderado

		fields = [
			
			'rut',
			'nombre',
			'apellido_p',			
			'apellido_m',
			'parentesco',
			'edad',
			'ocupacion',
			'Escolaridad',
			'opcion',
			'domicilio',
			'telefono',
		

			
		]
		labels = {
			
			'rut': 'Rut del apoderado:',
			'nombre': 'Nombre del integrante de la familia:',
			'apellido_p': 'Apellido Paterno',
			'apellido_m': 'Apellido Materno',
			'parentesco': 'Parentesco',
			'edad':'Edad',
			'ocupacion':'Ocupación',
			'Escolaridad':'Escolaridad',
			'opcion':'Indique SÍ -> si el familiar vive con el niño o niña y/o adolescente en la misma casa y NO -> si el familia no vive en la misma casa',
			
			'domicilio': 'Domicilio apoderado',
			'telefono':'Teléfono',
			
			

		}
		widgets = {
			
			'rut': forms.TextInput(attrs={'class':'form-control'}),
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'apellido_p': forms.TextInput(attrs={'class':'form-control'}),
			'apellido_m': forms.TextInput(attrs={'class':'form-control'}),
			'parentesco': forms.Select(attrs={'class':'form-control'}),
			'edad': forms.TextInput(attrs={'class':'form-control'}),
			'ocupacion': forms.TextInput(attrs={'class':'form-control'}),
			'Escolaridad': forms.Select(attrs={'class':'form-control'}),
			'opcion': forms.Select(attrs={'class':'form-control'}),
			'domicilio': forms.TextInput(attrs={'class':'form-control'}),
			'telefono': forms.TextInput(attrs={'class':'form-control'}),
			
			
			
		}





class HermanoForm(forms.ModelForm):

	class Meta:
		model = hermano

		fields = [
			
			'rut',
			'nombre',
			'apellido_p',			
			'apellido_m',
			'parentesco',
			'edad',
			'ocupacion',
			'Escolaridad',
			'opcion',
			'curso',
			'establecimiento', 
			'pertenece_centro', 
		

			
		]
		labels = {
			
			'rut': 'Rut del hermano:',
			'nombre': 'Nombre del integrante de la familia:',
			'apellido_p': 'Apellido Paterno',
			'apellido_m': 'Apellido Materno',
			'parentesco': 'Parentesco',
			'edad':'Edad',
			'ocupacion':'Ocupacion',
			'Escolaridad':'Escolaridad',
			'opcion':'Indique SÍ -> si el familiar vive con el niño o niña en la misma casa y NO -> si el familia no vive en la misma casa',
			'curso':'Ingrese el curso',
			'establecimiento':'Establecimiento educacional', 
			'pertenece_centro':'Pertencece al centro de bienestar?', 
	

		}
		widgets = {
			
			'rut': forms.TextInput(attrs={'class':'form-control'}),
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'apellido_p': forms.TextInput(attrs={'class':'form-control'}),
			'apellido_m': forms.TextInput(attrs={'class':'form-control'}),
			'parentesco': forms.Select(attrs={'class':'form-control'}),
			'edad': forms.TextInput(attrs={'class':'form-control'}),
			'ocupacion': forms.TextInput(attrs={'class':'form-control'}),
			'Escolaridad': forms.Select(attrs={'class':'form-control'}),
			'opcion': forms.Select(attrs={'class':'form-control'}),
			'curso': forms.TextInput(attrs={'class':'form-control'}),
			'establecimiento': forms.Select(attrs={'class':'form-control'}),
			'pertenece_centri': forms.Select(attrs={'class':'form-control'}),
				
			}

class EscolaridadForm(forms.ModelForm):

		
	class Meta:
		model = Escolaridad

		fields = [
			
			'curso',			
			'Letra',
			
		]
		labels = {
			
			'curso': 'Curso',
			'Letra': 'Letra',
			
		}
		widgets = {
			
			'curso': forms.Select(attrs={'class':'form-control'}),
			'Letra': forms.Select(attrs={'class':'form-control'}),
			
			
		}
class EscolaridadActualizaForm(forms.ModelForm):

		
	class Meta:
		model = Escolaridad

		fields = [
			'anno',
			'fecha_inicio',
			'fecha_termino',
			'conducta',
			'rendimiento',

			'curso',			
			'Letra',
			
		]
		labels = {
			'anno':'Año',
			'fecha_inicio':'Fecha de incio del período escolar(Solo si es por período)',
			'fecha_termino':'Fecha de término del período escolar (Solo si es por período)',
			'conducta':'Breve descripción de la conducta del estudiante',
			'rendimiento':'Breve descripción de la conducta del estudiante',
			'curso': 'Curso',
			'Letra': 'Letra',
			
		}
		widgets = {
			'anno': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_incio':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'fecha_termino':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'conducta':forms.Textarea(attrs={'class':'form-control'}),
			'rendimiento':forms.Textarea(attrs={'class':'form-control'}),
			'curso': forms.Select(attrs={'class':'form-control'}),
			'Letra': forms.Select(attrs={'class':'form-control'}),
			
			
		}
class EscolaridadActualizaFormCentro(forms.ModelForm):

		
	class Meta:
		model = Escolaridad

		fields = [
			'anno',
			'fecha_inicio',
			'fecha_termino',
			'conducta',
			'rendimiento',
			'establecimiento',
			'curso',			
			'Letra',
			
		]
		labels = {
			'anno':'Año',
			'fecha_inicio':'Fecha de incio del período escolar(Solo si es por período)',
			'fecha_termino':'Fecha de término del período escolar (Solo si es por período)',
			'conducta':'Breve descripción de la conducta del estudiante',
			'rendimiento':'Breve descripción de la conducta del estudiante',
			'establecimiento':'Selecionar establecimiento',
			'curso': 'Curso',
			'Letra': 'Letra',
			
		}
		widgets = {
			'anno': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_incio':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'fecha_termino':forms.TextInput(attrs={'"format": "DD-MM-YYYY",class':'datepicker','placeholder':'Ingresar Fecha '}),
			'conducta':forms.Textarea(attrs={'class':'form-control'}),
			'rendimiento':forms.Textarea(attrs={'class':'form-control'}),
			'establecimiento': forms.Select(attrs={'class':'form-control'}),
			'curso': forms.Select(attrs={'class':'form-control'}),
			'Letra': forms.Select(attrs={'class':'form-control'}),
			
			
		}
# Formulario para seleccionar el curso para una accion de convivencia escolar
class CursoForm(forms.ModelForm):

	class Meta:
		model = curso

		fields = [
			
			'numero',
			'letra',
			
		]
		labels = {
			'numero': 'Seleccionar curso',
			'letra':'Seleccionar letra',
			
			
		}
		widgets = {
			'numero': forms.Select(attrs={'class':'form-control'}),
			'letra': forms.Select(attrs={'class':'form-control'}),
			
			
		

		}

# Busqueda de estudiantes por nombre
class EstudiantebusquedaNombreForm(forms.ModelForm):

	class Meta:
		model = Estudiante

		fields = [
			
			'nombres',
			'firs_name',
			'last_name',
			
		]
		labels = {
			'nombres': 'Nombres',
			'firs_name':'Apellido Paterno',
			'last_name': 'Apellido Materno',
			
		}
		widgets = {
			'nombres': forms.TextInput(attrs={'class':'form-control'}),
			'firs_name': forms.TextInput(attrs={'class':'form-control'}),
			
		}

